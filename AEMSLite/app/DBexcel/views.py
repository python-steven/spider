from django.shortcuts import render
from app.login.models import PartItemResult,PartItem
from app.DBexcel.mod_excel import Excel_operation
from AEMSLite.settings import BASE_DIR
from app.maintain_monitor.views import Check_monitor_equipment
from app.NGrate.views import check_NGRate
from app.mail import send_mail
from bs4 import BeautifulSoup
from django.db import connection
from datetime import datetime, date, timedelta
from . import mod_logger
import time
import os, sys
import filetype
import traceback

def crontab_test():
    print(datetime.now()," :NGRate")
    check_NGRate()
    # print(data)  test data if normal
    time.sleep(2)
    print(datetime.now()," :Check_monitor_equipment")
    Check_monitor_equipment()

logger = mod_logger.Logger("debug")     # 日志记录

def deal_not_excel(filepath):
    with open(filepath,'r') as f:
        content = f.read()
    content.strip().replace('\ufeff', '')
    soup = BeautifulSoup(content, 'lxml')
    table = soup.findAll("table")[0]
    rows = table.findAll("tr")
    result = []
    for row in rows:
        cols = row.findAll(['td', 'th'])
        foo = []
        for col in cols:
            foo.append(col.getText())
        result.append(foo)

    return result

def insert_partItemResult(rows):
    insert_list = []
    count = 0
    for i in range(len(rows)):
        if rows[i]['RESULT'] == 'FAIL':    # 只插入FAIL
            SN_foo = PartItemResult.objects.filter(SN=rows[i]['SN'])

            # 当SN和TrnDate同时重复时不插入
            if not(SN_foo and rows[i]['TRNDATE'] in [SN.TrnDate for SN in SN_foo]):
                case = PartItemResult(
                    USN=rows[i]['USN'], SN=rows[i]['SN'], OSN=rows[i]['OSN'], Asset=rows[i]['ASSET'],
                    PN=rows[i]['PN'], PartName=rows[i]['PARTNAME'], Spec=rows[i]['SPEC'],
                    UsedTimes=rows[i]['USETIMES'], Stage=rows[i]['STAGE'], FixtureId=rows[i]['FIXTUREID'],
                    Result=rows[i]['RESULT'], ErrorCode=rows[i]['ERRORCODE'], TrnDate=rows[i]['TRNDATE'],
                    PlantCode=rows[i]['PLANTCODE'],
                )
                insert_list.append(case)
                count += 1
            else:
                rows[i] = None      # 标识None，避免后续PartItem处理
    try:
        PartItemResult.objects.bulk_create(insert_list)
    except Exception as e:
        raise e
    return count

# 批量插入/更新到PartItem 表
def update_partItem(rows):
    # sql = 'select max("USN"),"SN",max("OSN"),max("PN"),max("PartName"),max("Spec"),max("UsedTimes") as "UsedTimes",' \
    #       'count(case when "Result"=\'FAIL\' then "Result" else null end) as "ErrorCounts",max("TrnDate") as TrnDate ' \
    #       'from "PartItemResult" group by "SN";'
    count_in = 0    # 插入统计
    count_up = 0    # 更新统计
    pi_list = {}    # 整理待插入数据
    pu_list = {}    # 整理待更新数据
    for row in rows:
        if row:
            SN_foo = PartItem.objects.filter(SN=row['SN'])
            if SN_foo:      # 整理表内已有SN的数据放入pu_list中待更新
                SN_foo = SN_foo[0]
                if SN_foo not in pu_list.keys():
                    pu_list[SN_foo] = dict(zip(rows[0], [0] * 14))
                    pu_list[SN_foo]['TRNDATE'] = None
                foo = pu_list[SN_foo]
                foo['SN'] = row['SN']
                foo['OSN'] = row['OSN']
                foo['USN'] = row['USN']
                foo['PN'] = row['PN']
                foo['USETIMES'] = max(foo['USETIMES'], row['USETIMES'])
                foo['TRNDATE'] = max(foo['TRNDATE'], row['TRNDATE']) if foo['TRNDATE'] else row['TRNDATE']
                foo['PARTNAME'] = row['PARTNAME']
                foo['SPEC'] = row['SPEC']
                foo['RESULT'] += 1 if row['RESULT'] == 'FAIL' else 0
                pu_list[SN_foo] = foo
            else:       # 整理表内没有SN的数据放入pi_list中待插入
                if row['SN'] not in pi_list.keys():
                    pi_list[row['SN']] = dict(zip(rows[0], [0]*14))
                    pi_list[row['SN']]['TRNDATE'] = None

                foo = pi_list[row['SN']]
                foo['SN'] = row['SN']
                foo['OSN'] = row['OSN']
                foo['USN'] = row['USN']
                foo['PN'] = row['PN']
                foo['USETIMES'] = max(foo['USETIMES'], row['USETIMES'])
                foo['TRNDATE'] = max(foo['TRNDATE'], row['TRNDATE']) if foo['TRNDATE'] else row['TRNDATE']
                foo['PARTNAME'] = row['PARTNAME']
                foo['SPEC'] = row['SPEC']
                foo['RESULT'] += 1 if row['RESULT'] == 'FAIL' else 0
                pi_list[row['SN']] = foo

    # 插入数据
    insert_list = []
    for value in pi_list.values():
        NG_rate = round(value['RESULT']/value['USETIMES'], 10)
        case = PartItem(
            SN=value['SN'], OSN=value['OSN'],PN=value['PN'],
            PartName=value['PARTNAME'], Spec=value['SPEC'],
            UsedTimes=value['USETIMES'], NextCheckDate=None,
            ErrorCounts=value['RESULT'],TrnDate=value['TRNDATE'],
            NGRate=NG_rate, PlantCode=value['PLANTCODE'],
        )
        insert_list.append(case)
        count_in += 1
    if insert_list:
        PartItem.objects.bulk_create(insert_list)

    # 更新数据
    for key, value in pu_list.items():
        key.SN = value['SN']
        key.OSN = value['OSN']
        key.PN = value['PN']
        key.PartName = value['PARTNAME']
        key.Spec = value['SPEC']
        key.UsedTimes = max(key.UsedTimes, value['USETIMES'])
        key.NextCheckData = None
        key.ErrorCounts += value['RESULT']
        key.TrnDate = max(value['TRNDATE'], key.TrnDate)
        key.NGRate = round(key.ErrorCounts / key.UsedTimes, 10)
        key.PlantCode = value['PLANTCODE']
        key.save()
        count_up += 1

    return count_in, count_up

def get_cleaned_data(rows):
    # 判断是否有厂别
    if 'PlantCode' in rows[0]:
        plc = True
    else:
        plc = False
        rows[0].append('PLANTCODE')

    rows[0] = [str(x).upper() for x in rows[0]]

    new_rows = []

    for row in rows[1:]:
        new_row = dict(zip(rows[0], row))
        new_row['PLANTCODE'] = None if plc else new_row['PLANTCODE']    # 厂别
        new_row['USETIMES'] = int(new_row['USETIMES'])
        if new_row['TRNDATE'][-2:].upper() == 'PM':
            new_row['TRNDATE'] = datetime.strptime(new_row['TRNDATE'], '%m/%d/%Y %H:%M:%S %p') + timedelta(0.5)
        else:
            new_row['TRNDATE'] = datetime.strptime(new_row['TRNDATE'], '%m/%d/%Y %H:%M:%S %p')
        new_row['STAGE'] = new_row['STAGE'][:2]
        new_row['RESULT'] = 'FAIL' if 'fail' in new_row['RESULT'].lower() else 'PASS'
        new_rows.append(new_row)

    # for i, j in new_rows[0].items():
    #     print(i+' '+str(type(j)))
    # new_rows.sort(key=lambda x: x['TRNDATE'])     # 排序


    return new_rows

def main():
    logger.info(date.today().strftime('%Y-%m-%d'))
    pathname = os.path.join(BASE_DIR, 'app/DBexcel')
    excel_operation = Excel_operation(pathname)
    start = time.time()
    try:
        file_paths = excel_operation.get_xlsx_list()  # 获取目录下的excel文件列表
    except Exception as e:
        file_paths = []
        logger.error(u"从目录中获取excel文件列表失败,异常信息：%s" % str(e))

    pir_insert = 0   # partItemResult 插入行数统计
    pi_update = 0    # partItem 更新行数统计
    pi_insert = 0    # partItem 插入行数统计
    all_count = 0    # 所有行数统计

    for file_path in file_paths:
        logger.info(u'开始处理文件：%s' % file_path)
        try:
            if filetype.guess(file_path):
                rows = excel_operation.read_by_row(file_path, 0)
            else:
                rows = deal_not_excel(file_path)
        except Exception as e:
            rows = []
            logger.error(u'无法处理该文件类型, 文件名：%s, 异常信息: %s' % (file_path, str(e)))

        rows = get_cleaned_data(rows)
        all_count += len(rows)

        try:
            pir_insert += insert_partItemResult(rows)
        except Exception as e:
            logger.error("操作PartItemResult失败，异常信息: %s : %s" % (traceback.print_exc(), str(e)))

        try:
            i, j = update_partItem(rows)
            pi_insert += i
            pi_update += j
        except Exception as e:
            logger.error('操作PartItem失败，异常信息: %s : %s' % (traceback.print_exc(), str(e)))


        excel_operation.solved_backup(file_path)

    logger.info('total %d rows' % all_count)
    logger.info('insert PartItemResult %d rows' % pir_insert)
    logger.info('update PartItem %d rows' % pi_update)
    logger.info('insert PartItem %d rows' % pi_insert)
    logger.info('spent %d s\n' % (time.time()-start))

def getYesterday():
    today = date.today()
    one_day = timedelta(days=1)
    yesterday = today-one_day
    return yesterday

def send_log(receiver):
    log_path = os.path.join(BASE_DIR, 'app/DBexcel/log')
    today = date.today()
    tomorrow = getYesterday()
    log_file_path = os.path.join(log_path, today.strftime("%Y-%m-%d.log"))
    with open(log_file_path, 'r') as f:
        context = f.read()
    subject = tomorrow.strftime("%Y-%m-%d") + ' - DBexcel日志文件'
    send_mail(receiver, subject, context, 'plain')