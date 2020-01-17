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
            name = request.POST['u_name']
            password = request.POST['u_password']
            user = User.objects.get(Name=name)
            if user:
                if (user.Password == password):
                    if user.IsActivated == False:
                        Update_User_IsActivated(name)

                        request.session['user_Id'] = user.Id
                        request.session.set_expiry(0)
                        return restful.ok()
                    request.session['user_Id'] = user.Id
                    request.session.set_expiry(0)
                    return restful.ok()
                return restful.params_error(message='password error')
            return restful.params_error(message='user error')
        except:
            return restful.params_error(message="username error")
        

#修改用户的激活状态
def Update_User_IsActivated(Name):
    User.objects.filter(Name=Name).update(IsActivated=True)