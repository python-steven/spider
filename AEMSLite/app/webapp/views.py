from datetime import datetime,timedelta,date
import json
from django.db import connection
from django.http import JsonResponse,HttpResponse
from app import restful,rizhi
from django.views.decorators.csrf import csrf_exempt
from app.login.models import User,Department,Customer,BudgetCodeForm,PartItem,PartItemResult,MaintenanceLog,Configuration
import traceback
log_text = rizhi.Rookie(set_level="INFO", log_name="logging.log", log_path='/home/AEMSLite', )
#用户登录
@csrf_exempt
def webapp_login(request):
    try:
        if request.method == "POST":
            try:
                data = json.loads(request.body)
                input_user_id = data.get('user_id','')
                input_password = data.get('u_password','')
            except:
                return restful.params_error(message='data error',data='error')
            if input_user_id != "":
                user = User.objects.get(EmployeeId=input_user_id)
                user_password = user.Password
                if (user_password == input_password):
                    return restful.ok(message='login success',data="ok")
                else:
                    return restful.params_error(message='password error',data='error')
            else:
                return restful.params_error(message='account error',data='error')
            
        else:
            return restful.params_error(message='method error',data='error')
    except Exception as e:
        return restful.params_error(message="网络错误",data='error')


#设备列表筛选
@csrf_exempt
def webapp_ListFiltrate(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            input_start_time = data.get('start_time')
            input_end_time = data.get('end_time')
            input_sn = data.get('sn')
            input_part_name = data.get('part_name')
            input_maintainer = data.get('maintainer')
        except:
            return JsonResponse({"data":"get data error"}, safe=False, json_dumps_params={'ensure_ascii': False})
        #获取数据
        # count_count = Configuration.objects.get(Type="mt_count")
        # date = Configuration.objects.get(Type="mt_date")
        # count_max_value = int(count_count.Max)
        # day_max_value = int(date.Max)
        # start = datetime.now()
        # start_select = (list(PartItem.objects.order_by("-TrnDate").filter(TrnDate__lte=start).values("TrnDate")))[0]['TrnDate']
        # end = start_select - timedelta(days=7)
        try:
            cur = connection.cursor()
            sql = 'select "Id","SN","PN","CheckCycleCount","UsedTimes","CheckCycle",to_char("NextCheckDate",\'yyyy-MM-dd HH24:MI:SS\'),"NextCheckCount","PartName","WarningBeforeDays","WarningBeforeTimes","Maintainer" FROM "PartItem" WHERE "UseStatus"=\'normal\''
            #     'SELECT "Id","SN","PN","CheckCycleCount","UsedTimes","CheckCycle","NextCheckDate","NextCheckCount","PartName","WarningBeforeDays","WarningBeforeTimes" FROM "PartItem" where "UseStatus"=\'normal\' '
            # sql = sql + ' AND to_char("TrnDate",\'yyyy-MM-dd HH24:MI:SS\') >=\' ' + end.strftime("%Y-%m-%d %H:%M:%S") + '\' '
            if input_sn != "":
                sql = sql+' AND "SN" =\'' + input_sn + '\''
            if input_part_name != "":
                sql = sql+' AND "PartName" ilike \'%' + input_part_name + '%\''
            if input_maintainer != "":
                sql = sql+' AND "Maintainer" ilike \'%' + input_maintainer + '%\''
            #判断是否在选定的时间范围内
            if input_start_time != "" and input_end_time != "":
                start_time=datetime(int(input_start_time[0:4]),int(input_start_time[5:7]),int(input_start_time[8:10]),00,00,00)
                end_time=datetime(int(input_end_time[0:4]),int(input_end_time[5:7]),int(input_end_time[8:10]),23,59,59)
                sql = sql+' AND "TrnDate">= \'%{0}%\' AND "TrnDate"<= \'%{1}%\''.format(start_time, end_time)
            elif input_start_time != "" and input_end_time == "":
                start_time=datetime(int(input_start_time[0:4]),int(input_start_time[5:7]),int(input_start_time[8:10]))
                sql = sql+' AND "TrnDate">= \'%{0}%\''.format(start_time)
            elif input_start_time == "" and input_end_time != "":
                end_time=datetime(int(input_end_time[0:4]),int(input_end_time[5:7]),int(input_end_time[8:10]),23,59,59)
                sql = sql+' AND "TrnDate"<= \'%{0}%\''.format(end_time)
            # elif input_start_time == "" and input_end_time == "":
                # sql = sql +' AND to_char("TrnDate",\'yyyy-MM-dd HH24:MI:SS\') >=\' '+ end.strftime("%Y-%m-%d %H:%M:%S")+'\''
            sql =sql +' order by "Id"'
            cur.execute(sql)
            data = cur.fetchall()
        except:
            msg_err = "error: connect DB fail "
            return JsonResponse({"data":msg_err}, safe=False, json_dumps_params={'ensure_ascii': False})
        data_arr = []
        data1 = tidy(data)
        for i in range(len(data1)):
            data_arr.append({"Id": data[i][0], "SN": data[i][1], "PN": data[i][2], "PartName": data[i][8],
                             "CheckCycleCount": data[i][4], "UsedTimes": data[i][4], "CheckCycle": data[i][5],
                             "NextCheckDate": data[i][6],
                             "Maintainer": data[i][11], "Status": data[i][-1]})
        # for i in range(len(data)):
        #     status = ""
        #     day_result = 0
        #     count_result= 0
        #     if data[i][6] != None:
        #         day_result = (datetime.strptime(str(data[i][6]).split(' ')[0], "%Y-%m-%d") - datetime.strptime(str(datetime.now()).split(' ')[0], "%Y-%m-%d")).days
        #     if data[i][8] != 0:
        #         count_result = int(data[i][8]) - int(data[i][4])
        #     #计算状态的算法
        #     if data[i][6] == None and data[i][8] == 0:
        #         status = 'none'
        #     if data[i][6] != None and data[i][8] == 0:
        #         if day_result < 0:
        #             status = "OVERPROOF"
        #         if 0<=day_result <= (day_max_value * data[i][5]):
        #             status = "WARNING"
        #         if day_result >(day_max_value * data[i][5]):
        #             status = "NORMAL"
        #     if data[i][6] == None and data[i][8] != 0:
        #         # count_result = int(data[i][8]) - int(data[i][4])
        #         if count_result <0:
        #             status = "OVERPROOF"
        #         if 0<=count_result<=(count_max_value * data[i][3]):
        #             status = "WARNING"
        #         if count_result >(count_max_value * data[i][3]):
        #             status = "NORMAL"
        #     if data[i][6] != None and data[i][8] != 0:
        #         if count_result <0 or day_result <0:
        #             status ="OVERPROOF"
        #         else:
        #             if count_result >(count_max_value * data[i][3]) and day_result >(day_max_value * data[i][5]):
        #                 status = "NORMAL"
        #             else:
        #                 status = "WARNING"
        #     data_arr.append({"Id":data[i][0],"SN":data[i][1],"PN":data[i][10],"PartName":data[i][2],"CheckCycleCount":data[i][3]\
        #                         ,"UsedTimes":data[i][4],"CheckCycle":data[i][5],"NextCheckDate":data[i][6],"Maintainer":data[i][7]\
        #                         ,"Status":status})
        return restful.ok(data=data_arr)
    else:
        return restful.method_error(message='method error',data='error')
# 设备列表数据
@csrf_exempt
def webapp_PartItem(request):
    if request.method == "GET":
        try:
            data_arr = []
            # count_max_value = int(list(Configuration.objects.filter(Type="mt_count").values("Max"))[0]['Max'])
            # day_max_value = int(list(Configuration.objects.filter(Type="mt_date").values("Max"))[0]['Max'])
            # count_max_value = int(count_count[0]['Max'])
            # day_max_value = int(date[0]['Max'])
            start_select = (list(PartItem.objects.order_by("-TrnDate").filter(TrnDate__lte=datetime.now()).values("TrnDate")))[0]['TrnDate']
            end = start_select - timedelta(days=7)
            try:
                cur = connection.cursor()
                sql = 'select "Id","SN","PN","CheckCycleCount","UsedTimes","CheckCycle","NextCheckDate","NextCheckCount","PartName","WarningBeforeDays","WarningBeforeTimes","Maintainer" FROM "PartItem" WHERE "UseStatus"=\'normal\''
                #     'SELECT "Id","SN","PN","CheckCycleCount","UsedTimes","CheckCycle","NextCheckDate","NextCheckCount","PartName","WarningBeforeDays","WarningBeforeTimes" FROM "PartItem" where "UseStatus"=\'normal\' '
                sql = sql +' AND to_char("TrnDate",\'yyyy-MM-dd HH24:MI:SS\') >=\' '+ end.strftime("%Y-%m-%d %H:%M:%S")+'\' order by "Id" limit '+str(100)+' offset ' + str(0)
                cur.execute(sql)
                data = cur.fetchall()
            except:
                msg_err = "error: get DB PartItem data fail "
                data_dict = {"data": msg_err}
                return JsonResponse(data_dict, safe=False, json_dumps_params={'ensure_ascii': False})

            data1=tidy(data)
            for i in range(len(data1)):
                data_arr.append({"Id": data[i][0], "SN": data[i][1], "PN": data[i][2], "PartName": data[i][8],"CheckCycleCount": data[i][4], "UsedTimes": data[i][4], "CheckCycle": data[i][5], "NextCheckDate": data[i][6],
                                 "Maintainer": data[i][11], "Status": data[i][-1]})
                # status = ""
                # day_result = 0
                # count_result= 0
                # if data[i][6] != None:
                #     day_result = (datetime.strptime(str(data[i][6]), "%Y-%m-%d") - datetime.strptime(str(datetime.now()).split(' ')[0], "%Y-%m-%d")).days
                # if data[i][8] != 0:
                #     count_result = int(data[i][8]) - int(data[i][4])
                # #计算状态的算法
                # if data[i][6] == None and data[i][8] == 0:
                #     status = 'none'
                # if data[i][6] != None and data[i][8] == 0:
                #     if day_result < 0:
                #         status = "OVERPROOF"
                #     if 0<=day_result <= (day_max_value * data[i][5]):
                #         status = "WARNING"
                #     if day_result >(day_max_value * data[i][5]):
                #         status = "NORMAL"
                # if data[i][6] == None and data[i][8] != 0:
                #     # count_result = int(data[i][8]) - int(data[i][4])
                #     if count_result <0:
                #         status = "OVERPROOF"
                #     if 0<=count_result<=(count_max_value * data[i][3]):
                #         status = "WARNING"
                #     if count_result >(count_max_value * data[i][3]):
                #         status = "NORMAL"
                # if data[i][6] != None and data[i][8] != 0:
                #     if count_result <0 or day_result <0:
                #         status ="OVERPROOF"
                #     else:
                #         if count_result >(count_max_value * data[i][3]) and day_result >(day_max_value * data[i][5]):
                #             status = "NORMAL"
                #         else:
                #             status = "WARNING"


            return restful.ok(data=data_arr)
        except Exception as e:
            return restful.params_error(message=repr(e))




#保养设备列表 还未实现功能
#sql = 'select "Id","SN","PartName","CheckCycleCount","UsedTimes","CheckCycle",to_char("NextCheckDate",\'yyyy-MM-dd\'),"Maintainer","NextCheckCount","TrnDate","PN" FROM "PartItem" WHERE 1=1'
@csrf_exempt
def webapp_MaintainList(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            maintain_operator = data.get('maintain_operator')
            operator= User.objects.get(EmployeeId=maintain_operator).Name
            count_count = Configuration.objects.get(Type="mt_count")
            date = Configuration.objects.get(Type="mt_date")
            count_max_value = int(count_count.Max)
            day_max_value = int(date.Max)
            cur = connection.cursor()
            sql = 'select "Id","SN","PN","CheckCycleCount","UsedTimes","CheckCycle",to_char("NextCheckDate",\'yyyy-MM-dd\'),"NextCheckCount","PartName","WarningBeforeDays","WarningBeforeTimes","Maintainer" FROM "PartItem" WHERE "UseStatus"=\'normal\''
            #     'SELECT "Id","SN","PN","CheckCycleCount","UsedTimes","CheckCycle","NextCheckDate","NextCheckCount","PartName","WarningBeforeDays","WarningBeforeTimes" FROM "PartItem" where "UseStatus"=\'normal\' '
            # sql = sql + ' AND to_char("TrnDate",\'yyyy-MM-dd HH24:MI:SS\') >=\' ' + end.strftime("%Y-%m-%d %H:%M:%S") + '\' order by "Id" limit ' + str(100) + ' offset ' + str(0)
            # sql = 'select "Id","SN","PartName","CheckCycleCount","UsedTimes","CheckCycle",to_char("NextCheckDate",\'yyyy-MM-dd\'),"Maintainer","NextCheckCount","TrnDate","PN" FROM "PartItem" WHERE "UseStatus"=\'normal\''
            sql = sql +' AND "Maintainer" =\'' + operator + '\'' +' order by "Id"'
            cur.execute(sql)
            data = cur.fetchall()
            data_arr = []
            data1 = tidy(data)
            for i in range(len(data1)):
                data_arr.append({"Id": data[i][0], "SN": data[i][1], "PN": data[i][2], "PartName": data[i][8],
                                 "CheckCycleCount": data[i][4], "UsedTimes": data[i][4], "CheckCycle": data[i][5],
                                 "NextCheckDate": data[i][6],
                                 "Maintainer": data[i][11], "Status": data[i][-1]})
            # for i in range(len(data)):
            #     status = ""
            #     day_result = 0
            #     count_result = 0
            #     if data[i][6] != None:
            #         day_result = (datetime.strptime(str(data[i][6]).split(' ')[0], "%Y-%m-%d") - datetime.strptime(
            #             str(datetime.now()).split(' ')[0], "%Y-%m-%d")).days
            #     if data[i][8] != 0:
            #         count_result = int(data[i][8]) - int(data[i][4])
            #     # 计算状态的算法
            #     if data[i][6] == None and data[i][8] == 0:
            #         # data.remove(data[i])
            #         status = 'none'
            #     if data[i][6] != None and data[i][8] == 0:
            #         if day_result < 0:
            #             status = "OVERPROOF"
            #         if 0 <= day_result <= (day_max_value * data[i][5]):
            #             status = "WARNING"
            #         if day_result > (day_max_value * data[i][5]):
            #             # data.remove(data[i])
            #             status = "NORMAL"
            #     if data[i][6] == None and data[i][8] != 0:
            #         # count_result = int(data[i][8]) - int(data[i][4])
            #         if count_result < 0:
            #             status = "OVERPROOF"
            #         if 0 <= count_result <= (count_max_value * data[i][3]):
            #             status = "WARNING"
            #         if count_result > (count_max_value * data[i][3]):
            #             # data.remove(data[i])
            #             status = "NORMAL"
            #     if data[i][6] != None and data[i][8] != 0:
            #         if count_result < 0 or day_result < 0:
            #             status = "OVERPROOF"
            #         else:
            #             if count_result > (count_max_value * data[i][3]) and day_result > (day_max_value * data[i][5]):
            #                 # data.remove(data[i])
            #                 status = "NORMAL"
            #             else:
            #                 status = "WARNING"
            #     data_arr.append({"Id": data[i][0], "SN": data[i][1], "PN": data[i][10], "PartName": data[i][2],
            #                      "CheckCycleCount": data[i][3], "UsedTimes": data[i][4], "CheckCycle": data[i][5], "NextCheckDate": data[i][6],
            #                      "Maintainer": data[i][7], "Status": status})
            #     for i in range(len(data_arr)):
            #         if data_arr[i]["Status"] == "NORMAL" or data_arr[i]["Status"] == "none":
            #             data_arr.remove(data_arr[i])
            return restful.ok(data=data_arr)
            # maintain_list = list(PartItem.objects.filter(Maintainer=operator).values("Id","SN","PartName","CheckCycleCount","UsedTimes","CheckCycle","NextCheckDate","Maintainer","NextCheckCount","TrnDate","PN"))
            #清洗数据的显示部分
            # return restful.ok(data=maintain_list)
        except:
            return restful.params_error(message="error")
    else:
        return restful.params_error(message='ways error')
#设备保养筛选
@csrf_exempt
def webapp_Filtrate(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            input_sn = data.get('sn')
            input_pn = data.get('pn')
            input_date = data.get('date')
            input_status = data.get('status')
        except:
            return restful.params_error(message='get data error',data='error')
        #获取数据
        count_count = Configuration.objects.get(Type="mt_count")
        date = Configuration.objects.get(Type="mt_date")
        count_max_value = int(count_count.Max)
        day_max_value = int(date.Max)
        try:
            cur = connection.cursor()
            # sql = 'select "Id","SN","PartName","CheckCycleCount","UsedTimes","CheckCycle","NextCheckDate","Maintainer","NextCheckCount" FROM "PartItem" WHERE 1=1'
            # sql = 'select "Id","SN","PartName","CheckCycleCount","UsedTimes","CheckCycle",to_char("NextCheckDate",\'yyyy-MM-dd\'),"Maintainer","NextCheckCount","TrnDate","PN" FROM "PartItem" WHERE 1=1'
            sql = 'select "Id","SN","PN","CheckCycleCount","UsedTimes","CheckCycle",to_char("NextCheckDate",\'yyyy-MM-dd\'),"NextCheckCount","PartName","WarningBeforeDays","WarningBeforeTimes","Maintainer" FROM "PartItem" WHERE "UseStatus"=\'normal\''

            if input_status != "":
                sql =sql_select(sql,input_status,count_max_value,day_max_value)
            if input_sn != "":
                sql = sql+' AND "SN" =\'' + input_sn + '\''
            if input_pn != "":
                sql = sql+' AND "PN" =\'' + input_pn + '\''
            if input_date != "":
                max_next_time=datetime(int(input_date[0:4]),int(input_date[5:7]),int(input_date[8:10]),23,59,59)
                sql = sql+' AND "NextCheckDate"<= \'%{0}%\''.format(max_next_time)
            cur.execute(sql)
            data = cur.fetchall()
        except:
            msg_err = "error: connect DB fail "
            return restful.params_error(message=msg_err,data='error')
        data_arr = []
        data1 = tidy(data)
        for i in range(len(data1)):
            data_arr.append({"Id": data[i][0], "SN": data[i][1], "PN": data[i][2], "PartName": data[i][8],
                             "CheckCycleCount": data[i][4], "UsedTimes": data[i][4], "CheckCycle": data[i][5],
                             "NextCheckDate": data[i][6],
                             "Maintainer": data[i][11], "Status": data[i][-1]})
        # for i in range(len(data)):
        #     status = ""
        #     day_result = 0
        #     count_result = 0
        #     if data[i][6] != None:
        #         day_result = (datetime.strptime(str(data[i][6]).split(' ')[0], "%Y-%m-%d") - datetime.strptime(
        #             str(datetime.now()).split(' ')[0], "%Y-%m-%d")).days
        #     if data[i][8] != 0:
        #         count_result = int(data[i][8]) - int(data[i][4])
        #     # 计算状态的算法
        #     if data[i][6] == None and data[i][8] == 0:
        #         status = 'none'
        #     if data[i][6] != None and data[i][8] == 0:
        #         if day_result < 0:
        #             status = "OVERPROOF"
        #         if 0 <= day_result <= (day_max_value * data[i][5]):
        #             status = "WARNING"
        #         if day_result > (day_max_value * data[i][5]):
        #             status = "NORMAL"
        #     if data[i][6] == None and data[i][8] != 0:
        #         # count_result = int(data[i][8]) - int(data[i][4])
        #         if count_result < 0:
        #             status = "OVERPROOF"
        #         if 0 <= count_result <= (count_max_value * data[i][3]):
        #             status = "WARNING"
        #         if count_result > (count_max_value * data[i][3]):
        #             status = "NORMAL"
        #     if data[i][6] != None and data[i][8] != 0:
        #         if count_result < 0 or day_result < 0:
        #             status = "OVERPROOF"
        #         else:
        #             if count_result > (count_max_value * data[i][3]) and day_result > (day_max_value * data[i][5]):
        #                 status = "NORMAL"
        #             else:
        #                 status = "WARNING"
        #     data_arr.append({"Id": data[i][0], "SN": data[i][1], "PN": data[i][10], "PartName": data[i][2],
        #                      "CheckCycleCount": data[i][3], "UsedTimes": data[i][4], "CheckCycle": data[i][5],
        #                      "NextCheckDate": data[i][6],
        #                      "Maintainer": data[i][7], "Status": status})
        return restful.ok(data=data_arr)
    else:
        return restful.method_error(message='method error',data='error')

#用户做保养设置的提交动作的视图函数
@csrf_exempt
def webapp_MaintainCommit(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            maintain_sns = data.get('select_sn')
            maintain_date = data.get('maintian_date')
            maintain_operator = data.get('maintainer')
            maintain_status = data.get('status')
            maintain_text = data.get('content')
            maintain_remark = data.get('remark')
            #写入保养计入原有的数据到记录表
            try:
                operator = User.objects.get(Name=maintain_operator)
            except:
                return restful.params_error(message="maintainer not exist")
            op_id =operator.Id
            maintain_sns = maintain_sns[1:-1]
            maintain_sns_arr = maintain_sns.split(',')
            j=0
            for j in range(len(maintain_sns_arr)):
                maintain_log = PartItem.objects.get(SN=maintain_sns_arr[j][1:-1])
                MaintenanceLog.objects.create(PartItemId=maintain_log.Id,PartName=maintain_log.PartName,UpdatedTime=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                             ,Status=maintain_status,Content=maintain_text,OperatorId=op_id
                                             ,CheckDueDate=maintain_log.NextCheckDate,CheckCount=maintain_log.NextCheckCount
                                             ,UsedTimes=maintain_log.UsedTimes,Remark=maintain_remark,MaintenanceDate=maintain_date)
                maintain_obj = PartItem.objects.get(SN=maintain_sns_arr[j][1:-1])
                if maintain_obj.CheckCycleCount != None or maintain_obj.UsedTimes !=None:
                    maintain_obj.NextCheckCount = maintain_obj.CheckCycleCount+maintain_obj.UsedTimes
                    maintain_obj.save()
                if maintain_obj.CheckCycle != None:
                    # start_time = datetime.now()
                    user_time = datetime.strptime(str(maintain_date).split(' ')[0], "%Y-%m-%d")
                    delta = timedelta(days=maintain_obj.CheckCycle)
                    maintain_obj.NextCheckDate = user_time+delta
                    maintain_obj.save()
            return restful.ok(data="ok",message="maintain ok")
        except Exception as e:
            return restful.params_error(data='error',message=repr(e))
    else:
        return restful.params_error(data='error',message='method error')





# 设备保养记录筛选和数据获取是同一个的函数的使用
@csrf_exempt
def webapp_MaintainFiltrate(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            input_start_time = data.get('start_time')
            input_end_time = data.get('end_time')
            input_sn = data.get('sn')
            input_pn = data.get('pn')
            input_part_name = data.get('part_name')
            input_operator = data.get('operator')
        except:
            return restful.params_error(message="get data error", data='error')
        try:
            cur = connection.cursor()
            sql = 'select "PartItem"."SN","PartItem"."PN","PartItem"."Spec","Status","User"."Name","Content",to_char("MaintenanceDate",\'yyyy-MM-dd\')' \
                              ',"PartItemId","OperatorId","Remark" from "PartItem" right join "MaintenanceLog"  on ("PartItem"."Id" = "MaintenanceLog"."PartItemId") left join "User" on ("MaintenanceLog"."OperatorId" = "User"."Id") where 1=1'
            if input_start_time !="":
                start_time = datetime(int(input_start_time[0:4]), int(input_start_time[5:7]), int(input_start_time[8:10]),00, 00, 00)
                sql = sql + ' AND "MaintenanceLog"."MaintenanceDate" >=\'%{0}%\''.format(start_time)
            if input_end_time != "":
                end_time = datetime(int(input_end_time[0:4]), int(input_end_time[5:7]), int(input_end_time[8:10]), 23, 59,59)
                sql = sql + ' AND "MaintenanceLog"."MaintenanceDate" <=\'%{0}%\''.format(end_time)
            if input_sn != "":
                sql = sql + ' AND "PartItem"."SN" =\'' + input_sn + '\''
            if input_pn != "":
                sql = sql + ' AND "PartItem"."PN" ilike \'%' + input_pn + '%\''
            if input_part_name != "":
                sql = sql + ' AND "PartItem"."Spec" ilike \'%' + input_part_name + '%\''
            if input_operator !="":
                sql = sql +' AND "User"."Name" ilike\'%'+input_operator+'%\''
            #如果筛选为空的话，这里默认是选择前面100 items
            if input_start_time =="" and input_end_time==""and input_sn==""and input_pn==""and input_part_name==""and input_operator=="":
                sql = sql + ' order by "PartItemId" limit ' + str(100) + ' offset ' + str(0)
            cur.execute(sql)
            data = cur.fetchall()
        except:
            msg=traceback.format_exc()
            log_text.critical(msg)
            return restful.params_error(message=msg, data='error')
        data_arr = []
        for i in range(0,len(data)):
        # for i in range(len(data)):
        #     try:
        #         partitem_id = data[i][0]
        #         sn = data[i][1]
        #         pn = data[i][2]
        #         spec = data[i][4]
        #     except:
        #         continue
        #     if input_operator != "":
        #         try:
        #             input_operator_id = User.objects.get(Name=input_operator).Id
        #         except:
        #             return restful.params_error(message="operator is invalid", data='error')
        #         try:
        #             sql = 'select "Status","Content","MaintenanceDate","OperatorId" FROM "MaintenanceLog" WHERE "PartItemId"= %d AND "OperatorId" = %d' % (
        #             partitem_id, input_operator_id)
        #             # 判断是否在选定的时间范围内
        #             if input_start_time != "" and input_end_time != "":
        #                 start_time = datetime(int(input_start_time[0:4]), int(input_start_time[5:7]),int(input_start_time[8:10]), 00, 00, 00)
        #                 end_time = datetime(int(input_end_time[0:4]), int(input_end_time[5:7]),int(input_end_time[8:10]), 23, 59, 59)
        #                 sql = sql + ' AND "MaintenanceDate">= \'%{0}%\' AND "MaintenanceDate"<= \'%{1}%\''.format(
        #                     start_time, end_time)
        #             elif input_start_time != "" and input_end_time == "":
        #                 start_time = datetime(int(input_start_time[0:4]), int(input_start_time[5:7]),
        #                                       int(input_start_time[8:10]))
        #                 sql = sql + ' AND "MaintenanceDate">= \'%{0}%\''.format(start_time)
        #             elif input_start_time == "" and input_end_time != "":
        #                 end_time = datetime(int(input_end_time[0:4]), int(input_end_time[5:7]),
        #                                     int(input_end_time[8:10]), 23, 59, 59)
        #                 sql = sql + ' AND "MaintenanceDate"<= \'%{0}%\''.format(end_time)
        #             cur.execute(sql)
        #             data3 = cur.fetchall()
        #         except:
        #             continue
        #         for j in range(len(data3)):
        #             try:
        #                 operator = User.objects.get(Id=int(data3[j][3])).Name
        #                 status = data3[j][0]
        #                 content = data3[j][1]
        #                 date = data3[j][2]
        #                 date = str(date)
        #                 date = date[0:10]
        #             except:
        #                 continue
        #             data_dict_1 = {"Id": partitem_id, "SN": sn, "PN": pn, "Spec": spec, "Status": status,
        #                            "Operator": operator, "Content": content, "MaintenanceDate": date}
        #             if len(data_dict_1) != 0:
        #                 data_arr.append(data_dict_1)
        #     else:
        #         try:
        #             sql = 'select "Status","Content","MaintenanceDate","OperatorId" FROM "MaintenanceLog" WHERE "PartItemId" = %d ' % partitem_id
        #             # 判断是否在选定的时间范围内
        #             if input_start_time != "" and input_end_time != "":
        #                 start_time = datetime(int(input_start_time[0:4]), int(input_start_time[5:7]),
        #                                       int(input_start_time[8:10]), 00, 00, 00)
        #                 end_time = datetime(int(input_end_time[0:4]), int(input_end_time[5:7]),
        #                                     int(input_end_time[8:10]), 23, 59, 59)
        #                 sql = sql + ' AND "MaintenanceDate">= \'%{0}%\' AND "MaintenanceDate"<= \'%{1}%\''.format(
        #                     start_time, end_time)
        #             elif input_start_time != "" and input_end_time == "":
        #                 start_time = datetime(int(input_start_time[0:4]), int(input_start_time[5:7]),
        #                                       int(input_start_time[8:10]))
        #                 sql = sql + ' AND "MaintenanceDate">= \'%{0}%\''.format(start_time)
        #             elif input_start_time == "" and input_end_time != "":
        #                 end_time = datetime(int(input_end_time[0:4]), int(input_end_time[5:7]),
        #                                     int(input_end_time[8:10]), 23, 59, 59)
        #                 sql = sql + ' AND "MaintenanceDate"<= \'%{0}%\''.format(end_time)
        #             cur.execute(sql)
        #             data3 = cur.fetchall()
        #         except:
        #             continue
        #         for j in range(len(data3)):
        #             try:
        #                 operator = User.objects.get(Id=int(data3[j][3])).Name
        #                 status = data3[j][0]
        #                 content = data3[j][1]
        #                 date = data3[j][2]
        #                 date = str(date)
        #                 date = date[0:10]
        #             except:
        #                 continue
            data_dict_1 = {"Id":data[i][7],"SN": data[i][0], "PN": data[i][1], "Spec": data[i][2], "Status": data[i][3],
                           "Operator": data[i][4], "Content": data[i][5], "MaintenanceDate": data[i][6]}
            data_arr.append(data_dict_1)
        return restful.ok(data=data_arr)
    else:
        return restful.method_error(message='method error', data='error')



##查询函数的sql语句调用
def sql_select(sql,Status,count,date):
    # 正常的条件设置
    n1 = '("NextCheckDate" IS NOT NULL AND "NextCheckCount" !=0 AND "NextCheckCount"-"UsedTimes">'+str(count)+'*"CheckCycleCount" AND extract(day from("NextCheckDate"-current_date))>'+str(date)+'*"CheckCycle")'
    n2 = '("NextCheckDate" IS NOT NULL AND "NextCheckCount" =0 AND extract(day from("NextCheckDate"-current_date))>'+str(date)+'*"CheckCycle")'
    n3 = '("NextCheckDate" IS NULL AND "NextCheckCount" !=0 AND "NextCheckCount"-"UsedTimes">'+str(count)+'*"CheckCycleCount")'
    # 预警的条件设置
    w1 = '("NextCheckDate" IS NOT NULL AND "NextCheckCount" !=0 AND (("NextCheckCount"-"UsedTimes"<='+str(count)+'*"CheckCycleCount" AND "NextCheckCount"-"UsedTimes">= 0 AND extract(day from("NextCheckDate"-current_date))>=0)'
    w1 = w1+'OR ("NextCheckCount"-"UsedTimes">= 0 AND extract(day from("NextCheckDate"-current_date))>=0 AND extract(day from("NextCheckDate"-current_date))<='+str(date)+'*"CheckCycle")))'
    w2 = '("NextCheckDate" IS NOT NULL AND "NextCheckCount" =0 AND extract(day from("NextCheckDate"-current_date))<='+str(date)+'*"CheckCycle" AND extract(day from("NextCheckDate"-current_date))>=0)'
    w3 = '("NextCheckDate" IS NULL AND "NextCheckCount" !=0 AND "NextCheckCount"-"UsedTimes"<='+str(count)+'*"CheckCycleCount" AND "NextCheckCount"-"UsedTimes">=0)'
    # 超标的条件设置
    c1 ='("NextCheckDate" IS NOT NULL AND "NextCheckCount" !=0 AND ("NextCheckCount"-"UsedTimes"<0 OR extract(day from("NextCheckDate"-current_date))<0))'
    c2 ='("NextCheckDate" IS NOT NULL AND "NextCheckCount" =0 AND extract(day from("NextCheckDate"-current_date))<0)'
    c3 ='("NextCheckDate" IS NULL AND "NextCheckCount" !=0 AND "NextCheckCount"-"UsedTimes"<0)'
    # 未设定的条件设置
    noon = '("NextCheckDate" IS NULL AND "NextCheckCount"=0)'
    if Status == "NORMAL":
        sql = sql + ' AND('+n1+'OR'+n2+'OR'+n3+')'
    if Status == "WARNING":
        sql = sql + ' AND('+w1+'OR'+w2+'OR'+w3+')'
    if Status == "OVERPROOF":
        sql = sql + ' AND('+c1+'OR'+c2+'OR'+c3+')'
    if Status == "未设定":
        sql = sql +' AND('+noon+')'
    return sql


#处理获取的数据进行状态的判断
def tidy(data):
    limit_value1 = list(Configuration.objects.filter(Type="mt_count").values("Max", "Id"))
    limit_value2 = list(Configuration.objects.filter(Type="mt_date").values("Max", "Id"))
    for i in range(len(data)):
        data[i] = list(data[i])
        if data[i][6] == None:
            data[i].append("null")
        else:
            start_time = datetime.strptime(str(datetime.now()).split(' ')[0], "%Y-%m-%d")
            time_end = datetime.strptime(str(data[i][6]).split(' ')[0], "%Y-%m-%d")  # 获取数据表里面的日期数
            days = time_end - start_time
            data[i].append(int(days.days))
        if data[i][7] == 0:
            data[i].append("null")
        else:
            data[i].append(data[i][7] - data[i][4])
        # return data
        if data[i][9] == None and data[i][10] == None:
            if data[i][12] != "null" and data[i][13] != "null":
                if data[i][12]> limit_value2[0]['Max']*data[i][5] and data[i][13]>limit_value1[0]['Max']*data[i][3]:
                    data[i].append('NORMAL')
                if 0<=data[i][12]<= limit_value2[0]['Max']*data[i][5] and 0<=data[i][13]:
                    data[i].append('WARNING')
                if 0<=data[i][13]<= limit_value1[0]['Max']*data[i][3] and 0<=data[i][12]:
                    data[i].append('WARNING')
                if data[i][12]<0 or data[i][13]<0:
                    data[i].append('OVERPROOF')
            if data[i][12] != "null" and data[i][13] == "null":
                if data[i][12] > limit_value2[0]['Max']*data[i][5]:
                    data[i].append('NORMAL')
                if 0 <= data[i][12] <= limit_value2[0]['Max']*data[i][5]:
                    data[i].append('WARNING')
                if data[i][12]<0:
                    data[i].append('OVERPROOF')
            if data[i][12] == "null" and data[i][13] != "null":
                if data[i][13]>limit_value1[0]['Max']*data[i][3]:
                    data[i].append('NORMAL')
                if 0<=data[i][13]<= limit_value1[0]['Max']*data[i][3]:
                    data[i].append('WARNING')
                if data[i][13]<0:
                    data[i].append('OVERPROOF')
            if data[i][12] == "null" and data[i][13] == "null":
                data[i].append('none')
        if data[i][9] == None and data[i][10] != None:
            if data[i][12] != "null" and data[i][13] != "null":
                if data[i][12]> limit_value2[0]['Max']*data[i][5] and data[i][13]>data[i][10]:
                    data[i].append('NORMAL')
                if 0<=data[i][12]<= limit_value2[0]['Max']*data[i][5] and 0<=data[i][13]:
                    data[i].append('WARNING')
                if 0<=data[i][13]<= data[i][10] and 0<=data[i][12]:
                    data[i].append('WARNING')
                if data[i][12]<0 or data[i][13]<0:
                    data[i].append('OVERPROOF')
            if data[i][12] != "null" and data[i][13] == "null":
                if data[i][12] > limit_value2[0]['Max']*data[i][5]:
                    data[i].append('NORMAL')
                if 0 <= data[i][12] <= limit_value2[0]['Max']*data[i][5]:
                    data[i].append('WARNING')
                if data[i][12]<0:
                    data[i].append('OVERPROOF')
            if data[i][12] == "null" and data[i][13] != "null":
                if data[i][13]>data[i][9]:
                    data[i].append('NORMAL')
                if 0<=data[i][13]<= data[i][9]:
                    data[i].append('WARNING')
                if data[i][13]<0:
                    data[i].append('OVERPROOF')
            if data[i][12] == "null" and data[i][13] == "null":
                data[i].append('none')
        if data[i][9] != None and data[i][10] == None:
            if data[i][12] != "null" and data[i][13] != "null":
                if data[i][12]> data[i][9] and data[i][13]>limit_value1[0]['Max']*data[i][3]:
                    data[i].append('normal')
                if 0<=data[i][12]<= data[i][9] and 0<=data[i][13]:
                    data[i].append('warning')
                if 0<=data[i][13]<= limit_value1[0]['Max']*data[i][3] and 0<=data[i][12]:
                    data[i].append('warning')
                if data[i][12]<0 or data[i][13]<0:
                    data[i].append('danger')
            if data[i][12] != "null" and data[i][13] == "null":
                if data[i][12] > data[i][9]:
                    data[i].append('NORMAL')
                if 0 <= data[i][12] <= data[i][9]:
                    data[i].append('WARNING')
                if data[i][12]<0:
                    data[i].append('OVERPROOF')
            if data[i][12] == "null" and data[i][13] != "null":
                if data[i][13]>limit_value1[0]['Max']*data[i][3]:
                    data[i].append('NORMAL')
                if 0<=data[i][13]<= limit_value1[0]['Max']*data[i][3]:
                    data[i].append('WARNING')
                if data[i][13]<0:
                    data[i].append('OVERPROOF')
            if data[i][12] == "null" and data[i][13] == "null":
                data[i].append('none')
        if data[i][9] != None and data[i][10] != None:
            if data[i][12] != "null" and data[i][13] != "null":
                if data[i][12]> data[i][9] and data[i][13]>data[i][10]:
                    data[i].append('NORMAL')
                if 0<=data[i][12]<= data[i][9] and 0<=data[i][13]:
                    data[i].append('WARNING')
                if 0<=data[i][13]<= data[i][10] and 0<=data[i][12]:
                    data[i].append('WARNING')
                if data[i][12]<0 or data[i][13]<0:
                    data[i].append('OVERPROOF')
            if data[i][12] != "null" and data[i][13] == "null":
                if data[i][12] > data[i][9]:
                    data[i].append('NORMAL')
                if 0 <= data[i][12] <= data[i][9]:
                    data[i].append('WARNING')
                if data[i][12]<0:
                    data[i].append('OVERPROOF')
            if data[i][12] == "null" and data[i][13] != "null":
                if data[i][13]>data[i][10]:
                    data[i].append('NORMAL')
                if 0<=data[i][13]<= data[i][10]:
                    data[i].append('WARNING')
                if data[i][13]<0:
                    data[i].append('OVERPROOF')
            if data[i][12] == "null" and data[i][13] == "null":
                data[i].append('none')
    return data