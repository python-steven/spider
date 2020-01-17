from django.urls import path

from .views import UserData,modify_user,CustomerInfo,DepartmentInfo,del_user,modify_password\
    ,modify_customer,del_customer,delete_department,modify_department,Location_list,Location_add\
	,Location_delete,Location_edit,Model_add,Model_info,Model_modify,Model_delete,Subjects_add\
	,Subjects_info,Subjects_modify,Subjects_delete,Rate_info,Rate_add,Rate_modify,Rate_delete\
	,Fee_info,FeeAdd_limit,Fee_detail,FeeModify_limit,FeeDel_limit

app_name ="management"

urlpatterns = [
	path("user-data/",UserData.as_view(),name="UserData"),
	path("user-modify/",modify_user,name="modify_user"),
	path("user-delete/",del_user,name="del_user"),
	path("password-modify/",modify_password,name="modify_password"),
	path("Customer-Info/",CustomerInfo.as_view(),name="CustomerInfo"),
	path("Customer-modify/",modify_customer,name="modify_customer"),
	path("Customer-delete/",del_customer,name="del_customer"),
	path("Department-Info/",DepartmentInfo.as_view(),name="DepartmentInfo"),
	path("Department-modify/",modify_department,name="modify_department"),
	path("Department-delete/",delete_department,name="delete_department"),
	path("Location-list/",Location_list,name="Location_list"),
	path("Location-add/",Location_add,name="Location_add"),
	path("Location-delete/",Location_delete,name="Location_delete"),
	path("Location-edit/",Location_edit,name="Location_edit"),

	path("Model-add/",Model_add,name="Model_add"),
	path("Model-info/",Model_info,name="Model_info"),
	path("Model-modify/",Model_modify,name="Model_modify"),
	path("Model-delete/",Model_delete,name="Model_delete"),

	path("Subjects-add/",Subjects_add,name="Subjects_add"),
	path("Subjects-info/",Subjects_info,name="Subjects_info"),
	path("Subjects-modify/",Subjects_modify,name="Subjects_modify"),
	path("Subjects-delete/",Subjects_delete,name="Subjects_delete"),


	path("Rate-info/",Rate_info,name="Rate_info"),
	path("Rate-add/",Rate_add,name="Rate_add"),
	path("Rate-modify/",Rate_modify,name="Rate_modify"),
	path("Rate-delete/",Rate_delete,name="Rate_delete"),


	path("Fee-detail-info/",Fee_detail,name="Fee_detail"),
	path("Fee-Depart-Account-info/",Fee_info,name="Fee_info"),
	path("Fee-Limit-Add/",FeeAdd_limit,name="FeeAdd_limit"),
	path("Fee-Limit-Modify/",FeeModify_limit,name="FeeModify_limit"),
	path("Fee-Limit-del/",FeeDel_limit,name="FeeDel_limit"),



]
