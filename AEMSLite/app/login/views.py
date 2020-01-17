from django.shortcuts import render,redirect
from app.login.models import User
from django.views.generic import View
from app import restful,mail
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect,HttpResponse
import string
import random
# Create your views here.
class LoginView(View):
    @csrf_exempt
    def get(self,request):
        return render(request,"./login/login.html")
    @csrf_exempt
    def post(self,request):
        try:
            Employee_email = request.POST['Employee_email']
            password = request.POST['u_password']
            user = User.objects.get(Email=Employee_email)
            if (user.Password == password):
                if user.IsActivated == False:
                    # Update_User_IsActivated(Employee_email)
                    # request.session['user_Id'] = user.Id
                    # request.session.set_expiry(0)
                    # return restful.ok(message="login success")
                    return restful.params_error(message='User no active')
                else:
                    request.session['user_Id'] = user.Id
                    request.session.set_expiry(0)
                    return restful.ok(message="login success")
            return restful.params_error(message='password error')
        except:
            try:
                Employee_email = request.POST['Employee_email']
                password = request.POST['u_password']
                user = User.objects.get(EmployeeId=Employee_email)
                if (user.Password == password):
                    if user.IsActivated == False:
                        # Update_User_IsActivated(Employee_email)
                        # request.session['user_Id'] = user.Id
                        # request.session.set_expiry(0)
                        # return restful.ok(message="login success")
                        return restful.params_error(message='User no active')
                    else:
                        request.session['user_Id'] = user.Id
                        request.session.set_expiry(0)
                        return restful.ok(message="login success")
                return restful.params_error(message='password error')
            except:
                return restful.params_error(message="employee number error")

def Logout(request):
    if request.method == "POST":
        try:
            num = request.POST.get('check_out','')
            if num == '1':
                request.session['user_Id']=None
                request.session.flush()
                return restful.ok(message='logout')
            else:
                return restful.params_error(message="data error",data={'data':num})
        except Exception as e:
            return restful.params_error(message=repr(e))
            
#生成随机密码
def genPwd(length=8, chars=string.digits + string.ascii_letters):
    return ''.join(random.sample(chars * 10, 8))

    
#找回密码
@csrf_exempt
def Retrieve_password(request):
    if request.method == "POST":
        EID = request.POST.get('uname')
        data = {}
        try:
            user = User.objects.get(EmployeeId=EID)
            pwd = genPwd()
            user.Password = pwd
            user.save()
            data['user_name'] = user.Name
            data['new_pwd'] = pwd
            data['employee_id'] = EID
            mail.send_user_forget_pwd_mail([user.Email], data) 
            return restful.ok(message="The password has been sent to your mailbox.")
        except Exception as e:
            return restful.params_error(message="Error")

# def timeout_logout(request):
#     msg = "You don't operate PTS over 30 mins. For security issue you are logout automatically."
#     return render(
#                 request,
#                 "./login/login.html", 
#                 {'warning_msg': msg}
#                 )

# def force_logout(request):
#     msg = "Your info have been updated! For security issue you are logout automatically."
#     return render(
#                 request,
#                 "./login/login.html", 
#                 {'warning_msg': msg}
#                 )

#修改用户的激活状态
def Update_User_IsActivated(Employee_email):
    try:
        User.objects.filter(Email=Employee_email).update(IsActivated=True)
    except:
        User.objects.filter(EmployeeId=Employee_email).update(IsActivated=True)