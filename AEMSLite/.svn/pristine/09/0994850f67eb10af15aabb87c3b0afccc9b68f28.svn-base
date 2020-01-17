from django.shortcuts import render
from app.login.models import User
from django.views.generic import View
from app import restful
from django.views.decorators.csrf import csrf_exempt




# Create your views here.
class MangeMent(View):
    @csrf_exempt
    def get(self,request):
        username = request.session['username']
        user = User.objects.get(UserName=username)
        context ={
            'user': user,
        }

        return render(request,"./index/main.html",context=context)
