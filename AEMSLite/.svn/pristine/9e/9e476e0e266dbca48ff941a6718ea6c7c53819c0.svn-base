from django.shortcuts import render,redirect
from app.login.models import User
from django.views.generic import View
from app import restful
from django.views.decorators.csrf import csrf_exempt

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
                    Update_User_IsActivated(Employee_email)
                    request.session['user_Id'] = user.Id
                    request.session.set_expiry(0)
                    return restful.ok(message="login success")
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
                        Update_User_IsActivated(Employee_email)
                        request.session['user_Id'] = user.Id
                        request.session.set_expiry(0)
                        return restful.ok(message="login success")
                    request.session['user_Id'] = user.Id
                    request.session.set_expiry(0)
                    return restful.ok(message="login success")
                return restful.params_error(message='password error')
            except:
                return restful.params_error(message="employee number error")
        

#修改用户的激活状态
def Update_User_IsActivated(Employee_email):
    try:
        User.objects.filter(Email=Employee_email).update(IsActivated=True)
    except:
        User.objects.filter(EmployeeId=Employee_email).update(IsActivated=True)