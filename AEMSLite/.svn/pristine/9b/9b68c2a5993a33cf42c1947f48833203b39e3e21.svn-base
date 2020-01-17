# from app.login.models import BudgetCodeForm
# from django.db import connection
# from app import restful
from openpyxl import load_workbook,Workbook
# from AEMSLite.app.login import BudgetCodeForm
import time
import os
import psycopg2

conn = psycopg2.connect(
                database="aemslite",
                host="127.0.0.1",
                user="postgres",
                password = "1234qwer!@#$QWER",
                port = 5432,

            )

cur=conn.cursor()

partname = 'C'
sql1 = '''SELECT a.attname as name FROM pg_class as c,pg_attribute as a where c.relname = '%s' and a.attrelid = c.oid and a.attnum>0 and a.attrelid is not null ''' % 'PartItem'
sql9 = 'select "PartItem"."SN","PartItem"."PartName","PartItem"."NGRate","PartItem"."ErrorCounts","UsedTimes" from "PartItem" where "Id"=63'

# sql2 = 'select  COUNT("PartName") from "PartItem" where "PartName" in (select distinct "PartName" from "PartItem")'
sql2 ='SELECT "PartName", COUNT("PartName") FROM "PartItem" where '
sql3 =sql1+'where name in("SN","PartName","NGRate","ErrorCounts","UsedTimes")'
#正常
sql4 = sql2 + '"NGRate" < \'' + '0.01' + '\'group by "PartName"'
#预警
sql5 = sql2 + '"NGRate" >= \'' + '0.01' + '\'' \
      + 'AND "NGRate" <= \'' + '2' + '\'group by "PartName"'
#超标
sql6 = sql2 + '"NGRate" > \'' + '2' + '\'group by "PartName"'

sql7 = 'select "PartName" from "PartItem" where "PartName" like \'%{0}%\''.format(partname)

sql10 = 'SELECT "SN","PartName","NGRate","ErrorCounts","UsedTimes","Configuration"."Min","Configuration"."Max" FROM "PartItem" INNER JOIN "Configuration" on "Configuration"."Id"=2 AND "PartItem"."Id" IN (63,64,65)'
sql11 = 'select "Max","Min" from "Configuration" where "Id"=2 '

# print(sql1)
a = 32,33,34
sql2 = 'select "BudgetCodeForm"."ExternalNumberType","Department","Remark","AttachmentPath","BillingType","BudgetCode","ExternalNumber"' \
               ',"ApplyDate","ExternalNumberEffectiveDate","Pic","ProductName","Model","PurchaseType","UnitPrice"' \
               ',"Quantity","Unit","Currency","Customer","TypeOfMachine","ProjectCode","ApplyReason" from "BudgetCodeForm" '
#所有的SN按ErrorCode分类统计出各ErrorCode类的SN数量所有的SN按ErrorCode分类统计出各ErrorCode类的SN数量
sl= 'SELECT "ErrorCode", COUNT("SN") FROM "PartItemResult" where "Result"= \'FAIL\' GROUP BY "ErrorCode"'
#所有的SN按品名分类统计出各品名类的SN数量
sl2 = 'SELECT "PartName", COUNT("SN") FROM "PartItemResult" GROUP BY "PartName"'
#所有的result 为Fail的SN按fail次数落在user设定fail次数范围区间统计出这些SN（会有重复的SN）的数量
sl3_1 = 'SELECT COUNT("SN") FROM "PartItemResult" where "Result"= \'FAIL\' and "UsedTimes">0 and "UsedTimes" <1000'
sl3_2 = 'SELECT COUNT("SN") FROM "PartItemResult" where "Result"= \'FAIL\' and "UsedTimes">=1000 and "UsedTimes" <=1500'
sl3_3 = 'SELECT COUNT("SN") FROM "PartItemResult" where "Result"= \'FAIL\' and "UsedTimes">=1500 and "UsedTimes" <=2000'
#所有的result 为Fail的SN按品名分类统计出的SN（过滤重复的SN）的数量
sl4 = 'SELECT "PartName", COUNT("SN") FROM (select distinct "SN","PartName","Result" from "PartItemResult") as foo  where "Result"= \'FAIL\' GROUP BY "PartName"'
def tes():
    cur.execute(sl)
    data = cur.fetchall()
    print(data)

    cur.execute(sl2)
    data = cur.fetchall()
    print(data)

    cur.execute(sl3_1)
    data = cur.fetchall()
    cur.execute(sl3_2)
    data_2 = cur.fetchall()
    cur.execute(sl3_3)
    data_3 = cur.fetchall()
    data.append(data_2[0])
    data.append(data_3[0])
    print(data)

    cur.execute(sl4)
    data = cur.fetchall()
    print(data)
tes()

# time_num = int(time.time())
# time_num = str(time_num)
# sheet_name = "预算表单1"
# filename = 'download' + time_num + '.xlsx'
#
# wb = Workbook()
# index = 0
# wb.create_sheet(sheet_name, index=index)
# sheet = wb[sheet_name]
# for row in data:
#     sheet.append(row)
# wb.save(os.path.join('/home/AEMSLite/AEMSLite/report/', filename))


# file_url = request.build_absolute_uri(settings.MEDIA_CHANGE_URL + filename)
# download_url = []
# download_url[0] = file_url
# return restful.ok(data=download_url)

# sql3 = sql2 +'"Id" IN '+str(a)
# print(type(a))
# print(sql3)
# 产生表头信息
# data =[attr[0] for attr in data]
# # print(data.index("SN"))
# data1 =[]
# data1.append(data[data.index("SN")])
# data1.append(data[data.index("PartName")])
# data1.append('Min')
# data1.append('Max')
# data1.append(data[data.index("NGRate")])
# data1.append(data[data.index("ErrorCounts")])
# data1.append(data[data.index("UsedTimes")])
# data1.append("status")
# # print(data,len(data))
# print(data1)
# # #产生表信息
# cur.execute(sql10)
# data2 = cur.fetchall()
# data2.insert(0,data1)
# print(data2, len(data2))
# for row in data2:
#     if row[]
# budget_user = BudgetCodeForm.objects.filter(Id__in=[15,16]).values("Signer").distinct().count()
# print()