from django.db import connection
# from app import restful
# from app.login.models import User
from openpyxl import load_workbook,Workbook
from datetime import datetime,timedelta
import time
import os

# import psycopg2
# conn = psycopg2.connect(
#                 database="aemslite",
#                 host="127.0.0.1",
#                 user="postgres",
#                 password = "1234qwer!@#$QWER",
#                 port = 5432,)
# cur=conn.cursor()
# # def runquery(sql):
# #     cursor = conn.cursor()
# #     cursor.execute(sql,None)
# #     col_names = [desc[0] for desc in cursor.description]
# #     # print(col_names)
# #     row=cursor.fetchone()
# #     row = dict(zip(col_names, row))
# #     print(row)
# # sql = 'SELECT "PartName",COUNT("PartName") FROM "PartItem" where 1=1'
# # 柱状图需要的数据的原生语句
# # tab_sql = 'SELECT "Maintainer",COUNT("PartName") FROM "PartItem" where "TrnDate">=\''+end.strftime("%Y-%m-%d")+'\' and "TrnDate"<=\''+start_select.strftime("%Y-%m-%d") + '\''
# # def sql_select(sql,Status):
# #     # 正常的条件设置
# #     n1 = '("NextCheckDate" IS NOT NULL AND "NextCheckCount" !=0 AND "NextCheckCount"-"UsedTimes">'+str(0.1)+'*"CheckCycleCount" AND extract(day from("NextCheckDate"-current_date))>'+str(0.2)+'*"CheckCycle")'
# #     n2 = '("NextCheckDate" IS NOT NULL AND "NextCheckCount" =0 AND extract(day from("NextCheckDate"-current_date))>'+str(0.2)+'*"CheckCycle")'
# #     n3 = '("NextCheckDate" IS NULL AND "NextCheckCount" !=0 AND "NextCheckCount"-"UsedTimes">'+str(0.1)+'*"CheckCycleCount")'
# #     # 预警的条件设置
# #     w1 = '("NextCheckDate" IS NOT NULL AND "NextCheckCount" !=0 AND (("NextCheckCount"-"UsedTimes"<='+str(0.1)+'*"CheckCycleCount" AND "NextCheckCount"-"UsedTimes">= 0 AND extract(day from("NextCheckDate"-current_date))>=0)'
# #     w1 = w1+'OR ("NextCheckCount"-"UsedTimes">= 0 AND extract(day from("NextCheckDate"-current_date))>=0 AND extract(day from("NextCheckDate"-current_date))<='+str(0.2)+'*"CheckCycle")))'
# #     w2 = '("NextCheckDate" IS NOT NULL AND "NextCheckCount" =0 AND extract(day from("NextCheckDate"-current_date))<='+str(0.2)+'*"CheckCycle" AND extract(day from("NextCheckDate"-current_date))>=0)'
# #     w3 = '("NextCheckDate" IS NULL AND "NextCheckCount" !=0 AND "NextCheckCount"-"UsedTimes"<='+str(0.1)+'*"CheckCycleCount" AND "NextCheckCount"-"UsedTimes">=0)'
# #     # 超标的条件设置
# #     c1 ='("NextCheckDate" IS NOT NULL AND "NextCheckCount" !=0 AND "NextCheckCount"-"UsedTimes"<0 OR extract(day from("NextCheckDate"-current_date))<=0)'
# #     c2 ='("NextCheckDate" IS NOT NULL AND "NextCheckCount" =0 AND extract(day from("NextCheckDate"-current_date))<=0)'
# #     c3 ='("NextCheckDate" IS NULL AND "NextCheckCount" !=0 AND "NextCheckCount"-"UsedTimes"<0)'
# #     # 未设定的条件设置
# #     noon = '("NextCheckDate" IS NULL AND "NextCheckCount"=0)'
# #     if Status == "正常":
# #         sql = sql + ' AND('+n1+'OR'+n2+'OR'+n3+')'
# #     if Status == "预警":
# #         sql = sql + ' AND('+w1+'OR'+w2+'OR'+w3+')'
# #     if Status == "超标":
# #         sql = sql + ' AND('+c1+'OR'+c2+'OR'+c3+')'
# #     if Status == "未设定":
# #         sql = sql +' AND('+noon+')'
# #     return sql
#  # 有保养人的 达到超标的数量和SN
# # M_danger = 'select "Maintainer",count(*),array_agg("SN") from "PartItem" where "Maintainer" IS NOT NULL'
# # M_danger = sql_select(M_danger,"超标")+' GROUP BY "Maintainer"'
# # 没有有保养人的 达到超标的数量和SN
# # N_danger = 'select "Maintainer",count(*),array_agg("SN") from "PartItem" where "Maintainer" IS NULL'
# # N_danger = sql_select(N_danger,"超标")+' GROUP BY "Maintainer"'
#
# # 有保养人的 达到预警的数量和SN
# # M_warning = 'select "Maintainer",count(*),array_agg("SN") FROM "PartItem" where "Maintainer" IS NOT NULL'
# # M_warning = sql_select(M_warning,"预警")+' GROUP BY "Maintainer"'
# # 没有保养人的 达到预警的数量和SN
# # N_warning = 'select "Maintainer",count(*),array_agg("SN") FROM "PartItem" where "Maintainer" IS NULL'
# # N_warning = sql_select(N_warning, "预警") + ' GROUP BY "Maintainer"'
#
# #查询函数的sql语句调用
# # def sql_select(sql,Status,count,date):
# #     # 针对SN的 WarningBeforeDays，WarningBeforeTimes有设定的分析
# #     user_sn_1 = ' ("WarningBeforeDays" IS NOT NULL AND "WarningBeforeTimes" IS NOT NULL) AND '
# #     user_sn_2 = ' ("WarningBeforeDays" IS NOT NULL AND "WarningBeforeTimes" IS NULL) AND '
# #     user_sn_3 = ' ("WarningBeforeDays" IS NULL AND "WarningBeforeTimes" IS NOT NULL) AND '
# #     user_sn_4 = ' ("WarningBeforeDays" IS NULL AND "WarningBeforeTimes" IS NULL) AND '
# #     # 正常的条件设置01
# #     n1 = '('+user_sn_4+'"NextCheckDate" IS NOT NULL AND "NextCheckCount" !=0 AND "NextCheckCount"-"UsedTimes">'+str(count)+'*"CheckCycleCount" AND extract(day from("NextCheckDate"-current_date))>'+str(date)+'*"CheckCycle")'
# #     n2 = '('+user_sn_4+'"NextCheckDate" IS NOT NULL AND "NextCheckCount" =0 AND extract(day from("NextCheckDate"-current_date))>'+str(date)+'*"CheckCycle")'
# #     n3 = '('+user_sn_4+'"NextCheckDate" IS NULL AND "NextCheckCount" !=0 AND "NextCheckCount"-"UsedTimes">'+str(count)+'*"CheckCycleCount")'
# #     # 正常的条件设置02
# #     n11 = '('+user_sn_3+'"NextCheckDate" IS NOT NULL AND "NextCheckCount" !=0 AND "NextCheckCount"-"UsedTimes">"WarningBeforeTimes" AND extract(day from("NextCheckDate"-current_date))>'+str(date)+'*"CheckCycle")'
# #     n21 = '('+user_sn_3+'"NextCheckDate" IS NOT NULL AND "NextCheckCount" =0 AND extract(day from("NextCheckDate"-current_date))>'+str(date)+'*"CheckCycle")'
# #     n31 = '('+user_sn_3+'"NextCheckDate" IS NULL AND "NextCheckCount" !=0 AND "NextCheckCount"-"UsedTimes">"WarningBeforeTimes")'
# #     # 正常的条件设置03
# #     n12 = '('+user_sn_2+'"NextCheckDate" IS NOT NULL AND "NextCheckCount" !=0 AND "NextCheckCount"-"UsedTimes">'+str(count)+'*"CheckCycleCount" AND extract(day from("NextCheckDate"-current_date))>"WarningBeforeDays")'
# #     n22 = '('+user_sn_2+'"NextCheckDate" IS NOT NULL AND "NextCheckCount" =0 AND extract(day from("NextCheckDate"-current_date))>"WarningBeforeDays")'
# #     n32 = '('+user_sn_2+'"NextCheckDate" IS NULL AND "NextCheckCount" !=0 AND "NextCheckCount"-"UsedTimes">'+str(count)+'*"CheckCycleCount")'
# #     # 正常的条件设置04
# #     n13 = '('+user_sn_1+'"NextCheckDate" IS NOT NULL AND "NextCheckCount" !=0 AND "NextCheckCount"-"UsedTimes">"WarningBeforeTimes" AND extract(day from("NextCheckDate"-current_date))>"WarningBeforeDays")'
# #     n23 = '('+user_sn_1+'"NextCheckDate" IS NOT NULL AND "NextCheckCount" =0 AND extract(day from("NextCheckDate"-current_date))>"WarningBeforeDays")'
# #     n33 = '('+user_sn_1+'"NextCheckDate" IS NULL AND "NextCheckCount" !=0 AND "NextCheckCount"-"UsedTimes">"WarningBeforeTimes")'
# #
# #
# #     # 预警的条件设置01
# #     w1 = '('+user_sn_4+'"NextCheckDate" IS NOT NULL AND "NextCheckCount" !=0 AND (("NextCheckCount"-"UsedTimes"<='+str(count)+'*"CheckCycleCount" AND "NextCheckCount"-"UsedTimes">= 0 AND extract(day from("NextCheckDate"-current_date))>=0)'
# #     w1 = w1+'OR ("NextCheckCount"-"UsedTimes">= 0 AND extract(day from("NextCheckDate"-current_date))>=0 AND extract(day from("NextCheckDate"-current_date))<='+str(date)+'*"CheckCycle")))'
# #     w2 = '('+user_sn_4+'"NextCheckDate" IS NOT NULL AND "NextCheckCount" =0 AND extract(day from("NextCheckDate"-current_date))<='+str(date)+'*"CheckCycle" AND extract(day from("NextCheckDate"-current_date))>=0)'
# #     w3 = '('+user_sn_4+'"NextCheckDate" IS NULL AND "NextCheckCount" !=0 AND "NextCheckCount"-"UsedTimes"<='+str(count)+'*"CheckCycleCount" AND "NextCheckCount"-"UsedTimes">=0)'
# #     # 预警的条件设置02
# #     w11 = '('+user_sn_3+'"NextCheckDate" IS NOT NULL AND "NextCheckCount" !=0 AND (("NextCheckCount"-"UsedTimes"<="WarningBeforeTimes" AND "NextCheckCount"-"UsedTimes">=0 AND extract(day from("NextCheckDate"-current_date))>=0)'
# #     w11 = w11 + 'OR ("NextCheckCount"-"UsedTimes">= 0 AND extract(day from("NextCheckDate"-current_date))>=0 AND extract(day from("NextCheckDate"-current_date))<=' + str(date) + '*"CheckCycle")))'
# #     w21 = '('+user_sn_3+'"NextCheckDate" IS NOT NULL AND "NextCheckCount" =0 AND extract(day from("NextCheckDate"-current_date))<=' + str(date) + '*"CheckCycle" AND extract(day from("NextCheckDate"-current_date))>=0)'
# #     w31 = '('+user_sn_3+'"NextCheckDate" IS NULL AND "NextCheckCount" !=0 AND "NextCheckCount"-"UsedTimes"<="WarningBeforeTimes" AND "NextCheckCount"-"UsedTimes">=0)'
# #     # 预警的条件设置03
# #     w12 = '('+user_sn_2+'"NextCheckDate" IS NOT NULL AND "NextCheckCount" !=0 AND (("NextCheckCount"-"UsedTimes"<=' + str(count) + '*"CheckCycleCount" AND "NextCheckCount"-"UsedTimes">= 0 AND extract(day from("NextCheckDate"-current_date))>=0)'
# #     w12 = w12 + 'OR ("NextCheckCount"-"UsedTimes">= 0 AND extract(day from("NextCheckDate"-current_date))>=0 AND extract(day from("NextCheckDate"-current_date))<="WarningBeforeDays")))'
# #     w22 = '('+user_sn_2+'"NextCheckDate" IS NOT NULL AND "NextCheckCount" =0 AND extract(day from("NextCheckDate"-current_date))<="WarningBeforeDays" AND extract(day from("NextCheckDate"-current_date))>=0)'
# #     w32 = '('+user_sn_2+'"NextCheckDate" IS NULL AND "NextCheckCount" !=0 AND "NextCheckCount"-"UsedTimes"<=' + str(count) + '*"CheckCycleCount" AND "NextCheckCount"-"UsedTimes">=0)'
# #     # 预警的条件设置04
# #     w13 = '('+user_sn_1+'"NextCheckDate" IS NOT NULL AND "NextCheckCount" !=0 AND (("NextCheckCount"-"UsedTimes"<="WarningBeforeTimes" AND "NextCheckCount"-"UsedTimes">=0 AND extract(day from("NextCheckDate"-current_date))>=0)'
# #     w13 = w13 + 'OR ("NextCheckCount"-"UsedTimes">=0 AND extract(day from("NextCheckDate"-current_date))>=0 AND extract(day from("NextCheckDate"-current_date))<="WarningBeforeDays")))'
# #     w23 = '('+user_sn_1+'"NextCheckDate" IS NOT NULL AND "NextCheckCount" =0 AND extract(day from("NextCheckDate"-current_date))<="WarningBeforeDays" AND extract(day from("NextCheckDate"-current_date))>=0)'
# #     w33 = '('+user_sn_1+'"NextCheckDate" IS NULL AND "NextCheckCount" !=0 AND "NextCheckCount"-"UsedTimes"<="WarningBeforeTimes" AND "NextCheckCount"-"UsedTimes">=0)'
# #
# #     # 超标的条件设置
# #     c1 ='("NextCheckDate" IS NOT NULL AND "NextCheckCount" !=0 AND ("NextCheckCount"-"UsedTimes"<0 OR extract(day from("NextCheckDate"-current_date))<0))' #下次日期和下次保养次数不为空
# #     c2 ='("NextCheckDate" IS NOT NULL AND "NextCheckCount" =0 AND extract(day from("NextCheckDate"-current_date))<0)'                                      #下次日期不为空
# #     c3 ='("NextCheckDate" IS NULL AND "NextCheckCount" !=0 AND "NextCheckCount"-"UsedTimes"<0)'                                                            #下次保养次数不为空
# #
# #     noon = '("NextCheckDate" IS NULL AND "NextCheckCount"=0)'
# #     if Status == "正常":
# #         sql = sql + ' AND('+n1+'OR'+n2+'OR'+n3+'OR'+n11+'OR'+n21+'OR'+n31+'OR'+n12+'OR'+n22+'OR'+n32+'OR'+n13+'OR'+n23+'OR'+n33+')'
# #     if Status == "预警":
# #         sql = sql + ' AND('+w1+'OR'+w2+'OR'+w3+'OR'+w11+'OR'+w21+'OR'+w31+'OR'+w12+'OR'+w22+'OR'+w32+'OR'+w13+'OR'+w23+'OR'+w33+')'
# #     if Status == "超标":
# #         sql = sql + ' AND('+c1+'OR'+c2+'OR'+c3+')'
# #     if Status == "未设定":
# #         sql = sql +' AND('+noon+')'
# #     return sql
# # M_danger = 'select "Maintainer",count(*),array_agg("SN") from "PartItem" where "Maintainer" IS NOT NULL  and "UseStatus"=\'normal\''
# # M_danger = sql_select(M_danger,"正常",0.4,0.2)+' GROUP BY "Maintainer"'
# # N_danger = 'select "Maintainer",count(*),array_agg("SN") from "PartItem" where "Maintainer" IS NULL  and "UseStatus"=\'normal\''
# # N_danger = sql_select(N_danger,"正常",0.4,0.2)+' GROUP BY "Maintainer"'
# # cur.execute(M_danger)
# # danger = cur.fetchall()
# #
# # cur.execute(N_danger)
# # danger2 = cur.fetchall()
# #
# # cur.execute(M_warning)
# # warning = cur.fetchall()
# #
# # cur.execute(N_warning)
# # warning2 = cur.fetchall()
# # sqldict = 'select "Id" from "PartItem" where "Id" < 100 order by "Id" asc'
# # n="LINE"
# # s='select "Id" from "LocationLog" where "Location" ilike \'%'+n+'%\''
# # sql = 'select "PartItem"."Id","SN","PartName","CheckCycleCount","UsedTimes","CheckCycle","NextCheckDate","Maintainer","TrnDate","NextCheckCount","WarningBeforeDays","WarningBeforeTimes","Location" FROM "PartItem" RIGHT JOIN "LocationLog" ON "PartItem"."LocationId" ="LocationLog"."Id"  WHERE  "UseStatus"=\'normal\' '
# # sql = 'select "Id","SN","PartName","CheckCycleCount","UsedTimes","CheckCycle","NextCheckDate","Maintainer","TrnDate","NextCheckCount","WarningBeforeDays","WarningBeforeTimes","LocationId" FROM "PartItem" WHERE  "UseStatus"=\'normal\' '
# # config = 'select "Type","Max" from "Configuration" where "Type" = \''+'mt_count'+'\' or "Type" = \''+'mt_date'+'\''
# # sql = 'select "SN","Spec","CheckCycleCount","UsedTimes","CheckCycle",to_char("NextCheckDate",\'yyyy-MM-dd\'),"NextCheckCount","Maintainer","WarningBeforeDays","WarningBeforeTimes","LocationId" from "PartItem" where 1=1 '
#
# con = psycopg2.connect(
#                 database="aemslite",
#                 host="127.0.0.1",
#                 user="postgres",
#                 password = "1234qwer!@#$QWER",
#                 port = 5432,)

#捞出捞取数据库所有NG率达到或超过预警区间的USN发邮件提醒给收件人 定时的功能在被使用在DBexcle app。views里面的函数crontab_test使用了
# def Check_monitor_equipment():
#     try:
#         Total = 0
#         Overdue = 0
#         Warning = 0
#         # mt_count = list(Configuration.objects.filter(Type="mt_count").values('Max'))
#         # mt_date  = list(Configuration.objects.filter(Type="mt_date").values('Max'))
#         # count_stand = Configuration.objects.get(Type="mt_count")
#         # 有保养人的 达到超标的数量和SN+ 没有第二保养人的数据
#         M_danger = 'select "Maintainer",count(*),array_agg("SN") from "PartItem" where "Maintainer" IS NOT NULL and "SubMaintainers" IS NULL and "UseStatus"=\'normal\''
#         M_danger = sql_select(M_danger,"超标",0.1,0.4)+' GROUP BY "Maintainer"'
#         # 没有有保养人的 达到超标的数量和SN        + 没有第二保养人的数据
#         N_danger = 'select "Maintainer",count(*),array_agg("SN") from "PartItem" where "Maintainer" IS NULL and "SubMaintainers" IS NULL  and "UseStatus"=\'normal\''
#         N_danger = sql_select(N_danger,"超标",0.1,0.4)+' GROUP BY "Maintainer"'
#
#         # 有保养人的 达到预警的数量和SN + 没有第二保养人的数据
#         M_warning = 'select "Maintainer",count(*),array_agg("SN") FROM "PartItem" where "Maintainer" IS NOT NULL and "SubMaintainers" IS NULL  and "UseStatus"=\'normal\''
#         M_warning = sql_select(M_warning,"预警",0.1,0.4)+' GROUP BY "Maintainer"'
#         # 没有保养人的 达到预警的数量和SN + 没有第二保养人的数据
#         N_warning = 'select "Maintainer",count(*),array_agg("SN") FROM "PartItem" where "Maintainer" IS NULL and "SubMaintainers" IS NULL  and "UseStatus"=\'normal\''
#         N_warning = sql_select(N_warning, "预警",0.1,0.4) + ' GROUP BY "Maintainer"'
#
#         # """ 第二保养人邮件提醒功能的实现 """
#         # 有第二保养人的数据 超标数据
#         SM_danger2 = 'select "SN","Maintainer","SubMaintainers" from "PartItem" where "SubMaintainers" IS NOT NULL and "UseStatus"=\'normal\''
#         SM_danger2 = sql_select(SM_danger2, "超标",0.1,0.4)
#         # 有第二保养人的数据预警数据
#         SM_warning2 = 'select "SN","Maintainer","SubMaintainers" FROM "PartItem" where "SubMaintainers" IS NOT NULL and "UseStatus"=\'normal\''
#         SM_warning2 = sql_select(SM_warning2, "预警",0.1,0.4)
#
#         cur = conn.cursor()
#         cur.execute(M_danger)
#         danger = cur.fetchall()
#         cur.execute(N_danger)
#         danger2 = cur.fetchall()
#         cur.execute(M_warning)
#         warning = cur.fetchall()
#         cur.execute(N_warning)
#         warning2 = cur.fetchall()
#
#         cur = conn.cursor()
#         cur.execute(SM_warning2)
#         SM_warning2=cur.fetchall()
#         cur = conn.cursor()
#         cur.execute(SM_danger2)
#         SM_danger2 = cur.fetchall()
#         #存在第二保养人的数据的邮件发送函数
#         data_mail3 = mail_data_list(SM_danger2,SM_warning2)
#         #有保养人   的超标和预警数据 没有第二保养人的data
#         data_mail = mail_data_fun(danger, warning)
#
#         # 没有保养人 的超标和预警数据 没有第二保养人的data
#         data_mail2 = mail_data_fun(danger2, warning2)
#         #第二保养人的邮件发送
#         data_mail = mail_maintainer_sub(data_mail,data_mail3)
#
#
#         print(data_mail2)
#         # print(data_mail)
#         print("--------------------------------------------------------------")
# #         #有保养人的 超标的和预警的数据的提醒的发送mail给保养人
#         check_email = 'select "Email" FROM "User" where "Name" ilike \'%'
#
#         if len(data_mail) > 0:
#             for i in range(0,len(data_mail)):
#                 email_maintainer = []
#                 user_name = check_email+str(data_mail[i][0]) + '%\''
#                 print(user_name)
#                 cur = conn.cursor()
#                 cur.execute(user_name)
#                 user_data = cur.fetchall()
#                 print(user_data)
#                 # user_mail_data = list(User.objects.filter(Name=data_mail[i][0]).values("Email"))
#                 # email_maintainer.append(str(user_data[0]))
#                 # print(email_maintainer)
# #                 subject = "AEMS Lite System Notification for Equipment Maintenance"
# #                 content = """
# # <pre>
# # Dears,
# #     AEMS Lite system found that there is equipment to be maintained.
# #     Please take it to do maintenance in time...
# #     Total: """ + str(Total) + """
# #     Overdue: """ + str(Overdue) +"""
# #     Warning: """ + str(Warning) +"""
# #
# #
# #     THIS EMAIL WAS SENT BY PTS SERVER AUTOMATICALLY. PLEASE DON'T DIRECTLY REPLY!!!
# #     AEMS Lite System http://10.41.95.89:90/index/
# # </pre>
# # """
# #                 mail.sendmail(email_maintainer, content, subject)
# #         #没有保养人的 超标的和预警的数据的提醒的发送给设定的邮件接收人
# #         time.sleep(5)
# #         if len(data_mail2) >0:
# #             email_1 = []
# #             receiver_list = str((count_stand.Reminders)).split(',')
# #
# #             mail_user_data_info = list(User.objects.filter(Name__in=receiver_list).values("Email"))
# #             for i in range(0,len(mail_user_data_info)):
# #                 email_1.append(mail_user_data_info[i]['Email'])
# #             # for i in range(len(receiver_list)):
# #             # email_1.append(receiver_list[i] + '@wistron.com')
# #             Total = int(data_mail2[0][1]) + int(data_mail2[0][3])
# #             Overdue = data_mail2[0][1]
# #             Warning = data_mail2[0][3]
# #             subject = "AEMS Lite System Notification for Equipment Maintenance"
# #             content = """
# # <pre>
# # Dears,
# #     AEMS Lite system found that there is equipment to be maintained.
# #     Please take it to do maintenance in time...
# #     Total: """+str(Total)+"""
# #     Overdue: """+str(Overdue)+"""
# #     Warning: """+str(Warning)+"""
# #
# #
# #     THIS EMAIL WAS SENT BY PTS SERVER AUTOMATICALLY. PLEASE DON'T DIRECTLY REPLY!!!
# #     AEMS Lite System http://10.41.95.89:90/index/
# # </pre>
# # """
# #             mail.sendmail(email_1, content, subject)
#     except Exception as e:
#         return repr(e)
#邮件接收人数据重组
# def mail_data_fun(danger,warning):
#     mail_list = []
#     mail_data=[]
#     for i in range(0,len(danger)):
#         mail_list.append(danger[i][0])
#     for j in range(0,len(warning)):
#         warning_name = warning[j][0]
#         if warning_name not in mail_list:
#             mail_list.append(warning_name)
#     for k in range(0,len(mail_list)):
#         mail_data.append([mail_list[k],0,[],0,[]])
#     if len(danger) > 0:
#         for a in range(0, len(mail_data)):
#             for b in range(0, len(danger)):
#                 if danger[b][0] == mail_data[a][0]:
#                     mail_data[a][1] = danger[b][1]
#                     mail_data[a][2].extend(danger[b][2])
#     if len(warning)>0:
#         for c in range(0,len(mail_data)):
#             for d in range(0,len(warning)):
#                 if warning[d][0] == mail_data[c][0]:
#                     mail_data[c][3] = warning[d][1]
#                     mail_data[c][4].extend(warning[d][2])
#     return mail_data
#第二保养人存在邮件接收者的数据重组
# def mail_data_list(danger,warning):
#     mingzi = []
#     sns = []
#     data_type = [] #[名字,超标数量,[SN,SN,SN,SN],预警,[SN,SN,SN,] ]
#     for i in range(0, len(danger)):
#         danger[i] = list(danger[i])
#         s = danger[i][2].split(',')
#         danger[i].remove(danger[i][2])
#         danger[i].extend(s)
#     for i in range(0, len(warning)):
#         warning[i] = list(warning[i])
#         s = warning[i][2].split(',')
#         warning[i].remove(warning[i][2])
#         warning[i].extend(s)
#
#     for j in range(0, len(danger)):
#         sns.append(danger[j][0])
#         for k in range(1, len(danger[j])):
#             if danger[j][k] not in mingzi:
#                 mingzi.append(danger[j][k])
#     for j in range(0, len(warning)):
#         if warning[j][0] not in sns:
#             sns.append(warning[j][0])
#         for k in range(1, len(warning[j])):
#             if warning[j][k] not in mingzi:
#                 mingzi.append(warning[j][k])
#
#     for i in range(0, len(mingzi)):
#         if mingzi[i] != None:
#             data_type.append([mingzi[i], 0, [],0,[]])
#
#     for m in range(0, len(danger)):
#         for n in range(0, len(danger[m])):
#             for p in range(0, len(data_type)):
#                 if danger[m][n] == data_type[p][0]:
#                     data_type[p][2].append(danger[m][0])
#     for m in range(0, len(warning)):
#         for n in range(0, len(warning[m])):
#             for p in range(0, len(data_type)):
#                 if warning[m][n] == data_type[p][0]:
#                     data_type[p][4].append(warning[m][0])
#
#     for i in range(0, len(data_type)):
#         data_type[i][1] = len(data_type[i][2])
#         data_type[i][3] = len(data_type[i][4])
#
#     return data_type
#第二保养人和有保养人的数据的整合在一起
# def mail_maintainer_sub(warning,danger):
#     data_list = []
#     ming = []
#     if len(warning) > 0 and len(danger) > 0:
#         for i in range(0, len(warning)):
#             for j in range(0, len(danger)):
#                 if warning[i][0] == danger[j][0]:
#                     dan_sns, war_sns, data = [], [], []
#                     data.append(warning[i][0])
#                     data.append(danger[j][1] + warning[i][1])
#                     dan_sns.extend(danger[j][2])
#                     dan_sns.extend(warning[i][2])
#                     data.append(dan_sns)
#                     data.append(danger[j][3] + warning[i][3])
#                     war_sns.extend(danger[j][4])
#                     war_sns.extend(warning[i][4])
#                     data.append(war_sns)
#                     data_list.append(data)
#         for i in range(0, len(data_list)):
#             ming.append(data_list[i][0])
#         for j in range(0, len(warning)):
#             if warning[j][0] not in ming:
#                 data_list.append(warning[j])
#         for j in range(0, len(danger)):
#             if danger[j][0] not in ming:
#                 data_list.append(danger[j])
#     if len(warning) > 0 and len(danger) == 0:
#         data_list = warning
#     if len(warning) == 0 and len(danger) > 0:
#         data_list = danger
#     #去重：
#     for i in range(0,len(data_list)):
#         data_list[i][2]=list(set(data_list[i][2]))
#         data_list[i][4]=list(set(data_list[i][4]))
#         data_list[i][1]=len(data_list[i][2])
#         data_list[i][3]=len(data_list[i][4])
#
#     return data_list

#第二版
def sql_select(sql,Status,count,date):
    # 针对SN的 WarningBeforeDays，WarningBeforeTimes有设定的分析
    user_sn_1 = ' ("WarningBeforeDays" IS NOT NULL AND "WarningBeforeTimes" IS NOT NULL) AND '
    user_sn_2 = ' ("WarningBeforeDays" IS NOT NULL AND "WarningBeforeTimes" IS NULL) AND '
    user_sn_3 = ' ("WarningBeforeDays" IS NULL AND "WarningBeforeTimes" IS NOT NULL) AND '
    user_sn_4 = ' ("WarningBeforeDays" IS NULL AND "WarningBeforeTimes" IS NULL) AND '
    # 正常的条件设置01
    n1 = '('+user_sn_4+'"NextCheckDate" IS NOT NULL AND "NextCheckCount" !=0 AND "NextCheckCount"-"UsedTimes">'+str(count)+'*"CheckCycleCount" AND extract(day from("NextCheckDate"-current_date))>'+str(date)+'*"CheckCycle")'
    n2 = '('+user_sn_4+'"NextCheckDate" IS NOT NULL AND "NextCheckCount" =0 AND extract(day from("NextCheckDate"-current_date))>'+str(date)+'*"CheckCycle")'
    n3 = '('+user_sn_4+'"NextCheckDate" IS NULL AND "NextCheckCount" !=0 AND "NextCheckCount"-"UsedTimes">'+str(count)+'*"CheckCycleCount")'
    # 正常的条件设置02
    n11 = '('+user_sn_3+'"NextCheckDate" IS NOT NULL AND "NextCheckCount" !=0 AND "NextCheckCount"-"UsedTimes">"WarningBeforeTimes" AND extract(day from("NextCheckDate"-current_date))>'+str(date)+'*"CheckCycle")'
    n21 = '('+user_sn_3+'"NextCheckDate" IS NOT NULL AND "NextCheckCount" =0 AND extract(day from("NextCheckDate"-current_date))>'+str(date)+'*"CheckCycle")'
    n31 = '('+user_sn_3+'"NextCheckDate" IS NULL AND "NextCheckCount" !=0 AND "NextCheckCount"-"UsedTimes">"WarningBeforeTimes")'
    # 正常的条件设置03
    n12 = '('+user_sn_2+'"NextCheckDate" IS NOT NULL AND "NextCheckCount" !=0 AND "NextCheckCount"-"UsedTimes">'+str(count)+'*"CheckCycleCount" AND extract(day from("NextCheckDate"-current_date))>"WarningBeforeDays")'
    n22 = '('+user_sn_2+'"NextCheckDate" IS NOT NULL AND "NextCheckCount" =0 AND extract(day from("NextCheckDate"-current_date))>"WarningBeforeDays")'
    n32 = '('+user_sn_2+'"NextCheckDate" IS NULL AND "NextCheckCount" !=0 AND "NextCheckCount"-"UsedTimes">'+str(count)+'*"CheckCycleCount")'
    # 正常的条件设置04
    n13 = '('+user_sn_1+'"NextCheckDate" IS NOT NULL AND "NextCheckCount" !=0 AND "NextCheckCount"-"UsedTimes">"WarningBeforeTimes" AND extract(day from("NextCheckDate"-current_date))>"WarningBeforeDays")'
    n23 = '('+user_sn_1+'"NextCheckDate" IS NOT NULL AND "NextCheckCount" =0 AND extract(day from("NextCheckDate"-current_date))>"WarningBeforeDays")'
    n33 = '('+user_sn_1+'"NextCheckDate" IS NULL AND "NextCheckCount" !=0 AND "NextCheckCount"-"UsedTimes">"WarningBeforeTimes")'


    # 预警的条件设置01
    w1 = '('+user_sn_4+'"NextCheckDate" IS NOT NULL AND "NextCheckCount" !=0 AND (("NextCheckCount"-"UsedTimes"<='+str(count)+'*"CheckCycleCount" AND "NextCheckCount"-"UsedTimes">= 0 AND extract(day from("NextCheckDate"-current_date))>=0)'
    w1 = w1+'OR ("NextCheckCount"-"UsedTimes">= 0 AND extract(day from("NextCheckDate"-current_date))>=0 AND extract(day from("NextCheckDate"-current_date))<='+str(date)+'*"CheckCycle")))'
    w2 = '('+user_sn_4+'"NextCheckDate" IS NOT NULL AND "NextCheckCount" =0 AND extract(day from("NextCheckDate"-current_date))<='+str(date)+'*"CheckCycle" AND extract(day from("NextCheckDate"-current_date))>=0)'
    w3 = '('+user_sn_4+'"NextCheckDate" IS NULL AND "NextCheckCount" !=0 AND "NextCheckCount"-"UsedTimes"<='+str(count)+'*"CheckCycleCount" AND "NextCheckCount"-"UsedTimes">=0)'
    # 预警的条件设置02
    w11 = '('+user_sn_3+'"NextCheckDate" IS NOT NULL AND "NextCheckCount" !=0 AND (("NextCheckCount"-"UsedTimes"<="WarningBeforeTimes" AND "NextCheckCount"-"UsedTimes">=0 AND extract(day from("NextCheckDate"-current_date))>=0)'
    w11 = w11 + 'OR ("NextCheckCount"-"UsedTimes">= 0 AND extract(day from("NextCheckDate"-current_date))>=0 AND extract(day from("NextCheckDate"-current_date))<=' + str(date) + '*"CheckCycle")))'
    w21 = '('+user_sn_3+'"NextCheckDate" IS NOT NULL AND "NextCheckCount" =0 AND extract(day from("NextCheckDate"-current_date))<=' + str(date) + '*"CheckCycle" AND extract(day from("NextCheckDate"-current_date))>=0)'
    w31 = '('+user_sn_3+'"NextCheckDate" IS NULL AND "NextCheckCount" !=0 AND "NextCheckCount"-"UsedTimes"<="WarningBeforeTimes" AND "NextCheckCount"-"UsedTimes">=0)'
    # 预警的条件设置03
    w12 = '('+user_sn_2+'"NextCheckDate" IS NOT NULL AND "NextCheckCount" !=0 AND (("NextCheckCount"-"UsedTimes"<=' + str(count) + '*"CheckCycleCount" AND "NextCheckCount"-"UsedTimes">= 0 AND extract(day from("NextCheckDate"-current_date))>=0)'
    w12 = w12 + 'OR ("NextCheckCount"-"UsedTimes">= 0 AND extract(day from("NextCheckDate"-current_date))>=0 AND extract(day from("NextCheckDate"-current_date))<="WarningBeforeDays")))'
    w22 = '('+user_sn_2+'"NextCheckDate" IS NOT NULL AND "NextCheckCount" =0 AND extract(day from("NextCheckDate"-current_date))<="WarningBeforeDays" AND extract(day from("NextCheckDate"-current_date))>=0)'
    w32 = '('+user_sn_2+'"NextCheckDate" IS NULL AND "NextCheckCount" !=0 AND "NextCheckCount"-"UsedTimes"<=' + str(count) + '*"CheckCycleCount" AND "NextCheckCount"-"UsedTimes">=0)'
    # 预警的条件设置04
    w13 = '('+user_sn_1+'"NextCheckDate" IS NOT NULL AND "NextCheckCount" !=0 AND (("NextCheckCount"-"UsedTimes"<="WarningBeforeTimes" AND "NextCheckCount"-"UsedTimes">=0 AND extract(day from("NextCheckDate"-current_date))>=0)'
    w13 = w13 + 'OR ("NextCheckCount"-"UsedTimes">=0 AND extract(day from("NextCheckDate"-current_date))>=0 AND extract(day from("NextCheckDate"-current_date))<="WarningBeforeDays")))'
    w23 = '('+user_sn_1+'"NextCheckDate" IS NOT NULL AND "NextCheckCount" =0 AND extract(day from("NextCheckDate"-current_date))<="WarningBeforeDays" AND extract(day from("NextCheckDate"-current_date))>=0)'
    w33 = '('+user_sn_1+'"NextCheckDate" IS NULL AND "NextCheckCount" !=0 AND "NextCheckCount"-"UsedTimes"<="WarningBeforeTimes" AND "NextCheckCount"-"UsedTimes">=0)'

    # 超标的条件设置
    c1 ='("NextCheckDate" IS NOT NULL AND "NextCheckCount" !=0 AND ("NextCheckCount"-"UsedTimes"<0 OR extract(day from("NextCheckDate"-current_date))<0))' #下次日期和下次保养次数不为空
    c2 ='("NextCheckDate" IS NOT NULL AND "NextCheckCount" =0 AND extract(day from("NextCheckDate"-current_date))<0)'                                      #下次日期不为空
    c3 ='("NextCheckDate" IS NULL AND "NextCheckCount" !=0 AND "NextCheckCount"-"UsedTimes"<0)'                                                            #下次保养次数不为空

    noon = '("NextCheckDate" IS NULL AND "NextCheckCount"=0)'
    if Status == "正常":
        sql = sql + ' AND('+n1+'OR'+n2+'OR'+n3+'OR'+n11+'OR'+n21+'OR'+n31+'OR'+n12+'OR'+n22+'OR'+n32+'OR'+n13+'OR'+n23+'OR'+n33+')'
    if Status == "预警":
        sql = sql + ' AND('+w1+'OR'+w2+'OR'+w3+'OR'+w11+'OR'+w21+'OR'+w31+'OR'+w12+'OR'+w22+'OR'+w32+'OR'+w13+'OR'+w23+'OR'+w33+')'
    if Status == "超标":
        sql = sql + ' AND('+c1+'OR'+c2+'OR'+c3+')'
    if Status == "未设定":
        sql = sql +' AND('+noon+')'
    return sql
'''获取列表数据的工具[(),(),(),......],  这里只需要传sql语句就行'''
# def listdata(sqllist):
#     cur = con.cursor()
#     cur.execute(sqllist,None)
#     return cur.fetchall()
'''获取字典数据的工具[{},{},{},......], 这里也是需要传sql语句就行'''
# def dictdata(sqldict):
#     cur = conn.cursor()
#     cur.execute(sqldict, None)
#     desc = cur.description
#     return [dict(zip([col[0] for col in desc], row)) for row in cur.fetchall()]
"""预算表单的查询方式以及方法"""

def check():
    #with open(r'C:\Users\Z15123001\Desktop\log\log\tidy_aemslite.txt','r+w') as foo
    foo= open(r'C:\Users\Z15123001\Desktop\log\log\tidy_aemslite.txt','w+')
    normal= open(r'C:\Users\Z15123001\Desktop\log\log\200.txt','w+')
    error= open(r'C:\Users\Z15123001\Desktop\log\log\500.txt','w+')
    other= open(r'C:\Users\Z15123001\Desktop\log\log\else.txt','w+')
    with open(r'C:\Users\Z15123001\Desktop\log\log\aemslite_uwsgi.txt','r+') as f:
        data=f.readlines()
        # print(data)
        for i in data:
            if "200" in i:
                normal.writelines(i)
            if "500" in i:
                error.writelines(i)
            if "200" not in i and "500" not in i:
                other.writelines(i)

        f.close()
        normal.close()
        error.close()
        other.close()
        print("Done")





import calendar
# "获取当前月的额度以及数据 全部转换成人民币为计算单位"
# def FeeLimit_count(Department, AccountTitle):
#     # get all budget of current month data and calculate moneny
#     # calendar.monthrange(int(now.year),int(now.month))     indicate for this month has how many days ...
#     now = datetime.now()
#     startTime = "%s-10-01 00:00:00" % (now.year)
#     endTime = "%s-10-%s 23:59:59" % (now.year, calendar.monthrange(int(now.year), int(now.month))[1])
#     '''
#         get all Status is Approve data and data info include
#         (类别："PurchaseType",单价："UnitPrice",数量："Quantity",单位："Unit",币种："Currency",部门："Department" )
#     '''
#
#     sqlBudget = ' SELECT "UnitPrice","Quantity","Currency" FROM "BudgetCodeForm" WHERE "Department" = \''+Department +'\' AND "PurchaseType" = \''+AccountTitle+'\''
#     sqlBudget += ' AND "Status" =\'Approve\' AND "CreatedTime" >= \''+startTime+'\' AND "CreatedTime" <= \''+endTime+'\';'
#     data = dictdata(sqlBudget)
#     for i in range(0,len(data)):
#         sqlExchange = ' SELECT "ExchangeRate" FROM "ExchangeRate" WHERE "CurrencyTo"=\'CNY\' AND "CurrencyFrom" = \''+data[i]['Currency']+'\' AND "IsActivated" =\'true\' ORDER BY "UpdatedTime" DESC'
#         rate = dictdata(sqlExchange)
#         if len(rate) !=0:
#             cash = rate[0]['ExchangeRate']*data[i]['UnitPrice']*data[i]['Quantity']
#         else:
#             cash = 1 * data[i]['UnitPrice'] * data[i]['Quantity']
#
#         print(cash)
#     print(dictdata(sqlBudget))


# FeeLimit_count("MZVT00","雜購(非耗材類)")










# b='select "BudgetCodeForm"."Id","Department","Name","Customer","TypeOfMachine","ProductName","Model","UnitPrice","Quantity","ApplyReason","AttachmentPath" from "BudgetCodeForm" right join "User" on "BudgetCodeForm"."OwnerId"="User"."Id" where "BudgetCodeForm"."MergeId" IS NULL'
# c='select "BudgetCodeForm"."Id","Department","Name","Customer","TypeOfMachine","ProductName","Model","UnitPrice","Quantity","ApplyReason","AttachmentPath" from "BudgetCodeForm" right join "User" on "BudgetCodeForm"."OwnerId"="User"."Id" where "BudgetCodeForm"."MergeId" IS NOT NULL group by rollup(("BudgetCodeForm"."MergeId"))'
# c='select "BudgetCodeForm"."MergeId",array_agg("Name"),array_agg("Department"),array_agg("BudgetCodeForm"."Id") from "BudgetCodeForm" right join "User" on "BudgetCodeForm"."OwnerId"="User"."Id" where "BudgetCodeForm"."MergeId" IS NOT NULL  GROUP BY "BudgetCodeForm"."MergeId"'
# c='select "BudgetCodeForm"."MergeId",array_agg("Name") from "BudgetCodeForm" right join "User" on "BudgetCodeForm"."OwnerId"="User"."Id" where "BudgetCodeForm"."MergeId" IS NOT NULL  GROUP BY "BudgetCodeForm"."MergeId"'
# cd='select "BudgetCodeForm"."MergeId",array_agg("Id") from(select requester_id as id,accepter_id as fri from request_accepted union all select accepter_id as id,requester_id as fri from request_accepted )_add group by id'
#"BudgetCodeForm"."Id","Department",,"Customer","TypeOfMachine","ProductName","Model","UnitPrice","Quantity","ApplyReason","AttachmentPath"
# print(dictdata(b))
# print(dictdata(c))
# print(listdata(c))
# Check_monitor_equipment()

# def check():
#     # check_user = 'update "Maintainer","Trnate","" FROM "User" where "Name" ilike \'%'
#     name = "Haojie_Ma"
#     check_user = 'SELECT "Id","Maintainer" FROM "PartItem" where "Maintainer" = \''+name+'\' order by "Id" desc'
#     print(check_user)
#     cur = conn.cursor()
#     cur.execute(check_user)
#     user_data = cur.fetchall()
#     print(user_data)
# check()
#
#
#
# def modify_user():
#
#     select_name = 'Haojie_Ma'
#     # check_user1 = 'SELECT "Id","Maintainer" FROM "PartItem" where "Maintainer" = \'' + select_name + '\' order by "Id" desc'
#     # print(check_user1)
#     # cur = conn.cursor()
#     # cur.execute(check_user1)
#     # user_data = cur.fetchall()
#     # print(user_data)
#     # name = "Juan Li"
#
#
#
#     name2 = 'Steven_X_Xu'
#     check_user = 'UPDATE "PartItem" SET "Maintainer"= \'' + name2 + '\'  WHERE "Maintainer" =  \'' + select_name + '\''
#     print(check_user)
#     cur = conn.cursor()
#     cur.execute(check_user)
#     conn.commit()
#     # user_data = cur.fetchall()
#     # # print(user_data)

# modify_user()

"""给对象和类绑定方法"""
def fu(self):
    print(" I like you very much")
class A:

    def __init__(self,name,age):

        self.__name =name#ordinay you must create set and get ways to get this attribute
        self.age =age
    @staticmethod
    def demo():
        print("I am static ways ,please note")
    def __str__(self):#Java set this name is toString() ways
        return "class func %s   "%self.__class__.__name__
    def __call__(self, *args, **kwargs):
        print("i had used for function ,please note")
    def __run(self):
        print("__run")
a=A("set",18)
a._A__name ="Steven"
"""属性访问拦截器， 在访问实例属性时自动调用 在python中，类的属性和方法都理解为属性，且均可以通过__getattribute(self,*argsm**kwargs)
或者根据判断return所需要的返回值， 如果需要获取某个方法的返回值时，则需要在函数后面加个（）即可， 如果没有加的话吗返回的是函数引用地址， 

"""
class B:
    def __init__(self,name):
        self.name = name
        self.ob = "ob"

    def __getattribute__(self, item):#属性访问拦截器
        if item == 'name':
            return self.name
        else:
            return object.__getattribute__(self,item)
# s = B("steven")
# print(s.name)
# print(s.ob )
# print(s.hek )


from functools import wraps
def singleton(cls):
    instances = {}
    @wraps(cls)
    def getinstance(*args, **kw):
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]
    return getinstance
@singleton
class MyClass(object):
    a = 1
a=MyClass()
b=MyClass()
# print(id(a))
# print(id(b))



# def say_hello(country):#@语法中带参数的函数 相当于重写方法 但是我们需要返回该方法名
def control(func):#相当于定义一个方法去装载chinese的函数名
    def check(name,*args, **kwargs):
        if name == "china":
            print("nihao ", end='')
        if name == "American":
            print("hello", end='')
        return func(name,*args, **kwargs)
    return check
    # return control



@control
def chinese(name):
    print("我来自中国。")


@control
def american(name):
    print("I am from America.")

chinese("china")
american("American")





class object:
    """ The most base type """

    def __delattr__(self, *args, **kwargs):  # real signature unknown
        """ Implement delattr(self, name). """
        pass

    def __dir__(self, *args, **kwargs):  # real signature unknown
        """ Default dir() implementation. """
        pass

    def __eq__(self, *args, **kwargs):  # real signature unknown
        """ Return self==value. """
        pass

    def __format__(self, *args, **kwargs):  # real signature unknown
        """ Default object formatter. """
        pass

    def __getattribute__(self, *args, **kwargs):  # real signature unknown
        """ Return getattr(self, name). """
        pass

    def __ge__(self, *args, **kwargs):  # real signature unknown
        """ Return self>=value. """
        pass

    def __gt__(self, *args, **kwargs):  # real signature unknown
        """ Return self>value. """
        pass

    def __hash__(self, *args, **kwargs):  # real signature unknown
        """ Return hash(self). """
        pass

    def __init_subclass__(self, *args, **kwargs):  # real signature unknown
        """
        This method is called when a class is subclassed.

        The default implementation does nothing. It may be
        overridden to extend subclasses.
        """
        pass

    def __init__(self):  # known special case of object.__init__
        """ Initialize self.  See help(type(self)) for accurate signature. """
        pass

    def __le__(self, *args, **kwargs):  # real signature unknown
        """ Return self<=value. """
        pass

    def __lt__(self, *args, **kwargs):  # real signature unknown
        """ Return self<value. """
        pass

    @staticmethod  # known case of __new__
    def __new__(cls, *more):  # known special case of object.__new__
        """ Create and return a new object.  See help(type) for accurate signature. """
        pass

    def __ne__(self, *args, **kwargs):  # real signature unknown
        """ Return self!=value. """
        pass

    def __reduce_ex__(self, *args, **kwargs):  # real signature unknown
        """ Helper for pickle. """
        pass

    def __reduce__(self, *args, **kwargs):  # real signature unknown
        """ Helper for pickle. """
        pass

    def __repr__(self, *args, **kwargs):  # real signature unknown
        """ Return repr(self). """
        pass

    def __setattr__(self, *args, **kwargs):  # real signature unknown
        """ Implement setattr(self, name, value). """
        pass

    def __sizeof__(self, *args, **kwargs):  # real signature unknown
        """ Size of object in memory, in bytes. """
        pass

    def __str__(self, *args, **kwargs):  # real signature unknown
        """ Return str(self). """
        pass

    @classmethod  # known case
    def __subclasshook__(cls, subclass):  # known special case of object.__subclasshook__
        """
        Abstract classes can override this to customize issubclass().

        This is invoked early on by abc.ABCMeta.__subclasscheck__().
        It should return True, False or NotImplemented.  If it returns
        NotImplemented, the normal algorithm is used.  Otherwise, it
        overrides the normal algorithm (and the outcome is cached).
        """
        pass

    __class__ = None  # (!) forward: type, real value is ''
    __dict__ = {}
    __doc__ = ''
    __module__ = ''
















# A.fu = fu
# a=A()
# a.demo()
# a.fu()
# print(a)
# print(a.__class__.__name__)
# A().__call__()
class Person(object):
    def __init__(self, name, age, taste):
        self.name = name
        self._age = age
        self.__taste = taste

    def showperson(self):
        print(self.name)
        print(self._age)
        print(self.__taste)

    def dowork(self):
        self._work()
        self.__away()


    def _work(self):
        print('my _work')

    def __away(self):
        print('my __away')

class Student(Person):
    def construction(self, name, age, taste):
        self.name = name
        self._age = age
        self.__taste = taste

    def showstudent(self):
        print(self.name)
        print(self._age)
        print(self.__taste)

    @staticmethod
    def testbug():
        _Bug.showbug()

# 模块内可以访问，当from  cur_module import *时，不导入
class _Bug(object):
    @staticmethod
    def showbug():
        print("showbug")

# s1 = Student('jack', 25, 'football')
# s1.showperson()
# print('*'*20)
#
# # 无法访问__taste,导致报错
# # s1.showstudent()
# s1.construction('rose', 30, 'basketball')
# s1.showperson()
# print('*'*20)
#
# s1.showstudent()
# print('*'*20)
#
# Student.testbug()






""" 第二保养人邮件提醒功能的实现 """
# 有第二保养人的数据 超标数据
# M_danger2 = 'select "SN","Maintainer","SubMaintainers" from "PartItem" where "SubMaintainers" IS NOT NULL and "UseStatus"=\'normal\''
# SM_danger2 = sql_select(M_danger2, "超标", 0.4, 0.2)
# 有第二保养人的数据预警数据
# M_warning2 = 'select "SN","Maintainer","SubMaintainers" FROM "PartItem" where "SubMaintainers" IS NOT NULL and "UseStatus"=\'normal\''
# SM_warning2 = sql_select(M_warning2, "预警", 0.4, 0.2)
'''获取数据之后进行数据重组，按人名进行排列组合'''
# warning_data = listdata(SM_warning2)
# danger_data = listdata(SM_danger2)
# def data_list(danger,warning):
#     mingzi = []
#     sns = []
#     data_type = [] #[名字,超标数量,[SN,SN,SN,SN],预警,[SN,SN,SN,] ]
#     for i in range(0, len(danger)):
#         danger[i] = list(danger[i])
#         s = danger[i][2].split(',')
#         danger[i].remove(danger[i][2])
#         danger[i].extend(s)
#     for i in range(0, len(warning)):
#         warning[i] = list(warning[i])
#         s = warning[i][2].split(',')
#         warning[i].remove(warning[i][2])
#         warning[i].extend(s)
#
#     for j in range(0, len(danger)):
#         sns.append(danger[j][0])
#         for k in range(1, len(danger[j])):
#             if danger[j][k] not in mingzi:
#                 mingzi.append(danger[j][k])
#     for j in range(0, len(warning)):
#         if warning[j][0] not in sns:
#             sns.append(warning[j][0])
#         for k in range(1, len(warning[j])):
#             if warning[j][k] not in mingzi:
#                 mingzi.append(warning[j][k])
#
#     for i in range(0, len(mingzi)):
#         if mingzi[i] != None:
#             data_type.append([mingzi[i], 0, [],0,[]])
#
#     for m in range(0, len(danger)):
#         for n in range(0, len(danger[m])):
#             for p in range(0, len(data_type)):
#                 if danger[m][n] == data_type[p][0]:
#                     data_type[p][2].append(danger[m][0])
#     for m in range(0, len(warning)):
#         for n in range(0, len(warning[m])):
#             for p in range(0, len(data_type)):
#                 if warning[m][n] == data_type[p][0]:
#                     data_type[p][4].append(warning[m][0])
#
#     for i in range(0, len(data_type)):
#         data_type[i][1] = len(data_type[i][2])
#         data_type[i][3] = len(data_type[i][4])
#
#     return data_type
# def mail_data_fun(danger,warning):
#     mail_list = []
#     mail_data=[]
#     for i in range(0,len(danger)):
#         mail_list.append(danger[i][0])
#     for j in range(0,len(warning)):
#         warning_name = warning[j][0]
#         if warning_name not in mail_list:
#             mail_list.append(warning_name)
#     for k in range(0,len(mail_list)):
#         mail_data.append([mail_list[k],0,[],0,[]])
#     if len(danger) > 0:
#         for a in range(0, len(mail_data)):
#             for b in range(0, len(danger)):
#                 if danger[b][0] == mail_data[a][0]:
#                     mail_data[a][1] = danger[b][1]
#                     mail_data[a][2].extend(danger[b][2])
#     if len(warning)>0:
#         for c in range(0,len(mail_data)):
#             for d in range(0,len(warning)):
#                 if warning[d][0] == mail_data[c][0]:
#                     mail_data[c][3] = warning[d][1]
#                     mail_data[c][4].extend(warning[d][2])
#     return mail_data
# print(data_list(warning_data))
# print(data_list(danger_data))

# print(mail_data_fun(data_list(SM_danger2),data_list(SM_warning2)))

# def mail_maintainer_sub(warning,danger):
#     data_list = []
#     ming = []
#     if len(warning) > 0 and len(danger) > 0:
#         for i in range(0, len(warning)):
#             for j in range(0, len(danger)):
#                 if warning[i][0] == danger[j][0]:
#                     dan_sns, war_sns, data = [], [], []
#                     data.append(warning[i][0])
#                     data.append(danger[j][1] + warning[i][1])
#                     dan_sns.extend(danger[j][2])
#                     dan_sns.extend(warning[i][2])
#                     data.append(dan_sns)
#                     data.append(danger[j][3] + warning[i][3])
#                     war_sns.extend(danger[j][4])
#                     war_sns.extend(warning[i][4])
#                     data.append(war_sns)
#                     data_list.append(data)
#         for i in range(0, len(data_list)):
#             ming.append(data_list[i][0])
#         for j in range(0, len(warning)):
#             if warning[j][0] not in ming:
#                 data_list.append(warning[j])
#         for j in range(0, len(danger)):
#             if danger[j][0] not in ming:
#                 data_list.append(danger[j])
#     if len(warning) > 0 and len(danger) == 0:
#         data_list = warning
#     if len(warning) == 0 and len(danger) > 0:
#         data_list = danger
#     return data_list





'''获取列表的分组之后枚举出相关的额信息 array_agg()'''
"""array_agg(distinct deptno order by deptno desc)去重加排序"""
# sql_mail= 'select "Maintainer",count(*),array_agg("Id") from "PartItem" where "Maintainer" IS NOT NULL  and "UseStatus"=\'normal\''
# print(dictdata(sql_select(M_danger,"超标",0.5,0.5)+' GROUP BY "Maintainer"'))
# print(listdata(sql_select(M_danger,"超标",0.5,0.5)+' GROUP BY "Maintainer"'))   count(*),array_agg("Id")
# sql_mail2= 'select "Id" from "PartItem" where  "Maintainer" IS NOT NULL  and "UseStatus"=\'normal\' ORDER BY "Id" '
# print(listdata(M_danger))
# print(dictdata(M_danger))
# print(listdata(N_danger))
# print(dictdata(N_danger))

#判断是那种状态
# sql = 'SELECT "Id","SN","PN","CheckCycleCount","UsedTimes","CheckCycle","NextCheckDate","NextCheckCount","PartName","WarningBeforeDays","WarningBeforeTimes" FROM "PartItem" where 1=1 '
# sql = 'select "Id","SN","PartName","CheckCycleCount","UsedTimes","CheckCycle","NextCheckDate","Maintainer","TrnDate","NextCheckCount" FROM "PartItem" WHERE  "UseStatus"=\'normal\' '

# limit_value1 = list(Configuration.objects.filter(Type="mt_count").values("Max", "Id"))
# limit_value2 = list(Configuration.objects.filter(Type="mt_date").values("Max", "Id"))
# limit_value1 = [{'Max':0.4}] #cishu
# limit_value2 = [{'Max':0.2}] #shijian
# Next_maintain_time='2019-10-01'
# sql ='SELECT * FROM(' + sql+') as t1 WHERE "NextCheckDate" <= \''+Next_maintain_time+'\''
# sql = sql_select(sql,"正常",limit_value1[0]['Max'],limit_value2[0]['Max'])
# data=listdata(sql)
# print(data)
# def tidy(data):
#     for i in range(len(data)):
#         data[i] = list(data[i])
#         if data[i][6] == None:
#             data[i].append("null")
#         else:
#             start_time = datetime.strptime(str(datetime.now()).split(' ')[0], "%Y-%m-%d")
#             time_end = datetime.strptime(str(data[i][6]).split(' ')[0], "%Y-%m-%d")  # 获取数据表里面的日期数
#             days = time_end - start_time
#             data[i].append(days.days)
#         if data[i][7] == 0:
#             data[i].append("null")
#         else:
#             data[i].append(data[i][7] - data[i][4])
#
#         if data[i][9] == None and data[i][10] == None:
#             if data[i][11] != "null" and data[i][12] != "null":
#                 if data[i][11]> limit_value2[0]['Max']*data[i][5] and data[i][12]>limit_value1[0]['Max']*data[i][3]:
#                     data[i].append('normal')
#                 if 0<=data[i][11]<= limit_value2[0]['Max']*data[i][5] and 0<=data[i][12]:
#                     data[i].append('warning')
#                 if 0<=data[i][12]<= limit_value1[0]['Max']*data[i][3] and 0<=data[i][11]:
#                     data[i].append('warning')
#                 if data[i][11]<0 or data[i][12]<0:
#                     data[i].append('danger')
#             if data[i][11] != "null" and data[i][12] == "null":
#                 if data[i][11] > limit_value2[0]['Max']*data[i][5]:
#                     data[i].append('normal')
#                 if 0 <= data[i][11] <= limit_value2[0]['Max']*data[i][5]:
#                     data[i].append('warning')
#                 if data[i][11]<0:
#                     data[i].append('danger')
#             if data[i][11] == "null" and data[i][12] != "null":
#                 if data[i][12]>limit_value1[0]['Max']*data[i][3]:
#                     data[i].append('normal')
#                 if 0<=data[i][12]<= limit_value1[0]['Max']*data[i][3]:
#                     data[i].append('warning')
#                 if data[i][12]<0:
#                     data[i].append('danger')
#             if data[i][11] == "null" and data[i][12] == "null":
#                 data[i].append('none')
#         if data[i][9] == None and data[i][10] != None:
#             if data[i][11] != "null" and data[i][12] != "null":
#                 if data[i][11]> limit_value2[0]['Max']*data[i][5] and data[i][12]>data[i][10]:
#                     data[i].append('normal')
#                 if 0<=data[i][11]<= limit_value2[0]['Max']*data[i][5] and 0<=data[i][12]:
#                     data[i].append('warning')
#                 if 0<=data[i][12]<= data[i][10] and 0<=data[i][11]:
#                     data[i].append('warning')
#                 if data[i][11]<0 or data[i][12]<0:
#                     data[i].append('danger')
#             if data[i][11] != "null" and data[i][12] == "null":
#                 if data[i][11] > limit_value2[0]['Max']*data[i][5]:
#                     data[i].append('normal')
#                 if 0 <= data[i][11] <= limit_value2[0]['Max']*data[i][5]:
#                     data[i].append('warning')
#                 if data[i][11]<0:
#                     data[i].append('danger')
#             if data[i][11] == "null" and data[i][12] != "null":
#                 if data[i][12]>data[i][9]:
#                     data[i].append('normal')
#                 if 0<=data[i][12]<= data[i][9]:
#                     data[i].append('warning')
#                 if data[i][12]<0:
#                     data[i].append('danger')
#             if data[i][11] == "null" and data[i][12] == "null":
#                 data[i].append('none')
#         if data[i][9] != None and data[i][10] == None:
#             if data[i][11] != "null" and data[i][12] != "null":
#                 if data[i][11]> data[i][9] and data[i][12]>limit_value1[0]['Max']*data[i][3]:
#                     data[i].append('normal')
#                 if 0<=data[i][11]<= data[i][9] and 0<=data[i][12]:
#                     data[i].append('warning')
#                 if 0<=data[i][12]<= limit_value1[0]['Max']*data[i][3] and 0<=data[i][11]:
#                     data[i].append('warning')
#                 if data[i][11]<0 or data[i][12]<0:
#                     data[i].append('danger')
#             if data[i][11] != "null" and data[i][12] == "null":
#                 if data[i][11] > data[i][9]:
#                     data[i].append('normal')
#                 if 0 <= data[i][11] <= data[i][9]:
#                     data[i].append('warning')
#                 if data[i][11]<0:
#                     data[i].append('danger')
#             if data[i][11] == "null" and data[i][12] != "null":
#                 if data[i][12]>limit_value1[0]['Max']*data[i][3]:
#                     data[i].append('normal')
#                 if 0<=data[i][12]<= limit_value1[0]['Max']*data[i][3]:
#                     data[i].append('warning')
#                 if data[i][12]<0:
#                     data[i].append('danger')
#             if data[i][11] == "null" and data[i][12] == "null":
#                 data[i].append('none')
#         if data[i][9] != None and data[i][10] != None:
#             if data[i][11] != "null" and data[i][12] != "null":
#                 if data[i][11]> data[i][9] and data[i][12]>data[i][10]:
#                     data[i].append('normal')
#                 if 0<=data[i][11]<= data[i][9] and 0<=data[i][12]:
#                     data[i].append('warning')
#                 if 0<=data[i][12]<= data[i][10] and 0<=data[i][11]:
#                     data[i].append('warning')
#                 if data[i][11]<0 or data[i][12]<0:
#                     data[i].append('danger')
#             if data[i][11] != "null" and data[i][12] == "null":
#                 if data[i][11] > data[i][9]:
#                     data[i].append('normal')
#                 if 0 <= data[i][11] <= data[i][9]:
#                     data[i].append('warning')
#                 if data[i][11]<0:
#                     data[i].append('danger')
#             if data[i][11] == "null" and data[i][12] != "null":
#                 if data[i][12]>data[i][10]:
#                     data[i].append('normal')
#                 if 0<=data[i][12]<= data[i][10]:
#                     data[i].append('warning')
#                 if data[i][12]<0:
#                     data[i].append('danger')
#             if data[i][11] == "null" and data[i][12] == "null":
#                 data[i].append('none')
#
#     print(data)
# tidy(data)



# # 超标的条件设置02中情况
    # c11 = '(' + user_sn_3 + '"NextCheckDate" IS NOT NULL AND "NextCheckCount" !=0 AND ("NextCheckCount"-"UsedTimes"<"WarningBeforeTimes" OR extract(day from("NextCheckDate"-current_date))<0))'  # 下次日期和下次保养次数不为空
    # c21 = '(' + user_sn_3 + '"NextCheckDate" IS NOT NULL AND "NextCheckCount" =0 AND extract(day from("NextCheckDate"-current_date))<0)'  # 下次日期不为空
    # c31 = '(' + user_sn_3 + '"NextCheckDate" IS NULL AND "NextCheckCount" !=0 AND "NextCheckCount"-"UsedTimes"<"WarningBeforeTimes")'  # 下次保养次数不为空
    # # 超标的条件设置03中情况
    # c12 = '(' + user_sn_2 + '"NextCheckDate" IS NOT NULL AND "NextCheckCount" !=0 AND ("NextCheckCount"-"UsedTimes"<0 OR extract(day from("NextCheckDate"-current_date))<"WarningBeforeDays"))'  # 下次日期和下次保养次数不为空
    # c22 = '(' + user_sn_2 + '"NextCheckDate" IS NOT NULL AND "NextCheckCount" =0 AND extract(day from("NextCheckDate"-current_date))<"WarningBeforeDays")'  # 下次日期不为空
    # c32 = '(' + user_sn_2 + '"NextCheckDate" IS NULL AND "NextCheckCount" !=0 AND "NextCheckCount"-"UsedTimes"<0)'  # 下次保养次数不为空
    # # 超标的条件设置04中情况
    # c13 = '(' + user_sn_1 + '"NextCheckDate" IS NOT NULL AND "NextCheckCount" !=0 AND ("NextCheckCount"-"UsedTimes"<"WarningBeforeTimes" OR extract(day from("NextCheckDate"-current_date))<"WarningBeforeDays"))'  # 下次日期和下次保养次数不为空
    # c23 = '(' + user_sn_1 + '"NextCheckDate" IS NOT NULL AND "NextCheckCount" =0 AND extract(day from("NextCheckDate"-current_date))<"WarningBeforeDays")'  # 下次日期不为空
    # c33 = '(' + user_sn_1 + '"NextCheckDate" IS NULL AND "NextCheckCount" !=0 AND "NextCheckCount"-"UsedTimes"<"WarningBeforeTimes")'  # 下次保养次数不为空
    # 未设定的条件设置
# def tes():
#     print(danger)
#     print('有保养人的 超标')
#     print(danger2)
#     print('没有保养人的 超标')
#     print(warning)
#     print('有保养人的 预警')
#     print(warning2)
#     print('没有保养人的 预警')
# tes()

# sql = 'select "SN","Spec","CheckCycleCount","UsedTimes","CheckCycle",to_char("NextCheckDate",\'yyyy-MM-dd\'),"NextCheckCount","Maintainer" from "PartItem" where "Id" = \'519\''
# sql2 = 'SELECT "PartName", COUNT("SN") FROM "PartItemResult" where "Result"= \'FAIL\' '+ ' AND "ErrorCode" like \'%' + errorcode + '%\''+' AND "PartName" like \'%' + PartName + '%\''+' GROUP BY "PartName"'
# PN="HDD"
# sql = 'SELECT COUNT("SN"),"PartName" FROM (select distinct "SN","PartName","Result"' \
#                ',"Stage","FixtureId","USN","TrnDate","PN" from "PartItemResult") as foo where "Result"= \'FAIL\''
# sql = sql+ ' AND "PN" ilike \'%' + PN + '%\''+' GROUP BY "PartName"'
# sql = 'select count(*) from "PartItem" where "Maintainer"=\'None\''
# sql = 'update "PartItem" set "Maintainer"=\'Asia_Liu\' where "Maintainer"=\'Asia_liu\''
# n="Null"
# sql_no_nextcheckdate = 'SELECT "Id" FROM "PartItem" where "NextCheckDate" ilike '+n+' order by "Id" '

# sql = 'select "User"."Name","OperatorId","PartItem"."SN","PartItem"."PN","PartItem"."Spec","Status","Content"' \
#               ',to_char("MaintenanceDate",\'yyyy-MM-dd\'),"PartItemId","OperatorId" from "MaintenanceLog" left join "PartItem" on ("PartItem"."Id" = "MaintenanceLog"."PartItemId") ' \
#       'left join "User" on ("MaintenanceLog"."OperatorId" = "User"."Id") where "User"."Name" = \'Vicily Wei\''
# start = datetime.current_date
# delta = timedelta(days=300)
# end = start - delta
# c_date = (start + timedelta(days=20)).strftime("%Y-%m-%d")
# sql = 'select "Id" FROM "PartItem" WHERE to_char("TrnDate",\'yyyy-MM-dd\') >= \'' + end.strftime("%Y-%m-%d") + '\' and  to_char("TrnDate",\'yyyy-MM-dd\') <=\'' + start.strftime("%Y-%m-%d") + '\''
# sql_count = 'select count(*) FROM "PartItem" where to_char("TrnDate",\'yyyy-MM-dd\') >= \'' + end.strftime("%Y-%m-%d") + '\' and to_char("TrnDate",\'yyyy-MM-dd\') <= \'' + start.strftime("%Y-%m-%d") + '\''
# # sql3 = 'select "Id","SN","PartName","CheckCycleCount","UsedTimes","CheckCycle","NextCheckDate","Maintainer","TrnDate","NextCheckCount" FROM "PartItem" WHERE to_char("TrnDate",\'yyyy-MM-dd\') >= \'' + end.strftime(
# #     "%Y-%m-%d") + '\' and  to_char("TrnDate",\'yyyy-MM-dd\') <=\'' + start.strftime("%Y-%m-%d") + '\''
# #
# # sql2 =tab_sql = 'SELECT "Maintainer", COUNT("PartName") FROM "PartItem" where to_char("TrnDate",\'yyyy-MM-dd\') >=\' ' + end.strftime("%Y-%m-%d") + '\' and  to_char("TrnDate",\'yyyy-MM-dd\') <=\'' + start.strftime("%Y-%m-%d") + '\''
# # sql2 = sql2 + ' AND "Maintainer" = \'{0}\''.format("Steven_X_Xu")
# # sql2 = sql2 + 'AND ("NextCheckCount"-"UsedTimes" < 0 OR "NextCheckDate" < \'' + start.strftime("%Y-%m-%d") + '\') GROUP BY "Maintainer"'
#
# sql_count = sql_count + 'AND "PartName" = \'{0}\''.format('test')
# sql = sql + 'AND "PartName" = \'{0}\''.format('test')
# # sql_count = sql_count + ' AND (("NextCheckCount"-"UsedTimes" <= ' + '10' + ' AND "NextCheckCount"-"UsedTimes" >= 0 AND to_char("NextCheckDate",\'yyyy-MM-dd\') >=\'' + start.strftime("%Y-%m-%d") + '\')'
# # sql_count = sql_count + ' OR  (to_char("NextCheckDate",\'yyyy-MM-dd\')>=\'' + start.strftime("%Y-%m-%d") + '\' AND to_char("NextCheckDate",\'yyyy-MM-dd\') <= \'' + c_date + '\' AND "NextCheckCount"-"UsedTimes">=0))'
#
# sql_count = sql_count + ' AND (("NextCheckCount"-"UsedTimes" <= ' + '10' + ' AND "NextCheckCount"-"UsedTimes" >= 0 AND to_char("NextCheckDate",\'yyyy-MM-dd\') >=\'' + start.strftime("%Y-%m-%d") + '\')'
# sql_count = sql_count + ' OR  (to_char("NextCheckDate",\'yyyy-MM-dd\')>=\'' + start.strftime("%Y-%m-%d") + '\' AND to_char("NextCheckDate",\'yyyy-MM-dd\') <= \'' + c_date + '\' AND "NextCheckCount"-"UsedTimes">=0))'
#
# sql = sql + ' AND (("NextCheckCount"-"UsedTimes" <= ' + '10' + ' AND "NextCheckCount"-"UsedTimes" >= 0 AND to_char("NextCheckDate",\'yyyy-MM-dd\') >=\'' + start.strftime("%Y-%m-%d") + '\')'
# sql = sql + ' OR  (to_char("NextCheckDate",\'yyyy-MM-dd\')>=\'' + start.strftime("%Y-%m-%d") + '\' AND to_char("NextCheckDate",\'yyyy-MM-dd\') <= \'' + c_date + '\' AND "NextCheckCount"-"UsedTimes">=0))'
# print(sql_count)
# sql = 'select "Id","SN","PartName","CheckCycleCount","UsedTimes","CheckCycle","NextCheckDate","Maintainer","TrnDate","NextCheckCount" FROM "PartItem" WHERE to_char("TrnDate",\'yyyy-MM-dd\') >= \'' + end.strftime(
#     "%Y-%m-%d") + '\' and  to_char("TrnDate",\'yyyy-MM-dd\') <=\'' + start.strftime("%Y-%m-%d") + '\''
# sql = sql + 'AND "TrnDate" >= \'{0}\''.format('2019-07-01')
# sql = 'SELECT "PartName",COUNT("PartName") FROM "PartItem" where to_char("TrnDate",\'yyyy-MM-dd\') >=\'' + end.strftime("%Y-%m-%d") + '\' and to_char("TrnDate",\'yyyy-MM-dd\') <=\'' + start.strftime("%Y-%m-%d") + '\'' +'and to_char("NextCheckDate",\'yyyy-MM-dd\') <>\'None\';'

# sql3 = sql + 'AND ("NextCheckCount"-"UsedTimes" < 0 OR ("NextCheckDate" < \'' + start.strftime("%Y-%m-%d") + '\')) GROUP BY "PartName" '

# 未设定
# sql_no_nextcheckdate = 'SELECT "Id" FROM "PartItem" where "NextCheckDate" IS NULL order by "Id" '
# c_count=str(5)
# c_date= (datetime.current_date + timedelta(days=20)).strftime("%Y-%m-%d")
# #超标的SN
# danger_data = 'select count(*) from "PartItem" where "NextCheckDate" IS NOT NULL AND ("NextCheckCount"<"UsedTimes" OR to_char("NextCheckDate",\'yyyy-MM-dd\') <\'' + start.strftime("%Y-%m-%d") + '\')'
# #预警的数量
# warning_data = 'select count(*) FROM "PartItem" where "NextCheckDate" IS NOT NULL'
# warning_data = warning_data + ' AND (("NextCheckCount"-"UsedTimes" <= ' + c_count + ' AND "NextCheckCount"-"UsedTimes" >= 0 AND to_char("NextCheckDate",\'yyyy-MM-dd\') >=\'' + start.strftime("%Y-%m-%d") + '\')'
# warning_data = warning_data + ' OR  (to_char("NextCheckDate",\'yyyy-MM-dd\')>=\'' + start.strftime("%Y-%m-%d") + '\' AND to_char("NextCheckDate",\'yyyy-MM-dd\') <= \'' + c_date + '\' AND "NextCheckCount"-"UsedTimes">=0))'
#
# #超标的的有设保养人的
# danger_data_Mainter = danger_data+' AND "Maintainer" IS NOT NULL;'
# #超标的的没有设保养人的
# danger_data_no_Mainter = danger_data+' AND "Maintainer" IS  NULL;'
#
# #预警的有设保养人的
# warning_data_Mainter = warning_data+'AND "Maintainer" IS NOT NULL;'
# #预警的没有设保养人的
# warning_data_no_Mainter = warning_data+'AND "Maintainer" IS  NULL;'
#
#
# #有保养人的 达到超标的数量和SN
# sle = 'select "Maintainer",count(*),array_agg("SN") from "PartItem" where "NextCheckDate" IS NOT NULL AND "Maintainer" IS NOT NULL AND ("NextCheckCount"<"UsedTimes" OR to_char("NextCheckDate",\'yyyy-MM-dd\') <\'' + start.strftime("%Y-%m-%d") + '\') GROUP BY "Maintainer" ORDER BY -count(*)'
# #没有有保养人的 达到超标的数量和SN
# sle2 = 'select "Maintainer",count(*),array_agg("SN") from "PartItem" where "NextCheckDate" IS NOT NULL AND "Maintainer" IS NULL AND ("NextCheckCount"<"UsedTimes" OR to_char("NextCheckDate",\'yyyy-MM-dd\') <\'' + start.strftime("%Y-%m-%d") + '\') GROUP BY "Maintainer"'
# #有保养人的 达到预警的数量和SN
# warning = 'select "Maintainer",count(*),array_agg("SN") FROM "PartItem" where "NextCheckDate" IS NOT NULL AND "Maintainer" IS NOT NULL'
# warning1 = warning + ' AND (("NextCheckCount"-"UsedTimes" <= ' + c_count + ' AND "NextCheckCount"-"UsedTimes" >= 0 AND to_char("NextCheckDate",\'yyyy-MM-dd\') >=\'' + start.strftime("%Y-%m-%d") + '\')'
# warning2 = warning1 + ' OR  (to_char("NextCheckDate",\'yyyy-MM-dd\')>=\'' + start.strftime("%Y-%m-%d") + '\' AND to_char("NextCheckDate",\'yyyy-MM-dd\') <= \'' + c_date + '\' AND "NextCheckCount"-"UsedTimes">=0)) GROUP BY "Maintainer"'
#
# #没有保养人的 达到预警的数量和SN
# warning3 = 'select "Maintainer",count(*),array_agg("SN") FROM "PartItem" where "NextCheckDate" IS NOT NULL AND "Maintainer" IS NULL'
# warning4 = warning3 + ' AND (("NextCheckCount"-"UsedTimes" <= ' + c_count + ' AND "NextCheckCount"-"UsedTimes" >= 0 AND to_char("NextCheckDate",\'yyyy-MM-dd\') >=\'' + start.strftime("%Y-%m-%d") + '\')'
# warning5 = warning4 + ' OR  (to_char("NextCheckDate",\'yyyy-MM-dd\')>=\'' + start.strftime("%Y-%m-%d") + '\' AND to_char("NextCheckDate",\'yyyy-MM-dd\') <= \'' + c_date + '\' AND "NextCheckCount"-"UsedTimes">=0)) GROUP BY "Maintainer"'


# sql4= sql +
# # 计算 查询数据的总的多少条数据
# sql_count = 'select count(*) FROM "PartItem" where 1=1'  # to_char("TrnDate",\'yyyy-MM-dd\') >= \''+ end.strftime("%Y-%m-%d")+'\' and to_char("TrnDate",\'yyyy-MM-dd\') <= \''+start.strftime("%Y-%m-%d")+'\''
# # 查询条件的数据
# sql = 'select "Id","SN","PartName","CheckCycleCount","UsedTimes","CheckCycle","NextCheckDate","Maintainer","TrnDate","NextCheckCount" FROM "PartItem" WHERE 1=1'  # to_char("TrnDate",\'yyyy-MM-dd\') >= \''+ end.strftime("%Y-%m-%d")+'\' and  to_char("TrnDate",\'yyyy-MM-dd\') <=\''+start.strftime("%Y-%m-%d")+'\''
# # 饼图数据按正常和预警和超标分类计算数量
# visual_sql = 'SELECT "PartName", COUNT("PartName") FROM "PartItem" where 1=1'  # to_char("TrnDate",\'yyyy-MM-dd\') >= \''+ end.strftime("%Y-%m-%d")+'\' and to_char("TrnDate",\'yyyy-MM-dd\') <= \''+start.strftime("%Y-%m-%d")+'\''
# # 柱状图的数据 按条件查询出来之后再 按负责人分类
# tab_sql = 'SELECT "Maintainer", COUNT("PartName") FROM "PartItem" where 1=1'  # to_char("TrnDate",\'yyyy-MM-dd\') >=\' ' + end.strftime("%Y-%m-%d") + '\' and  to_char("TrnDate",\'yyyy-MM-dd\') <=\'' + start.strftime("%Y-%m-%d") + '\''
# sn ="Z17002D72"
# c_count ='10'
# start = datetime.current_date
# c_date = (start + timedelta(days=20)).strftime("%Y-%m-%d")
# sql_count = sql_count + 'AND "SN" = \'' + sn + '\''
# sql = sql + 'AND "SN" = \'' + sn + '\''
# visual_sql = visual_sql + 'AND "SN" = \'' + sn + '\''
# tab_sql = tab_sql + 'AND "SN" = \'' + sn + '\''
#
# # normal
# visual_sql_normal = visual_sql + 'AND "NextCheckCount"-"UsedTimes" > ' + c_count + ' AND to_char("NextCheckDate",\'yyyy-MM-dd\') >\'' + c_date + '\' GROUP BY "PartName"'
# tab_normal = tab_sql + 'AND "NextCheckCount"-"UsedTimes" > ' + c_count + ' AND to_char("NextCheckDate",\'yyyy-MM-dd\') >\'' + c_date + '\' GROUP BY "Maintainer"'
# # warning
# visual_sql_waring = visual_sql + ' AND (("NextCheckCount"-"UsedTimes" <= ' + c_count + ' AND "NextCheckCount"-"UsedTimes" >= 0 AND to_char("NextCheckDate",\'yyyy-MM-dd\') >=\'' + start.strftime(
#     "%Y-%m-%d") + '\')'
# visual_sql_waring = visual_sql_waring + ' OR  (to_char("NextCheckDate",\'yyyy-MM-dd\')>=\'' + start.strftime(
#     "%Y-%m-%d") + '\' AND to_char("NextCheckDate",\'yyyy-MM-dd\') <= \'' + c_date + '\' AND "NextCheckCount"-"UsedTimes">=0))  GROUP BY "PartName"'
# tab_warning = tab_sql + ' AND ("NextCheckCount"-"UsedTimes" <= ' + c_count + ' AND "NextCheckCount"-"UsedTimes" >= 0 AND to_char("NextCheckDate",\'yyyy-MM-dd\') >=\'' + start.strftime(
#     "%Y-%m-%d") + '\')'
# tab_warning = tab_warning + ' OR  (to_char("NextCheckDate",\'yyyy-MM-dd\')>=\'' + start.strftime(
#     "%Y-%m-%d") + '\' AND to_char("NextCheckDate",\'yyyy-MM-dd\') <= \'' + c_date + '\' AND "NextCheckCount"-"UsedTimes">=0)  GROUP BY "Maintainer"'
# # danger
# visual_sql_danger = visual_sql + 'AND ("NextCheckCount"-"UsedTimes" < 0 OR "NextCheckDate" < \'' + start.strftime(
#     "%Y-%m-%d") + '\') GROUP BY "PartName"'
# tab_danger = tab_sql + 'AND ("NextCheckCount"-"UsedTimes" < 0 OR "NextCheckDate" < \'' + start.strftime(
#     "%Y-%m-%d") + '\') GROUP BY "Maintainer"'
# cur.execute(visual_sql_normal)
# normal = cur.fetchall()
# cur.execute(visual_sql_waring)
# warning = cur.fetchall()
# cur.execute(visual_sql_danger)
# danger = cur.fetchall()


    # cur.execute(sle2)
    # sle2_data = cur.fetchall()
    # cur.execute(warning2)
    # warning = cur.fetchall()
    # cur.execute(warning5)
    # warning6 = cur.fetchall()
    #
    # data_mail = mail_data_fun(sle_data,warning)
    # print(data_mail)
    #
    # # 没有保养人 的超标和
    # data_mail2 = mail_data_fun(sle2_data, warning6)
    # print(data_mail2)

# danger=[('name',7,['SN1','SN2']),]
# data_type = [('name',7,['SN1'],8,['SN'])]
# def mail_data_fun(danger,warning):
#     mail_list = []
#     mail_data=[]
#     for i in range(0,len(danger)):
#         mail_list.append(danger[i][0])
#     for j in range(0,len(warning)):
#         warning_name = warning[j][0]
#         if warning_name not in mail_list:
#             mail_list.append(warning_name)
#     for k in range(0,len(mail_list)):
#         mail_data.append([mail_list[k],0,[],0,[]])
#     if len(danger) > 0:
#         for a in range(0, len(mail_data)):
#             for b in range(0, len(danger)):
#                 if danger[b][0] == mail_data[a][0]:
#                     mail_data[a][1] = danger[b][1]
#                     mail_data[a][2].extend(danger[b][2])
#     if len(warning)>0:
#         for c in range(0,len(mail_data)):
#             for d in range(0,len(warning)):
#                 if warning[d][0] == mail_data[c][0]:
#                     mail_data[c][3] = warning[d][1]
#                     mail_data[c][4].extend(warning[d][2])
#     return mail_data





#     print(danger_data)
    # cur.execute(sql3)
    # data = cur.fetchall()
    # cur.execute(danger_data)
    # danger = cur.fetchall()
    # cur.execute(warning_data)
    # warning = cur.fetchall()
    #
    #
    # cur.execute(danger_data_Mainter)
    # danger_M = cur.fetchall()
    # cur.execute(danger_data_no_Mainter)
    # danger_N = cur.fetchall()
    #
    # cur.execute(warning_data_Mainter)
    # warning_M = cur.fetchall()
    # cur.execute(warning_data_no_Mainter)
    # warning_N = cur.fetchall()
    # # for i in range(0, len(data)):
    # #     print(data[i][6],data[i][9])
    # #     if data[i][6] == None :
    # #         # and data[i][9] == 0
    # #         data[i] = list(data[i])
    # #         data[i].append(0)
    # #     else:
    # #         data[i] = list(data[i])
    # #         time_end = datetime.strptime(str(data[i][6]).split(' ')[0], "%Y-%m-%d")
    # #         days = time_end - start_time
    # #         data[i].append(days.days)
    # #     if data[i][9] == 0:
    # #         data[i] = list(data[i])
    # #         data[i].append(0)
    # #     else:
    # #         data[i] = list(data[i])
    # #         data[i].append(data[i][9] - data[i][4])
    # # print(data)
    # print(danger)
    # print(warning)
    # print(danger_M)
    # print(danger_N)
    # print(warning_M)
    # print(warning_N)



#sql = 'select "PartItem"."SN","PartItem"."PN","PartItem"."Spec","Status","PartItem"."Maintainer","Content"' ',to_char("MaintenanceDate",\'yyyy-MM-dd\'),"PartItemId" FROM "MaintenanceLog" left outer join "PartItem" on "MaintenanceLog"."PartItemId" ="PartItem"."Id" '
# start = datetime.current_date
# delta = timedelta(days=300)
# end = start-delta
# c_count = str(10)
# c_date = (start + timedelta(days=20)).strftime("%Y-%m-%d")  # 拿到当前的时间+预警天数得到日期的范围是（当前时间,c_date）
# # # 正常
# # sql1 = sql + 'AND ("NextCheckCount"-"UsedTimes" > ' + c_count + ' AND "NextCheckDate" >\'' + c_date + '\' ) GROUP BY "Maintainer"'
# # # 预警
# # sql2 = sql + 'AND ("NextCheckCount"-"UsedTimes"<='+c_count+' AND "NextCheckCount"-"UsedTimes" >= 0 AND to_char("NextCheckDate",\'yyyy-MM-dd\') >=\'' + start.strftime("%Y-%m-%d") + '\') OR  (to_char("NextCheckDate",\'yyyy-MM-dd\')>=\'' + start.strftime("%Y-%m-%d") + '\' AND to_char("NextCheckDate",\'yyyy-MM-dd\') <= \'' + c_date + '\' AND "NextCheckCount"-"UsedTimes">=0) GROUP BY "Maintainer"'
# # # 超标
# # sql3 = sql + 'AND ("NextCheckCount"-"UsedTimes" < 0 OR "NextCheckDate" < \'' + start.strftime("%Y-%m-%d") + '\') GROUP BY "Maintainer"'
#
#
# tab_sql = 'SELECT "Maintainer", COUNT("PartName") FROM "PartItem" where to_char("TrnDate",\'yyyy-MM-dd\') >=\' '+ end.strftime("%Y-%m-%d")+'\' and  to_char("TrnDate",\'yyyy-MM-dd\') <=\''+start.strftime("%Y-%m-%d")+'\''
#
# # 正常
# table_normal = tab_sql + 'AND "NextCheckCount"-"UsedTimes" > '+c_count+' AND "NextCheckDate" >\''+c_date+'\' GROUP BY "Maintainer"'
# # 预警
# table_warning = tab_sql + ' AND ("NextCheckCount"-"UsedTimes" <= ' + c_count + ' AND "NextCheckCount"-"UsedTimes" >= 0 AND to_char("NextCheckDate",\'yyyy-MM-dd\') >=\'' + start.strftime("%Y-%m-%d") + '\')'
# table_warning = table_warning + ' OR  (to_char("NextCheckDate",\'yyyy-MM-dd\')>=\'' + start.strftime("%Y-%m-%d")+ '\' AND to_char("NextCheckDate",\'yyyy-MM-dd\') <= \'' + c_date + '\' AND "NextCheckCount"-"UsedTimes">=0) GROUP BY "Maintainer"'
# # 超标
# table_danger = tab_sql + 'AND ("NextCheckCount"-"UsedTimes" < 0 OR "NextCheckDate" < \''+start.strftime("%Y-%m-%d")+'\') GROUP BY "Maintainer"'

    # cur.execute(table_warning)
    # tab_warning = cur.fetchall()
    # print(table_warning)
    # cur.execute(table_danger)
    # tab_danger = cur.fetchall()
    # print(table_danger)
    #
    # name_list = []
    # name_data = []
    # #     #获取名字的列表
    # for i in range(0, len(tab_normal)):
    #     n_name = tab_normal[i][0]
    #     name_list.append(n_name)
    # for j in range(0, len(tab_warning)):
    #     w_name = tab_warning[j][0]
    #     if w_name not in name_list:
    #         name_list.append(w_name)
    # for k in range(0, len(tab_danger)):
    #     d_name = tab_danger[k][0]
    #     if d_name not in name_list:
    #         name_list.append(d_name)
    # # 把数据变成[["name",0,0,0]]
    # for l in range(0, len(name_list)):
    #     name_data.append([name_list[l], 0, 0, 0])
    # # 添加normal 数据：[]   [('name',12)]
    # print(name_data)
    # print(name_list)
    # if len(tab_normal) > 0:
    #     for a in range(0, len(name_data)):
    #         for b in range(0, len(tab_normal)):
    #             if tab_normal[b][0] == name_data[a][0]:
    #                 name_data[a][1] = tab_normal[b][1]
    # # 添加warning 数据
    # if len(tab_warning) > 0:
    #     for a in range(0, len(name_data)):
    #         for b in range(0, len(tab_warning)):
    #             if tab_warning[b][0] == name_data[a][0]:
    #                 name_data[a][2] = tab_warning[b][1]
    # # 添加danger 数据
    # if len(tab_danger) > 0:
    #     for a in range(0, len(name_data)):
    #         for b in range(0, len(tab_danger)):
    #             if tab_danger[b][0] == name_data[a][0]:
    #                 name_data[a][3] = tab_danger[b][1]
    #
    # # da = tab_query_way(warning,danger,normal)
    # print(name_data)


# def tab_query_way(tab_warning,tab_danger,tab_normal):
#     name_list=[]
#     name_data=[]
# #     #获取名字的列表
#     for i in range(0,len(tab_normal)):
#         n_name=tab_normal[i][0]
#         name_list.append(n_name)
#     for j in range(0,len(tab_warning)):
#         w_name=tab_warning[j][0]
#         if w_name not in name_list:
#             name_list.append(w_name)
#     for k in range(0,len(tab_danger)):
#         d_name=tab_danger[k][0]
#         if d_name not in name_list:
#             name_list.append(d_name)
#     #把数据变成[["name",0,0,0]]
#     for l in range(0,len(name_list)):
#         name_data.append([name_list[l],0,0,0])
#     #添加normal 数据：[]   [('name',12)]
#     if len(tab_normal)>0:
#         for a in range(0,len(name_data)):
#             for b in range(0,len(tab_normal)):
#                 if tab_normal[b][0] == name_data[a][0]:
#                     name_data[a][1]=tab_normal[b][1]
#     #添加warning 数据
#     if len(tab_warning)>0:
#         for a in range(0,len(name_data)):
#             for b in range(0,len(tab_warning)):
#                 if tab_warning[b][0] == name_data[a][0]:
#                     name_data[a][2] = tab_warning[b][1]
#     # 添加danger 数据
#     if len(tab_danger) > 0:
#         for a in range(0, len(name_data)):
#             for b in range(0, len(tab_danger)):
#                 if tab_danger[b][0] == name_data[a][0]:
#                     name_data[a][3] =tab_danger[b][1]
#     return  name_data

# def modify_user(request):
#     if request.method == "POST":
#         id = int(request.POST.get('id',''))
#         session_id = int(request.session['user_Id'])
#         username = request.POST.get('username','')
#         department = request.POST.get('department','')
#         role = request.POST.get('role','')
#
#         check_DepartMent = Department.objects.filter(Department=department)
#         check_Name = User.objeqts.exclude(Id=id).filter(Name=username).count()
#         check_Role = User.objects.get(Id=session_id)
#         #验证角色是否为admin 是否有权限
#         if check_Role.Role != "admin":
#             return restful.params_error(message='Connect Administrator to check permission')
#         #检查姓名是否用过
#         if check_Name >0:
#             return restful.params_error(message='User Name Had Used')
#         #检查部门的存在性
#         if check_DepartMent.count() == 0 :
#             return restful.params_error(message='Department Not Exist')
#         department_id=list(check_DepartMent.values("Id"))[0]["Id"]
#         if session_id == id:
#             """修改自己的个人信息"""
#             User.objects.filter(Id=id).update(Name=username, Role=role, UpdatedTime=UpdatedTime,DepartmentId=department_id)
#             return restful.ok(message="user modify success",data={"user":"Myself"})
#         else:
#             User.objects.filter(Id=id).update(Name=username, Role=role, UpdatedTime=UpdatedTime,DepartmentId=department_id)
#             return restful.ok(message="user modify success", data={"user": "other"})


        # if user_obj.Role == "admin":
        #     try:
        #         user = User.objects.exclude(Id=id).get(Name=username)
        #         if user:
        #             return restful.params_error(message='user name had used')
        #     except:
        #         try:
        #             modify_department = Department.objects.get(Department=department)
        #             department_id = modify_department.Id
        #             User.objects.filter(Id=id).update(Name=username, Role=role, UpdatedTime=UpdatedTime,
        #                                               DepartmentId=department_id)
        #             return restful.ok(message="user modify success")
        #         except:
        #             User.objects.filter(Id=id).update(Name=username, Role=role, UpdatedTime=UpdatedTime)
        #             return restful.ok(message='User modify success')
        # else:
        #     return restful.params_error(message="please connect admin")


"""
import turtle
from datetime import *
# 抬起画笔，向前运动一段距离放下
def Skip(step):
    turtle.penup()
    turtle.forward(step)
    turtle.pendown()
def mkHand(name, length):
    turtle.reset()                                   # 注册Turtle形状，建立表针Turtle
    Skip(-length * 0.1)
    turtle.begin_poly()                              # 开始记录多边形的顶点。当前的乌龟位置是多边形的第一个顶点。
    turtle.forward(length * 1.1)
    turtle.end_poly()                                # 停止记录多边形的顶点。当前的乌龟位置是多边形的最后一个顶点。将与第一个顶点相连。
    handForm = turtle.get_poly()                     # 返回最后记录的多边形。
    turtle.register_shape(name, handForm)
def Init():
    global secHand, minHand, hurHand, printer
    turtle.mode("logo")                             # 重置Turtle指向北
    mkHand("secHand", 135)                          # 建立三个表针Turtle并初始化
    mkHand("minHand", 125)
    mkHand("hurHand", 90)
    secHand = turtle.Turtle()
    secHand.shape("secHand")
    minHand = turtle.Turtle()
    minHand.shape("minHand")
    hurHand = turtle.Turtle()
    hurHand.shape("hurHand")
    for hand in secHand, minHand, hurHand:
        hand.shapesize(1, 1, 3)
        hand.speed(0)
    printer = turtle.Turtle()                       # 建立输出文字Turtle
    printer.hideturtle()                            # 隐藏画笔的turtle形状
    printer.penup()
def SetupClock(radius):
    turtle.reset()                                  # 建立表的外框
    turtle.pensize(7)
    for i in range(60):
        Skip(radius)
        if i % 5 == 0:
            turtle.forward(20)
            Skip(-radius - 20)
            Skip(radius + 20)
            if i == 0:
                turtle.write(int(12), align="center", font=("Courier", 14, "bold"))
            elif i == 30:
                Skip(25)
                turtle.write(int(i / 5), align="center", font=("Courier", 14, "bold"))
                Skip(-25)
            elif (i == 25 or i == 35):
                Skip(20)
                turtle.write(int(i / 5), align="center", font=("Courier", 14, "bold"))
                Skip(-20)
            else:
                turtle.write(int(i / 5), align="center", font=("Courier", 14, "bold"))
            Skip(-radius - 20)
        else:
            turtle.dot(5)
            Skip(-radius)
        turtle.right(6)
def Week(t):
    week = ["星期一", "星期二", "星期三","星期四", "星期五", "星期六", "星期日"]
    return week[t.weekday()]
def Date(t):
    y = t.year
    m = t.month
    d = t.day
    return "%s %d%d" % (y, m, d)
def Tick():                                                  # 绘制表针的动态显示
    t = datetime.today()
    second = t.second + t.microsecond * 0.000001
    minute = t.minute + second / 60.0
    hour = t.hour + minute / 60.0
    secHand.setheading(6 * second)
    minHand.setheading(6 * minute)
    hurHand.setheading(30 * hour)
    turtle.tracer(False)
    printer.forward(65)
    printer.write(Week(t), align="center",font=("Courier", 14, "bold"))
    printer.back(130)
    printer.write(Date(t), align="center",font=("Courier", 14, "bold"))
    printer.home()
    turtle.tracer(True)
    turtle.ontimer(Tick, 100)                      # 100ms后继续调用tick
def main():                                        # 打开/关闭龟动画，并为更新图纸设置延迟。
    turtle.tracer(False)
    Init()
    SetupClock(160)
    turtle.tracer(True)
    Tick()
    turtle.mainloop()
if __name__ == "__main__":
    main()



import os
import sys
import time
import logging


file_name = os.path.split(os.path.splitext(sys.argv[0])[0])[-1]
file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'log')
log_time = time.strftime("%Y-%m-%d.log", time.localtime())


class Rookie:
    def __getattr__(self, items):
        return getattr(self.logger, items)

    @property
    def logger(self):
        return self.__logger

    @logger.setter
    def logger(self, func):
        self.__logger = func
    def __init__(self, set_level="INFO", name=file_name, log_name=log_time, log_path=file_path, role=True):
        self.__logger = logging.getLogger(name)
        self.__logger.setLevel(getattr(logging, set_level.upper()) if hasattr(logging, set_level.upper()) else logging.INFO)
        if not os.path.exists(log_path):
            os.makedirs(log_path)
        formatter = logging.Formatter(fmt="%(asctime)s - {0} -%(levelname)s  -%(message)s".format(__file__),datefmt="%Y-%m-%d  %H:%M:%S %p %a", )
        create_list = []
        create_list.append(logging.FileHandler(os.path.join(log_path, log_name), encoding="utf-8"))
        if role:
            create_list.append(logging.StreamHandler())
        for i in create_list:
            i.setFormatter(formatter)
            self.addHandler(i)
a = Rookie()
a.warning("函数执行定义")













#计算预算编码的月费用的限制
import calendar
import time
def limit_fee():
    #先拿到每月的限制费用
    #或者是先拿到每周的限制费用
    month_fee =200
    #计算当前月的预算编码的费用
    day_now = time.localtime()
    day_begin = '%d-%02d-01' % (day_now.tm_year, day_now.tm_mon)
    wday,monthRange = calendar.monthrange(day_now.tm_year,day_now.tm_mon)
    day_end ='%d-%02d-%02d' % (day_now.tm_year,day_now.tm_mon,monthRange)
    print(day_begin,day_end)
    #或者说计算当前一周的预算编码费用
limit_fee()


"""
"""
‘’‘’‘’‘’‘’系统信息的command‘’‘’‘’‘’‘’                   
arch                        显示机器的处理器架构
uname -m                    显示机器的处理器架构
uname -r                    显示正在使用的内核版本 
dmidecode -q                显示硬件系统部件 - (SMBIOS / DMI) 
hdparm -i /dev/hda          罗列一个磁盘的架构特性 
hdparm -tT /dev/sda         在磁盘上执行测试性读取操作 
cat /proc/cpuinfo           显示CPU info的信息 
cat /proc/interrupts        显示中断 
cat /proc/meminfo           校验内存使用 
cat /proc/swaps             显示哪些swap被使用 
cat /proc/version           显示内核的版本 
cat /proc/net/dev           显示网络适配器及统计 
cat /proc/mounts            显示已加载的文件系统 
lspci -tv                   罗列 PCI 设备 
lsusb -tv                   显示 USB 设备 
date                        显示系统日期 
cal 2007                    显示2007年的日历表 
date 041217002007.00        设置日期和时间 - 月日时分年.秒 
clock -w                    将时间修改保存到 BIOS 
‘’‘’‘’‘’‘’‘’关机(系统的关机，重启以及登出)‘’‘’‘’‘’‘’‘’‘’
shutdown -h now             关闭系统
init 0                      关闭系统
telinit 0                   关闭系统
shutdown -h hours:minutes & 按预定时间关闭系统 
shutdown -c                 取消按预定时间关闭系统 
shutdown -r now             重启
reboot                      重启
logout                      注销
''''''''''''文件和目录''''''''''''''''''''
cd /home                    进入 '/ home' 目录' 
cd ..                       返回上一级目录 
cd ../..                    返回上两级目录 
cd                          进入个人的主目录 
cd ~user1                   进入个人的主目录 
cd -                        返回上次所在的目录 
pwd                         显示工作路径 
ls                          查看目录中的文件 
ls -F                       查看目录中的文件 
ls -l                       显示文件和目录的详细资料 
ls -a                       显示隐藏文件 
ls *[0-9]*                  显示包含数字的文件名和目录名 
tree                        显示文件和目录由根目录开始的树形结构
lstree                      显示文件和目录由根目录开始的树形结构
mkdir dir1                  创建一个叫做 'dir1' 的目录' 
mkdir dir1 dir2             同时创建两个目录 
mkdir -p /tmp/dir1/dir2     创建一个目录树 
rm -f file1                 删除一个叫做 'file1' 的文件' 
rmdir dir1                  删除一个叫做 'dir1' 的目录' 
rm -rf dir1                 删除一个叫做 'dir1' 的目录并同时删除其内容 
rm -rf dir1 dir2            同时删除两个目录及它们的内容 
mv dir1 new_dir             重命名/移动 一个目录 
cp file1 file2              复制一个文件 
cp dir/* .                  复制一个目录下的所有文件到当前工作目录 
cp -a /tmp/dir1 .           复制一个目录到当前工作目录 
cp -a dir1 dir2             复制一个目录 
ln -s file1 lnk1            创建一个指向文件或目录的软链接 
ln file1 lnk1               创建一个指向文件或目录的物理链接 
touch -t 0712250000 file1   修改一个文件或目录的时间戳 - (YYMMDDhhmm) 
file file1 outputs the mime type of the file as text 
iconv -l                    列出已知的编码 
iconv -f fromEncoding -t toEncoding inputFile > outputFile creates a new from the given input file by assuming it is encoded in fromEncoding and converting it to toEncoding. 
find . -maxdepth 1 -name *.jpg -print -exec convert "{}" -resize 80x60 "thumbs/{}" \; batch resize files in the current directory and send them to a thumbnails directory (requires convert from Imagemagick)
‘’‘’‘’‘’‘’文件搜索‘’‘’‘’‘’‘’‘’
find / -name file1                          从 '/' 开始进入根文件系统搜索文件和目录 
find / -user user1                          搜索属于用户 'user1' 的文件和目录 
find /home/user1 -name \*.bin               在目录 '/ home/user1' 中搜索带有'.bin' 结尾的文件 
find /usr/bin -type f -atime +100           搜索在过去100天内未被使用过的执行文件 
find /usr/bin -type f -mtime -10            搜索在10天内被创建或者修改过的文件 
find / -name \*.rpm -exec chmod 755 '{}' \; 搜索以 '.rpm' 结尾的文件并定义其权限 
find / -xdev -name \*.rpm                   搜索以 '.rpm' 结尾的文件，忽略光驱、捷盘等可移动设备 
locate \*.ps                                寻找以 '.ps'结尾的文件 - 先运行 'updatedb' 命令 
whereis halt                                显示一个二进制文件、源码或man的位置 
which halt                                  显示一个二进制文件或可执行文件的完整路径
‘’‘’‘’‘’‘’‘挂载一个文件系统’‘’‘’‘’‘’‘’‘’‘’‘’
mount /dev/hda2 /mnt/hda2                   挂载一个叫做hda2的盘 - 确定目录 '/ mnt/hda2' 已经存在 
umount /dev/hda2                            卸载一个叫做hda2的盘 - 先从挂载点 '/ mnt/hda2' 退出 
fuser -km /mnt/hda2                         当设备繁忙时强制卸载 
umount -n /mnt/hda2                         运行卸载操作而不写入 /etc/mtab 文件- 当文件为只读或当磁盘写满时非常有用 
mount /dev/fd0 /mnt/floppy                  挂载一个软盘 
mount /dev/cdrom /mnt/cdrom                 挂载一个cdrom或dvdrom 
mount /dev/hdc /mnt/cdrecorder              挂载一个cdrw或dvdrom 
mount /dev/hdb /mnt/cdrecorder              挂载一个cdrw或dvdrom 
mount -o loop file.iso /mnt/cdrom           挂载一个文件或ISO镜像文件 
mount -t vfat /dev/hda5 /mnt/hda5           挂载一个Windows FAT32文件系统 
mount /dev/sda1 /mnt/usbdisk                挂载一个usb 捷盘或闪存设备 
mount -t smbfs -o username=user,password=pass //WinClient/share /mnt/share  挂载一个windows网络共享 
‘’‘’‘’‘’‘’‘’‘’‘磁盘空间’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’
df -h                                                                   显示已经挂载的分区列表 
ls -lSr |more                                                           以尺寸大小排列文件和目录 
du -sh dir1                                                             估算目录 'dir1'     已经使用的磁盘空间' 
du -sk * | sort -rn                                                     以容量大小为依据依次显示文件和目录的大小 
rpm -q -a --qf '%10{SIZE}t%{NAME}n' | sort -k1,1n                       以大小为依据依次显示已安装的rpm包所使用的空间 (fedora, redhat类系统) 
dpkg-query -W -f='${Installed-Size;10}t${Package}n' | sort -k1,1n       以大小为依据显示已安装的deb包所使用的空间 (ubuntu, debian类系统) 
‘’‘’‘’‘’‘’‘’‘’‘’‘’用户和群组‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’
groupadd group_name                                                     创建一个新用户组 
groupdel group_name                                                     删除一个用户组 
groupmod -n new_group_name old_group_name                               重命名一个用户组 
useradd -c "Name Surname " -g admin -d /home/user1 -s /bin/bash user1   创建一个属于 "admin" 用户组的用户 
useradd user1                                                           创建一个新用户 
userdel -r user1                                                        删除一个用户 ( '-r' 排除主目录) 
usermod -c "User FTP" -g system -d /ftp/user1 -s /bin/nologin user1     修改用户属性 
passwd                                                                  修改口令 
passwd user1                                                            修改一个用户的口令 (只允许root执行) 
chage -E 2005-12-31 user1                                               设置用户口令的失效期限 
pwck                                                                    检查 '/etc/passwd' 的文件格式和语法修正以及存在的用户 
grpck                                                                   检查 '/etc/passwd' 的文件格式和语法修正以及存在的群组 
newgrp group_name                                                       登陆进一个新的群组以改变新创建文件的预设群组
‘’‘’‘’‘’‘’‘’‘’‘’‘’文件的权限 - 使用 "+" 设置权限，使用 "-" 用于取消‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘
ls -lh                                          显示权限 
ls /tmp | pr -T5 -W$COLUMNS                     将终端划分成5栏显示 
chmod ugo+rwx directory1                        设置目录的所有人(u)、群组(g)以及其他人(o)以读（r ）、写(w)和执行(x)的权限 
chmod go-rwx directory1                         删除群组(g)与其他人(o)对目录的读写执行权限 
chown user1 file1                               改变一个文件的所有人属性 
chown -R user1 directory1                       改变一个目录的所有人属性并同时改变改目录下所有文件的属性 
chgrp group1 file1                              改变文件的群组 
chown user1:group1 file1                        改变一个文件的所有人和群组属性 
find / -perm -u+s                               罗列一个系统中所有使用了SUID控制的文件 
chmod u+s /bin/file1                            设置一个二进制文件的 SUID 位 - 运行该文件的用户也被赋予和所有者同样的权限 
chmod u-s /bin/file1                            禁用一个二进制文件的 SUID位 
chmod g+s /home/public                          设置一个目录的SGID 位 - 类似SUID ，不过这是针对目录的 
chmod g-s /home/public                          禁用一个目录的 SGID 位 
chmod o+t /home/public                          设置一个文件的 STIKY 位 - 只允许合法所有人删除文件 
chmod o-t /home/public                          禁用一个目录的 STIKY 位
’‘’‘’‘’‘’‘’‘’‘’‘’‘文件的特殊属性 - 使用 "+" 设置权限，使用 "-" 用于取消’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’
chattr +a file1                                 只允许以追加方式读写文件 
chattr +c file1                                 允许这个文件能被内核自动压缩/解压 
chattr +d file1                                 在进行文件系统备份时，dump程序将忽略这个文件 
chattr +i file1                                 设置成不可变的文件，不能被删除、修改、重命名或者链接 
chattr +s file1                                 允许一个文件被安全地删除 
chattr +S file1                                 一旦应用程序对这个文件执行了写操作，使系统立刻把修改的结果写到磁盘 
chattr +u file1                                 若文件被删除，系统会允许你在以后恢复这个被删除的文件 
lsattr                                          显示特殊的属性 
‘’‘’‘’‘’‘’‘’‘’‘’‘’‘打包和压缩文件’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’
bunzip2 file1.bz2                               解压一个叫做 'file1.bz2'的文件 
bzip2 file1                                     压缩一个叫做 'file1' 的文件 
gunzip file1.gz                                 解压一个叫做 'file1.gz'的文件 
gzip file1                                      压缩一个叫做 'file1'的文件 
gzip -9 file1                                   最大程度压缩 
rar a file1.rar test_file                       创建一个叫做 'file1.rar' 的包 
rar a file1.rar file1 file2 dir1                同时压缩 'file1', 'file2' 以及目录 'dir1' 
rar x file1.rar                                 解压rar包 
unrar x file1.rar                               解压rar包 
tar -cvf archive.tar file1                      创建一个非压缩的 tarball 
tar -cvf archive.tar file1 file2 dir1           创建一个包含了 'file1', 'file2' 以及 'dir1'的档案文件 
tar -tf archive.tar                             显示一个包中的内容 
tar -xvf archive.tar                            释放一个包 
tar -xvf archive.tar -C /tmp                    将压缩包释放到 /tmp目录下 
tar -cvfj archive.tar.bz2 dir1                  创建一个bzip2格式的压缩包 
tar -jxvf archive.tar.bz2                       解压一个bzip2格式的压缩包 
tar -cvfz archive.tar.gz dir1                   创建一个gzip格式的压缩包 
tar -zxvf archive.tar.gz                        解压一个gzip格式的压缩包 
zip file1.zip file1                             创建一个zip格式的压缩包 
zip -r file1.zip file1 file2 dir1               将几个文件和目录同时压缩成一个zip格式的压缩包 
unzip file1.zip                                 解压一个zip格式压缩包
‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’RPM 包 - （Fedora, Redhat及类似系统）‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘
rpm -ivh package.rpm                            安装一个rpm包 
rpm -ivh --nodeeps package.rpm                  安装一个rpm包而忽略依赖关系警告 
rpm -U package.rpm                              更新一个rpm包但不改变其配置文件 
rpm -F package.rpm                              更新一个确定已经安装的rpm包 
rpm -e package_name.rpm                         删除一个rpm包 
rpm -qa                                         显示系统中所有已经安装的rpm包 
rpm -qa | grep httpd                            显示所有名称中包含 "httpd" 字样的rpm包 
rpm -qi package_name                            获取一个已安装包的特殊信息 
rpm -qg "System Environment/Daemons"            显示一个组件的rpm包 
rpm -ql package_name                            显示一个已经安装的rpm包提供的文件列表 
rpm -qc package_name                            显示一个已经安装的rpm包提供的配置文件列表 
rpm -q package_name --whatrequires              显示与一个rpm包存在依赖关系的列表 
rpm -q package_name --whatprovides              显示一个rpm包所占的体积 
rpm -q package_name --scripts                   显示在安装/删除期间所执行的脚本l 
rpm -q package_name --changelog                 显示一个rpm包的修改历史 
rpm -qf /etc/httpd/conf/httpd.conf              确认所给的文件由哪个rpm包所提供 
rpm -qp package.rpm -l                          显示由一个尚未安装的rpm包提供的文件列表 
rpm --import /media/cdrom/RPM-GPG-KEY           导入公钥数字证书 
rpm --checksig package.rpm                      确认一个rpm包的完整性 
rpm -qa gpg-pubkey                              确认已安装的所有rpm包的完整性 
rpm -V package_name                             检查文件尺寸、 许可、类型、所有者、群组、MD5检查以及最后修改时间 
rpm -Va                                         检查系统中所有已安装的rpm包- 小心使用 
rpm -Vp package.rpm                             确认一个rpm包还未安装 
rpm2cpio package.rpm | cpio --extract --make-directories *bin*      从一个rpm包运行可执行文件 
rpm -ivh /usr/src/redhat/RPMS/`arch`/package.rpm    从一个rpm源码安装一个构建好的包 
rpmbuild --rebuild package_name.src.rpm             从一个rpm源码构建一个 rpm 包
‘’‘’‘’‘’‘’‘’‘’‘’‘YUM 软件包升级器 - （Fedora, RedHat及类似系统）’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘
yum install package_name                        下载并安装一个rpm包 
yum localinstall package_name.rpm               将安装一个rpm包，使用你自己的软件仓库为你解决所有依赖关系 
yum update package_name.rpm                     更新当前系统中所有安装的rpm包 
yum update package_name                         更新一个rpm包 
yum remove package_name                         删除一个rpm包 
yum list                                        列出当前系统中安装的所有包 
yum search package_name                         在rpm仓库中搜寻软件包 
yum clean packages                              清理rpm缓存删除下载的包 
yum clean headers                               删除所有头文件 
yum clean all                                   删除所有缓存的包和头文件
’‘’‘’‘’‘’‘’‘’‘’‘’DEB 包 (Debian, Ubuntu 以及类似系统)‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’
dpkg -i package.deb                             安装/更新一个 deb 包 
dpkg -r package_name                            从系统删除一个 deb 包 
dpkg -l                                         显示系统中所有已经安装的 deb 包 
dpkg -l | grep httpd                            显示所有名称中包含 "httpd" 字样的deb包 
dpkg -s package_name                            获得已经安装在系统中一个特殊包的信息 
dpkg -L package_name                            显示系统中已经安装的一个deb包所提供的文件列表 
dpkg --contents package.deb                     显示尚未安装的一个包所提供的文件列表 
dpkg -S /bin/ping                               确认所给的文件由哪个deb包提供 
‘’‘’‘’‘’‘’‘’‘’‘’‘’APT 软件工具 (Debian, Ubuntu 以及类似系统)‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’
apt-get install package_name                    安装/更新一个 deb 包 
apt-cdrom install package_name                  从光盘安装/更新一个 deb 包 
apt-get update                                  升级列表中的软件包 
apt-get upgrade                                 升级所有已安装的软件 
apt-get remove package_name                     从系统删除一个deb包 
apt-get check                                   确认依赖的软件仓库正确 
apt-get clean                                   从下载的软件包中清理缓存 
apt-cache search searched-package               返回包含所要搜索字符串的软件包名称
‘’‘’‘’‘’‘’‘’‘’‘’‘’‘查看文件内容’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’
cat file1                   从第一个字节开始正向查看文件的内容 
tac file1                   从最后一行开始反向查看一个文件的内容 
more file1                  查看一个长文件的内容 
less file1                  类似于 'more' 命令，但是它允许在文件中和正向操作一样的反向操作 
head -2 file1               查看一个文件的前两行 
tail -2 file1               查看一个文件的最后两行 
tail -f /var/log/messages   实时查看被添加到一个文件中的内容
‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’文本处理‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’
cat file1 file2 ... | command <> file1_in.txt_or_file1_out.txt general syntax for text manipulation using PIPE, STDIN and STDOUT 
cat file1 | command( sed, grep, awk, grep, etc...) > result.txt             合并一个文件的详细说明文本，并将简介写入一个新文件中 
cat file1 | command( sed, grep, awk, grep, etc...) >> result.txt            合并一个文件的详细说明文本，并将简介写入一个已有的文件中 
grep Aug /var/log/messages                                                  在文件 '/var/log/messages'中查找关键词"Aug" 
grep ^Aug /var/log/messages                                                 在文件 '/var/log/messages'中查找以"Aug"开始的词汇 
grep [0-9] /var/log/messages                                                选择 '/var/log/messages' 文件中所有包含数字的行 
grep Aug -R /var/log/*                                                      在目录 '/var/log' 及随后的目录中搜索字符串"Aug" 
sed 's/stringa1/stringa2/g' example.txt                                     将example.txt文件中的 "string1" 替换成 "string2" 
sed '/^$/d' example.txt                                                     从example.txt文件中删除所有空白行 
sed '/ *#/d; /^$/d' example.txt                                             从example.txt文件中删除所有注释和空白行 
echo 'esempio' | tr '[:lower:]' '[:upper:]'                                 合并上下单元格内容 
sed -e '1d' result.txt                                                      从文件example.txt 中排除第一行 
sed -n '/stringa1/p'                                                        查看只包含词汇 "string1"的行 
sed -e 's/ *$//' example.txt                                                删除每一行最后的空白字符 
sed -e 's/stringa1//g' example.txt                                          从文档中只删除词汇 "string1" 并保留剩余全部 
sed -n '1,5p;5q' example.txt                                                查看从第一行到第5行内容 
sed -n '5p;5q' example.txt                                                  查看第5行 
sed -e 's/00*/0/g' example.txt                                              用单个零替换多个零 
cat -n file1                                                                标示文件的行数 
cat example.txt | awk 'NR%2==1'                                             删除example.txt文件中的所有偶数行 
echo a b c | awk '{print $1}'                                               查看一行第一栏 
echo a b c | awk '{print $1,$3}'                                            查看一行的第一和第三栏 
paste file1 file2                                                           合并两个文件或两栏的内容 
paste -d '+' file1 file2                                                    合并两个文件或两栏的内容，中间用"+"区分 
sort file1 file2                                                            排序两个文件的内容 
sort file1 file2 | uniq                                                     取出两个文件的并集(重复的行只保留一份) 
sort file1 file2 | uniq -u                                                  删除交集，留下其他的行 
sort file1 file2 | uniq -d                                                  取出两个文件的交集(只留下同时存在于两个文件中的文件) 
comm -1 file1 file2                                                         比较两个文件的内容只删除 'file1' 所包含的内容 
comm -2 file1 file2                                                         比较两个文件的内容只删除 'file2' 所包含的内容 
comm -3 file1 file2                                                         比较两个文件的内容只删除两个文件共有的部分
‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘字符设置和文件格式转换’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘
dos2unix filedos.txt fileunix.txt           将一个文本文件的格式从MSDOS转换成UNIX 
unix2dos fileunix.txt filedos.txt           将一个文本文件的格式从UNIX转换成MSDOS 
recode ..HTML < page.txt > page.html        将一个文本文件转换成html 
recode -l | more                            显示所有允许的转换格式 
’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘文件系统分析’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’
badblocks -v /dev/hda1                      检查磁盘hda1上的坏磁块 
fsck /dev/hda1                              修复/检查hda1磁盘上linux文件系统的完整性 
fsck.ext2 /dev/hda1                         修复/检查hda1磁盘上ext2文件系统的完整性 
e2fsck /dev/hda1                            修复/检查hda1磁盘上ext2文件系统的完整性 
e2fsck -j /dev/hda1                         修复/检查hda1磁盘上ext3文件系统的完整性 
fsck.ext3 /dev/hda1                         修复/检查hda1磁盘上ext3文件系统的完整性 
fsck.vfat /dev/hda1                         修复/检查hda1磁盘上fat文件系统的完整性 
fsck.msdos /dev/hda1                        修复/检查hda1磁盘上dos文件系统的完整性 
dosfsck /dev/hda1                           修复/检查hda1磁盘上dos文件系统的完整性
‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘初始化一个文件系统’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘
mkfs /dev/hda1                      在hda1分区创建一个文件系统 
mke2fs /dev/hda1                    在hda1分区创建一个linux ext2的文件系统 
mke2fs -j /dev/hda1                 在hda1分区创建一个linux ext3(日志型)的文件系统 
mkfs -t vfat 32 -F /dev/hda1        创建一个 FAT32 文件系统 
fdformat -n /dev/fd0                格式化一个软盘 
mkswap /dev/hda3                    创建一个swap文件系统
’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘SWAP文件系统’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘
mkswap /dev/hda3                创建一个swap文件系统 
swapon /dev/hda3                启用一个新的swap文件系统 
swapon /dev/hda2 /dev/hdb3      启用两个swap分区

’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’备份‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘
dump -0aj -f /tmp/home0.bak /home                                                   制作一个 '/home' 目录的完整备份 
dump -1aj -f /tmp/home0.bak /home                                                   制作一个 '/home'目录的交互式备份 
restore -if /tmp/home0.bak                                                          还原一个交互式备份 
rsync -rogpav --delete /home /tmp                                                   同步两边的目录 
rsync -rogpav -e ssh --delete /home ip_address:/tmp                                 通过SSH通道rsync 
rsync -az -e ssh --delete ip_addr:/home/public /home/local                          通过ssh和压缩将一个远程目录同步到本地目录 
rsync -az -e ssh --delete /home/local ip_addr:/home/public                          通过ssh和压缩将本地目录同步到远程目录 
dd bs=1M if=/dev/hda | gzip | ssh user@ip_addr 'dd of=hda.gz'                       通过ssh在远程主机上执行一次备份本地磁盘的操作 
dd if=/dev/sda of=/tmp/file1                                                        备份磁盘内容到一个文件 
tar -Puf backup.tar /home/user                                                      执行一次对 '/home/user' 目录的交互式备份操作 
( cd /tmp/local/ && tar c . ) | ssh -C user@ip_addr 'cd /home/share/ && tar x -p'   通过ssh在远程目录中复制一个目录内容 
( tar c /home ) | ssh -C user@ip_addr 'cd /home/backup-home && tar x -p'            通过ssh在远程目录中复制一个本地目录 
tar cf - . | (cd /tmp/backup ; tar xf - )                                           本地将一个目录复制到另一个地方，保留原有权限及链接 
find /home/user1 -name '*.txt' | xargs cp -av --target-directory=/home/backup/ --parents 从一个目录查找并复制所有以 '.txt' 结尾的文件到另一个目录 
find /var/log -name '*.log' | tar cv --files-from=- | bzip2 > log.tar.bz2           查找所有以 '.log' 结尾的文件并做成一个bzip包 
dd if=/dev/hda of=/dev/fd0 bs=512 count=1                                           做一个将 MBR (Master Boot Record)内容复制到软盘的动作 
dd if=/dev/fd0 of=/dev/hda bs=512 count=1                                           从已经保存到软盘的备份中恢复MBR内容 
’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’光盘‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘
cdrecord -v gracetime=2 dev=/dev/cdrom -eject blank=fast -force                     清空一个可复写的光盘内容 
mkisofs /dev/cdrom > cd.iso                                                         在磁盘上创建一个光盘的iso镜像文件 
mkisofs /dev/cdrom | gzip > cd_iso.gz                                               在磁盘上创建一个压缩了的光盘iso镜像文件 
mkisofs -J -allow-leading-dots -R -V "Label CD" -iso-level 4 -o ./cd.iso data_cd    创建一个目录的iso镜像文件 
cdrecord -v dev=/dev/cdrom cd.iso                                                   刻录一个ISO镜像文件 
gzip -dc cd_iso.gz | cdrecord dev=/dev/cdrom -                                      刻录一个压缩了的ISO镜像文件 
mount -o loop cd.iso /mnt/iso                                                       挂载一个ISO镜像文件 
cd-paranoia -B                                                                      从一个CD光盘转录音轨到 wav 文件中 
cd-paranoia -- "-3"                                                                 从一个CD光盘转录音轨到 wav 文件中（参数-3） 
cdrecord --scanbus                                                                  扫描总线以识别scsi通道 
dd if=/dev/hdc | md5sum                                                             校验一个设备的md5sum编码，例如一张 CD 
’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘网络 - （以太网和WIFI无线）’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’
ifconfig eth0                                                                       显示一个以太网卡的配置 
ifup eth0                                                                           启用一个 'eth0' 网络设备 
ifdown eth0                                                                         禁用一个 'eth0' 网络设备 
ifconfig eth0 192.168.1.1 netmask 255.255.255.0                                     控制IP地址 
ifconfig eth0 promisc                                                               设置 'eth0' 成混杂模式以嗅探数据包 (sniffing) 
dhclient eth0                                                                       以dhcp模式启用 'eth0' 
route -n show routing table 
route add -net 0/0 gw IP_Gateway configura default gateway 
route add -net 192.168.0.0 netmask 255.255.0.0 gw 192.168.1.1 configure static route to reach network '192.168.0.0/16' 
route del 0/0 gw IP_gateway remove static route 
echo "1" > /proc/sys/net/ipv4/ip_forward activate ip routing 
hostname show hostname of system 
host www.example.com lookup hostname to resolve name to ip address and viceversa
nslookup www.example.com lookup hostname to resolve name to ip address and viceversa
ip link show show link status of all interfaces 
mii-tool eth0 show link status of 'eth0' 
ethtool eth0 show statistics of network card 'eth0' 
netstat -tup show all active network connections and their PID 
netstat -tupl show all network services listening on the system and their PID 
tcpdump tcp port 80 show all HTTP traffic 
iwlist scan show wireless networks 
iwconfig eth1 show configuration of a wireless network card 
hostname show hostname 
host www.example.com lookup hostname to resolve name to ip address and viceversa 
nslookup www.example.com lookup hostname to resolve name to ip address and viceversa 
whois www.example.com lookup on Whois database 






java 位运算：
<<(左移) 在一定的范围内，每次向左移一位原来的数乘以2
>>(右移) 在一定的范围内，每次向右移一位原来的数除以2
>>和>>无符号的区别
>>：正数向右移高位用0补，负数向右移高位用1补
>>>:无论正数还是负数高位用0补





"""









