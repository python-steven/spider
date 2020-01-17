from datetime import datetime
import calendar
from django.shortcuts import render,redirect
from app.login.models import User
from django.contrib import messages
from django.http import HttpResponseRedirect,HttpResponse
from app.restful import force_logout,result,params_error,ok
import psycopg2
conn = psycopg2.connect(
                database="aemslite",
                host="127.0.0.1",
                user="postgres",
                password = "1234qwer!@#$QWER",
                port = 5432,)
'''获取字典数据的工具[{},{},{},......], 这里也是需要传sql语句就行'''
def dictdata(sqldict):
    cur = conn.cursor()
    cur.execute(sqldict, None)
    desc = cur.description
    return [dict(zip([col[0] for col in desc], row)) for row in cur.fetchall()]

def access_control(method):
    def check(request):
        now_time = datetime.now()
        last_access_time_str = request.COOKIES.get('LAST_ACCESS_TIME')
        
        last_access_time = datetime.strptime(last_access_time_str, '%Y-%m-%d %H:%M:%S')

        # if user did not operate web for more than 30 minutes, need logout
        passed_time = now_time - last_access_time
        if passed_time.total_seconds() > 1800:
            msg = "You don't operate AEMSLite system over 30 mins. For security issue you are logout automatically."
            return  force_logout(message=msg)
        
        # if user info have been updated, need logout
        user_id = request.session.get('user_Id','')
        user_info = User.objects.get(Id=user_id)
        updated_time_tmp = user_info.UpdatedTime
        updated_time = datetime.strptime(str(updated_time_tmp).split('.')[0], '%Y-%m-%d %H:%M:%S')

        passed_time = updated_time - last_access_time
        if passed_time.total_seconds() >= 0:
            msg = "Your info have been updated! For security issue you are logout automatically."
            return  force_logout(message=msg)

        return method(request)
    return check

'''
    ways for @ apply budgetcode items to cacluate fee and limit function
    get all budget of current month data and calculate money
    calendar.monthrange(int(now.year),int(now.month))     indicate for this month has how many days ...
'''
# "获取当前月的额度以及数据 全部转换成人民币为计算单位"
def FeeLimit_count(method):
    def check(self,request):
        #if you apply single forme need to check this partment and class items cash for check  ammount
        now = datetime.now()
        startTime = "%s-%s-01 00:00:00" % (now.year,now.month)
        endTime = "%s-%s-%s 23:59:59" % (now.year,now.month, calendar.monthrange(int(now.year), int(now.month))[1])
        ''' 
            get all Status is Approve data and data info include 
            (class："PurchaseType",price："UnitPrice",mount："Quantity",unit："Unit",currency："Currency",department："Department" ,"Status":'Approve' )
        '''
        price = request.POST.get('bud_price')              # price
        qty = request.POST.get('bud_qty')                  # mount
        money_type = request.POST.get('bud_money_type')    # currency

        Department = request.POST.get('Department','')  # department
        AccountTitle = request.POST.get('account_type','')  # account
        DepartId = dictdata('SELECT "Id" FROM "Department" WHERE "Department" = \''+Department+'\' AND "IsActivated" =\'true\' ORDER BY "UpdatedTime" DESC')[0]['Id']
        AccountId = dictdata('SELECT "Id" FROM "AccountTitle" WHERE "Type" = \''+AccountTitle+'\' AND "IsActivated" =\'true\' ORDER BY "UpdatedTime" DESC')[0]['Id']
        sqlFee = ' SELECT "LimitCost","LimitPeriod" FROM "FeeLimit" WHERE "DepartmentId"= \'' + str(DepartId) + '\'  AND "AccountTitleId" = \'' + str(AccountId) + '\' AND "IsActivated" =\'true\' ORDER BY "UpdatedTime" DESC'
        feefee = dictdata(sqlFee)
        if len(feefee) == 0:
            return method(self,request)
        if len(feefee) != 0 and feefee[0]['LimitPeriod'] == "month":
            startTime = "%s-%s-01 00:00:00" % (now.year, now.month)
            endTime = "%s-%s-%s 23:59:59" % (now.year, now.month, calendar.monthrange(int(now.year), int(now.month))[1])
        if len(feefee) != 0 and feefee[0]['LimitPeriod'] == "year":
            startTime = "%s-01-01 00:00:00" % (now.year)
            endTime = "%s-12-%s 23:59:59" % (now.year, calendar.monthrange(int(now.year), 12)[1])
        if len(feefee) != 0 and feefee[0]['LimitPeriod'] == "week":
            import datetime as da
            monday, sunday = da.date.today(), da.date.today()
            one_day = da.timedelta(days=1)
            while monday.weekday() != 0:
                monday -= one_day
            while sunday.weekday() != 6:
                sunday += one_day
            startTime = "%s 00:00:00" % (str(monday))
            endTime = "%s 23:59:59" % (str(sunday))

        sqlBudget = ' SELECT "UnitPrice","Quantity","Currency" FROM "BudgetCodeForm" WHERE "Department" = \''+Department +'\' AND "PurchaseType" = \''+AccountTitle+'\''
        sqlBudget += ' AND ( "Status" =\'Approve\' OR "Status" =\'Process\' ) AND "CreatedTime" >= \''+startTime+'\' AND "CreatedTime" <= \''+endTime+'\';'
        data = dictdata(sqlBudget)
        if len(data) !=0:
            apply_cost = eval(price)*int(qty)
            cash = 0
            if money_type != 'CNY':
                sqlExchange = ' SELECT "ExchangeRate" FROM "ExchangeRate" WHERE "CurrencyTo"=\'CNY\' AND "CurrencyFrom" = \'' + money_type + '\' AND "IsActivated" =\'true\' ORDER BY "UpdatedTime" DESC'
                apply_rate = dictdata(sqlExchange)
                if len(apply_rate) !=0:
                    apply_cost = apply_cost*apply_rate[0]['ExchangeRate']
                else:
                    apply_cost = 0
            else:
                apply_cost = apply_cost
            for i in range(0,len(data)):
                sqlExchange = ' SELECT "ExchangeRate" FROM "ExchangeRate" WHERE "CurrencyTo"=\'CNY\' AND "CurrencyFrom" = \''+data[i]['Currency']+'\' AND "IsActivated" =\'true\' ORDER BY "UpdatedTime" DESC'
                rate = dictdata(sqlExchange)
                if len(rate) !=0:
                    cash += rate[0]['ExchangeRate']*data[i]['UnitPrice']*data[i]['Quantity']
                else:
                    cash += 0
            # get Fee limit
            # sqlFee = ' SELECT "LimitCost" FROM "FeeLimit" WHERE "DepartmentId"= \'' + str(DepartId) + '\'  AND "AccountTitleId" = \'' + str(AccountId) + '\' AND "IsActivated" =\'true\' ORDER BY "UpdatedTime" DESC'
            # feefee = dictdata(sqlFee)
            if len(feefee) !=0:
                feefee =feefee[0]['LimitCost']
                leave_cost = feefee-cash
                if apply_cost > leave_cost:
                    return params_error(message="Form over budget")
                else:
                    return method(self,request)
            else:
                #  if it had't no limit cash and we no need to check this limit;
                return method(self, request)
        else:
            return method(self,request)

    return check

# merger Form Fee limit functions define        (类别："PurchaseType",单价："UnitPrice",数量："Quantity",单位："Unit",币种："Currency",部门："Department" ,"Status":'Approve' )
def MergerFeeLimit(method):
    def check(request):

        now = datetime.now()
        startTime = "%s-%s-01 00:00:00" % (now.year,now.month)
        endTime = "%s-%s-%s 23:59:59" % (now.year,now.month ,calendar.monthrange(int(now.year), int(now.month))[1])
        ''' 
            get all Status is Approve data and data info include 
            (class："PurchaseType",price："UnitPrice",mount："Quantity",unit："Unit",currency："Currency",department："Department" ,"Status":'Approve' )
        '''

        ids = tuple(request.POST.getlist('ids[]',''))
        sqlMerger = ' SELECT "UnitPrice","Quantity","Currency","DepartmentId","AccountTitleId" FROM "BudgetCodeForm" WHERE "Id" IN  '+str(ids)
        data = dictdata(sqlMerger)
        for i in range(0,len(data)):
            sqlExchange = ' SELECT "ExchangeRate" FROM "ExchangeRate" WHERE "CurrencyTo"=\'CNY\' AND "CurrencyFrom" = \'' + data[i]['Currency'] + '\' AND "IsActivated" =\'true\' ORDER BY "UpdatedTime" DESC'
            rate = dictdata(sqlExchange)
            if len(rate) != 0:
                rate = rate[0]['ExchangeRate']
            else:
                rate = 1
            data[i]['apply_cost']=rate*data[i]['UnitPrice']*data[i]['Quantity']
        # for data to tidy and sort different partment and account make deal with [{''},{},{}]
        dataSermial = []
        data2 = []
        for item in data:
            _items ={"DepartmentId":item["DepartmentId"],"AccountTitleId":item["AccountTitleId"]}
            try:
                indexNum = dataSermial.index(_items)
                data2[indexNum]['apply_cost'] = data2[indexNum]['apply_cost']+item['apply_cost']
            except:
                dataSermial.append(_items)
                data2.append(item)

        for k in range(0,len(data2)):
            #check if it had partment and account  limit for this limit
            sqlFee = ' SELECT "LimitCost","LimitPeriod" FROM "FeeLimit" WHERE "DepartmentId"= \'' + str(data2[k]['DepartmentId']) + '\'  AND "AccountTitleId" = \'' + str(data2[k]['AccountTitleId']) + '\' AND "IsActivated" =\'true\' ORDER BY "UpdatedTime" DESC'
            feefee = dictdata(sqlFee)
            if len(feefee) !=0:
                if len(feefee) != 0 and feefee[0]['LimitPeriod'] == "month":
                    startTime = "%s-%s-01 00:00:00" % (now.year, now.month)
                    endTime = "%s-%s-%s 23:59:59" % (
                    now.year, now.month, calendar.monthrange(int(now.year), int(now.month))[1])
                if len(feefee) != 0 and feefee[0]['LimitPeriod'] == "year":
                    startTime = "%s-01-01 00:00:00" % (now.year)
                    endTime = "%s-12-%s 23:59:59" % (now.year, calendar.monthrange(int(now.year), 12)[1])
                if len(feefee) != 0 and feefee[0]['LimitPeriod'] == "week":
                    import datetime as da
                    monday, sunday = da.date.today(), da.date.today()
                    one_day = da.timedelta(days=1)
                    while monday.weekday() != 0:
                        monday -= one_day
                    while sunday.weekday() != 6:
                        sunday += one_day
                    startTime = "%s 00:00:00" % (str(monday))
                    endTime = "%s 23:59:59" % (str(sunday))
            #check this monthy status approved ang process ang this department and account get all data and check count cash
                cash = 0
                sqlBudget = ' SELECT "UnitPrice","Quantity","Currency" FROM "BudgetCodeForm" WHERE "DepartmentId" = \'' + str(data2[k]['DepartmentId']) + '\' AND "AccountTitleId" = \'' + str(data2[k]['AccountTitleId']) + '\''
                sqlBudget += ' AND ( "Status" =\'Approve\' OR "Status" =\'Process\' ) AND "CreatedTime" >= \'' + startTime + '\' AND "CreatedTime" <= \'' + endTime + '\';'
                data_approve = dictdata(sqlBudget)
                if len(data_approve) !=0:
                    for i in range(0,len(data_approve)):
                        sqlExchange = ' SELECT "ExchangeRate" FROM "ExchangeRate" WHERE "CurrencyTo"=\'CNY\' AND "CurrencyFrom" = \''+data_approve[i]['Currency']+'\' AND "IsActivated" =\'true\' ORDER BY "UpdatedTime" DESC'
                        approve_rate = dictdata(sqlExchange)
                        if len(approve_rate) !=0:
                            cash += approve_rate[0]['ExchangeRate']*data_approve[i]['UnitPrice']*data_approve[i]['Quantity']
                        else:
                            cash += 0
                feefee = feefee[0]['LimitCost']
                leave_cost = feefee - cash
                if data2[k]['apply_cost'] > leave_cost:
                    return params_error(message="Form over budget")
        return method(request)
    return check