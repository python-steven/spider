from django.shortcuts import render, redirect
# from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from app.login.models import User,Department,Customer,BudgetCodeForm,PartItem,PartItemResult,MaintenanceLog,Configuration
from app.login.views import Update_User_IsActivated
from django.views.generic.base import View
from django.db import connection
from django.http import HttpResponseRedirect,HttpResponse
from app import restful,mail
from datetime import datetime,timedelta,date
from django.conf import settings
import random
import string
import os
import time
from openpyxl import load_workbook,Workbook
import json
UpdatedTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# 用户管理页面的数据的获取和增加用户：
class UserData(View):
    @csrf_exempt
    def get(self, request):
        try:
            page = int(request.GET.get('page'))
            number = request.GET.get('num')
            dict_data = {}
            sql1 = 'SELECT "User"."Id","EmployeeId","Name","Department","Email","Role" FROM "User" INNER JOIN ' \
                   '"Department" ON "User"."DepartmentId" = "Department"."Id" WHERE "User"."IsActivated"=True'
            sql2 = 'select count(*) FROM "User" INNER JOIN "Department" ON "User"."DepartmentId" = "Department"' \
                   '."Id" WHERE "User"."IsActivated"=True'
            cur = connection.cursor()
            cur.execute(sql2)
            count = cur.fetchall()  # 数量的总数
            if number == 'All':
                cur = connection.cursor()
                cur.execute(sql1)
                data = cur.fetchall()
                dict_data['data'] = data
                dict_data['page_count'] = count[0][0]
                return restful.ok(data=dict_data)
            if number != "All":
                number = int(number)
                count_page = count[0][0] // int(number)  # 总数除以一页显示多少条，得到总的页数
                if count[0][0] % number > 0:
                    count_page += 1
                if page <= count_page:
                    sql1 = sql1 + ' order by "Name" limit ' + str(number) + ' offset ' + str(page - 1)
                    cur = connection.cursor()
                    cur.execute(sql1)
                    data = cur.fetchall()
                    dict_data['data'] = data
                    dict_data['page_count'] = count_page
                    return restful.ok(data=dict_data)
                else:
                    return restful.params_error(message="it had no other pages")
        except Exception as e:
            return restful.params_error(message=repr(e))
    # 增加用户的功能
    @csrf_exempt
    def post(self, request):
        password = genPassword()
        employee_id = request.POST['userid']
        name = request.POST['username']
        email = request.POST['mail']
        role = request.POST['role']
        department = request.POST['department']
        updated_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        created_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        try:
            user = User.objects.exclude(EmployeeId=employee_id).filter(Email=email)
            user_employee = User.objects.get(EmployeeId=employee_id)
            if len(user) != 0:
                return restful.params_error(message="user email had used")
            if len(user) == 0 and user_employee:
                User.objects.filter(EmployeeId=employee_id).update(IsActivated=True, Name=name, Password=password
                                                                   , Email=email, Role=role, CreatedTime=created_time
                                                                   , UpdatedTime=updated_time)
                subject = "Inform Your New Password in AEMS Lite System"
                content = """
<pre>
Dear """ + str(name) + """,
    AEMS Lite System has automatically generated a new password for you:
    Your Account is: """ + employee_id + """
    Your Password is:""" + password + """
    Please use your e-mail as user name and this password to login AEMSLite system. After you login, 
    please remember to change it.
    <a href="http://10.41.95.106:90/login">Login AEMS Lite System</a>

   ---------------------------------------------------------------------------------------
    THIS EMAIL WAS SENT BY AEMS Lite SERVER AUTOMATICALLY. PLEASE DON'T DIRECTLY REPLY!!!
</pre>
 """

                mail.sendmail([email, ], content, subject)
                return restful.ok(message="user add success")
        except:
            try:
                user = User.objects.get(Name=name)
                if user:
                    return restful.params_error(message='user name had used')
            except:
                try:
                    user = User.objects.get(Email=email)
                    if user:
                        return restful.params_error(message="user email had used")
                except:
                    try:
                        department_ob = Department.objects.get(Department=department)
                        department_id = department_ob.Id
                        User.objects.create(EmployeeId=employee_id, Name=name, Password=password, Email=email,
                                            Role=role, CreatedTime=created_time, UpdatedTime=updated_time,
                                            DepartmentId=department_id)
                        subject = "Inform Your New Password in AEMS Lite System"
                        content = """
<pre>
Dear """ + str(name) + """,
    AEMS Lite System has automatically generated a new password for you:
    Your Account is: """ + employee_id + """
    Your Password is:""" + password + """
    Please use your e-mail as user name and this password to login AEMSLite system. After you login, 
    please remember to change it.
    <a href="http://10.41.95.106:90/login">Login AEMS Lite System</a>

   ---------------------------------------------------------------------------------------
    THIS EMAIL WAS SENT BY AEMS Lite SERVER AUTOMATICALLY. PLEASE DON'T DIRECTLY REPLY!!!
</pre>
"""

                        mail.sendmail([email, ], content, subject)
                        return restful.ok(message='User created success')
                    except:
                        User.objects.create(EmployeeId=employee_id, Name=name, Password=password, Email=email,
                                            Role=role, CreatedTime=created_time, UpdatedTime=updated_time)
                        subject = "Inform Your New Password in AEMS Lite System"
                        content = """
<pre>
Dear """ + str(name) + """,
    AEMS Lite System has automatically generated a new password for you:
    Your Account is: """ + employee_id + """
    Your Password is:""" + password + """
    Please use your e-mail as user name and this password to login AEMSLite system. After you login, 
    please remember to change it.
    <a href="http://10.41.95.106:90/login">Login AEMS Lite System</a>

   ---------------------------------------------------------------------------------------
    THIS EMAIL WAS SENT BY AEMS Lite SERVER AUTOMATICALLY. PLEASE DON'T DIRECTLY REPLY!!!
</pre>
 """
                        mail.sendmail([email, ], content, subject)
                        return restful.ok(message='User add success')

# 随机生成密码的函数
def genPassword(length=8, chars=string.digits + string.ascii_letters):
    return ''.join(random.sample(chars * 10, 8))

# 修改用户的相关信息的函数
@csrf_exempt
def modify_user(request):
    if request.method == "POST":
        id = int(request.POST['id'])
        username = request.POST['username']
        department = request.POST['department']
        role = request.POST['role']
        session_id = request.session['user_Id']
        user_obj = User.objects.get(Id=session_id)
        if user_obj.Role == "admin":
            try:
                user = User.objects.exclude(Id=id).get(Name=username)
                if user:
                    return restful.params_error(message='user name had used')
            except:
                try:
                    modify_department = Department.objects.get(Department=department)
                    department_id = modify_department.Id
                    User.objects.filter(Id=id).update(Name=username, Role=role, UpdatedTime=UpdatedTime
                                                      , DepartmentId=department_id)
                    return restful.ok(message="user modify success")
                except:
                    User.objects.filter(Id=id).update(Name=username, Role=role, UpdatedTime=UpdatedTime)
                    return restful.ok(message='User modify success')
        else:
            return restful.params_error(message="please connect admin")

# 删除用户的函数
@csrf_exempt
def del_user(request):
    if request.method == "POST":
        try:
            name = request.POST['name']
            session_id = request.session['user_Id']
            user_obj = User.objects.get(Id=session_id)
            if user_obj.Role == "admin":
                budget_code = BudgetCodeForm.objects.exclude(Status="Approve").filter(Pic=name)
                if len(budget_code) != 0:
                    return restful.params_error(message="User had using can't delete")
                budget_code2 = BudgetCodeForm.objects.exclude(Status="Approve").filter(Signer=name)
                if len(budget_code2) != 0:
                    return restful.params_error(message="User had using can't delete")
                else:
                    user = User.objects.get(Name=name)
                    user.IsActivated = False
                    user.save()
                    return restful.ok(message='delete success')
        except:
            return restful.params_error(message="please connect admin")

# 修改用户密码
@csrf_exempt
def modify_password(request):
    if request.method == "POST":
        OldPwd = request.POST['OldPwd']
        NewPwd = request.POST['NewPwd']
        session_id = request.session['user_Id']
        user_obj = User.objects.get(Id=session_id)
        if user_obj.Password == OldPwd:
            User.objects.filter(Id=session_id).update(Password=NewPwd)
            return restful.ok(message='modify password success')
        else:
            return restful.params_error(message="The original password is wrong")

# 增加客户和获取客户的信息
class CustomerInfo(View):
    @csrf_exempt
    def get(self, request):
        try:
            page = int(request.GET.get('page'))
            number = request.GET.get('num')
            dict_data ={}
            count = Customer.objects.exclude(IsActivated='False').count()
            if number == "All" :
                customerinfo = Customer.objects.exclude(IsActivated='False')
                customerinfo = customerinfo.values()
                customerinfo = list(customerinfo)
                dict_data['data'] =customerinfo
                dict_data['page_count'] =count
                return restful.ok(data=dict_data)
            if number != "All":
                number = int(number)
                page_num = count // number  # 总共多少页
                if count % number > 0:
                    page_num = page_num + 1
                if page_num >= page:
                    customerinfo = Customer.objects.exclude(IsActivated='False')[(page-1)*number:number*page]
                    customerinfo = customerinfo.values()
                    customerinfo = list(customerinfo)
                    dict_data['data'] = customerinfo
                    dict_data['page_count'] = page_num
                    return restful.ok(data=dict_data)
                else:
                    return restful.params_error(message="it had no other pages")
        except Exception as e:
            return restful.params_error(message=repr(e))
    @csrf_exempt
    def post(self, request):
        customer = request.POST['customer_val']
        updatedtime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        try:
            customer_ob = Customer.objects.get(Customer=customer)
            if customer_ob.Id and customer_ob.IsActivated == False:
                customer_ob.IsActivated = True
                customer_ob.save()
                return restful.ok(message="Customer add success")
            else:
                return restful.params_error(message="Customer had exist")
        except:
            Customer.objects.create(Customer=customer, UpdatedTime=updatedtime)
            return restful.ok(message='Customer add success')

# 修改客户数据
@csrf_exempt
def modify_customer(request):
    if request.method == "POST":
        customer = request.POST['customer_name']
        customer_id = request.POST['customer_id']
        try:
            customer_ob = Customer.objects.exclude(Id=customer_id).get(Customer=customer)
            if customer_ob:
                return restful.params_error(message="Customer had can't exist")
        except:
            Customer.objects.filter(Id=customer_id).update(Customer=customer, UpdatedTime=UpdatedTime)
            return restful.ok(message="customer had modify")

# 删除客户数据
@csrf_exempt
def del_customer(request):
    if request.method == "POST":
        customer = request.POST['del_nm']
        try:
            budget_code = BudgetCodeForm.objects.exclude(Status="Approve").filter(Customer=customer)
            if len(budget_code) != 0:
                return restful.params_error(message="customer had using can't delete")
            else:
                cus = Customer.objects.get(Customer=customer)
                cus.IsActivated = False
                cus.save()
                return restful.ok(message="Customer delete success")
        except:
            return restful.params_error(message='please connect admin')

# 增加部门和获取部门数据
class DepartmentInfo(View):
    @csrf_exempt
    def get(self, request):
        try:
            page = int(request.GET.get('page'))
            number = request.GET.get('num')
            dict_data = {}
            count = Department.objects.exclude(IsActivated='False').count()
            if number == "All":
                department_info = Department.objects.exclude(IsActivated='False')
                department_info = list(department_info.values())
                dict_data['data'] = department_info
                dict_data['page_count'] = count
                return restful.ok(data=dict_data)
            if number != "All":
                number = int(number)
                page_num = count // number  # 总共多少页
                if count % number > 0:
                    page_num = page_num + 1
                if page_num >= page:
                    department_info = Department.objects.exclude(IsActivated='False')[(page-1)*number:number*page]
                    department_info = list(department_info.values())
                    dict_data['data'] = department_info
                    dict_data['page_count'] = page_num
                    return restful.ok(data=dict_data)
                else:
                    return restful.params_error(message="it had no other pages")
        except Exception as e:
            return restful.params_error(message=repr(e))
    @csrf_exempt
    def post(self, request):
        department = request.POST['department']
        updatedtime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        try:
            part = Department.objects.get(Department=department)
            if part.Id and part.IsActivated == False:
                part.IsActivated = True
                part.save()
                return restful.ok(message="Department create success")
            else:
                return restful.params_error(message="Department had Exist")
        except:
            Department.objects.create(Department=department, UpdatedTime=updatedtime)
            return restful.ok(message='Department create success')

# 修改部门数据
@csrf_exempt
def modify_department(request):
    if request.method == "POST":
        depart = request.POST['modifyPartName']
        depart_id = request.POST['modifyPartId']
        try:
            depart_ob = Department.objects.exclude(Id=depart_id).get(Department=depart)
            if depart_ob:
                return restful.params_error(message="Customer had used")
        except:
            Department.objects.filter(Id=depart_id).update(Department=depart, UpdatedTime=UpdatedTime)
            return restful.ok(message="Department had modify")

# 删除部门数据
@csrf_exempt
def delete_department(request):
    if request.method == "POST":
        depart_name = request.POST['delPart']
        try:
            budget_code = BudgetCodeForm.objects.exclude(Status="Approve").filter(Department=depart_name)
            if len(budget_code) != 0:
                return restful.params_error(message="department had using can't delete")
            else:
                depart = Department.objects.get(Department=depart_name)
                depart.IsActivated = False
                depart.save()
                return restful.ok(message='department delete success')
        except:
            return restful.params_error(message='please connect admin')