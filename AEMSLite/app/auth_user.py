from django.http import HttpResponseRedirect,HttpResponse
from datetime import datetime
# from app import restful
# from app.login.views import Logout
from django.shortcuts import render,redirect
from app.login.models import User
from app.restful import params_error
def auth(func):
    def auth_func(request):
        now_time = datetime.now()
        last_access_time_str = request.COOKIES.get('LAST_ACCESS_TIME')
        
        last_access_time = datetime.strptime(last_access_time_str, '%Y-%m-%d %H:%M:%S')
        # if user did not operate web for more than 30 minutes, need logout
        passed_time = now_time - last_access_time
        if passed_time.total_seconds() > 10:
            return  params_error(message="/login/")
        # else:
        #     return redirect("/index/")

        # user_Id = request.session.get('user_Id','')
        # user_Role = request.session.get('user_role','')
        # if user_Id > 0 and len(user_Role) > 0: #判断是否登录
        #     try:
        #         user = User.objects.get(Id=user_Id)
        #         if user.Role == user_Role:
        #           return func(request)
        #         else:
        #             # Logout(request)
        #             # return render(request, "./AEMSLite/templates/login/login.html")
        #             # return render(request, "login/login.html")
        #             return restful.params_error(data={'user_Id': user_Id, 'user_Role': user_Role})
        #             # return HttpResponseRedirect("/login/")
        #     except Exception as e:
        #         return restful.params_error(data={'e': repr(e)})
        # else:#如果没登录就跳转到登录界面
        #     return restful.params_error(data={'user_Id':user_Id,'user_Role':user_Role})
        return func(request)
    return auth_func