from django.urls import path
from .views import webapp_login,webapp_PartItem,webapp_Filtrate
from .views import webapp_ListFiltrate,webapp_MaintainFiltrate,webapp_MaintainCommit,webapp_MaintainList

app_name ="webapp"
urlpatterns = [
    path("login/", webapp_login,name="webapp_login"),                                      #登入的url 的路径

    path("PartItem/", webapp_PartItem,name="webapp_PartItem"),                             #设备列表的默认获取前一周的数据
    path("ListFiltrate/", webapp_ListFiltrate,name="webapp_ListFiltrate"),                 #设备列表的筛选功能的实现的数据

    path("MaintainList/", webapp_MaintainList,name="webapp_MaintainList"),                 #设备保养的获取数据
    path("Filtrate/", webapp_Filtrate,name="webapp_Filtrate"),                             #设备保养的筛选功能的实现的数据的加载数据的实现
    path("MaintainCommit/", webapp_MaintainCommit,name="webapp_MaintainCommit"),           #设备的保养动作的实现的功能的实现

    path("MaintainFiltrate/", webapp_MaintainFiltrate,name="webapp_MaintainFiltrate"),     #保养记录的数据的获取的动作
]