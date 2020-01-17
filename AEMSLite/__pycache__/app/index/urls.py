from django.urls import path

from .views import \
	IndexView,UserData,modify_user,CustomerInfo,DepartmentInfo,del_user,modify_customer,del_customer\
	,delete_department,modify_department,BudgetCodeApply,Budget_info_get,Budget_check_user,Budget_check_principal\
	,Budget_form_save,Budget_merge_order,budget_singing_info,merge_form_sub,merge_signed,merge_signed_finished\
	,merge_statement_detail,budget_modify_type,budget_delete_type,merge_rejected,budget_copy_type,statement_query\
	,budget_modify_unique,budget_code_detail,statement_bring_info,MonitorEquipment,setup_parameter,monitor_query_info\
	,visual_data,maintain_equipment_info,analysis_equipment_info,maintain_setup_info,analysis_data,maintain_setup_by_pn\
	,analysis_setup_data,analysis_setup_value


app_name ="index"

urlpatterns = [
	path("",IndexView.as_view(),name="index"),
	path("user-data/",UserData.as_view(),name="UserData"),
	path("user-modify/",modify_user,name="modify_user"),
	path("user-delete/",del_user,name="del_user"),

	path("Customer-Info/",CustomerInfo.as_view(),name="CustomerInfo"),
	path("Customer-modify/",modify_customer,name="modify_customer"),
	path("Customer-delete/",del_customer,name="del_customer"),

	path("Department-Info/",DepartmentInfo.as_view(),name="DepartmentInfo"),
	path("Department-modify/",modify_department,name="modify_department"),
	path("Department-delete/",delete_department,name="delete_department"),

	path("Budget-code-apply/",BudgetCodeApply.as_view(),name="BudgetCodeApply"),#Budget-code-save/
	path("Budget-form-save/",Budget_form_save,name="Budget_form_save"),
	path("Budget-merge-order/",Budget_merge_order,name="Budget_merge_order"),
	path("budget-modify-type/",budget_modify_type,name="budget_modify_type"),
	path("budget-modify-unique/",budget_modify_unique,name="budget_modify_unique"),
	path("budget-delete-type/",budget_delete_type,name="budget_delete_type"),
	path("budget-copy-type/",budget_copy_type,name="budget_copy_type"),
	path("budget-code-detail/",budget_code_detail,name="budget_code_detail"),

	path("merge-sub/",merge_form_sub,name="merge_form_sub"),
	path("merged-signed/",merge_signed,name="merge_signed"),
	path("merged-rejected/",merge_rejected,name="merge_rejected"),
	path("merged-signed-finished/",merge_signed_finished,name="merge_signed_finished"),
	path("merged-statement-detail/",merge_statement_detail,name="merge_statement_detail"),
	path("statement-query/",statement_query,name="statement_query"),
	path("statement-bring-info/",statement_bring_info,name="statement_bring_info"),

	path("Budget-info-get/",Budget_info_get,name="Budget_info_get"),
	path("Budget-check-user/",Budget_check_user,name="Budget_check_user"),
	path("Budget-check-principal/",Budget_check_principal,name="Budget_check_principal"),
	path("budget-singing-info/",budget_singing_info,name="budget_singing_info"),


	path("monitor-equipment-info/",MonitorEquipment.as_view(),name="MonitorEquipment"),
	path("setup-parameter/",setup_parameter,name="setup_parameter"),
	path("monitor-query-info/",monitor_query_info,name="monitor_query_info"),
	path("visual-data/",visual_data,name="visual_data"),

	path("maintain-equipment-info/",maintain_equipment_info.as_view(),name="maintain_equipment_info"),
	path("maintain-setup-info/",maintain_setup_info,name="maintain_setup_info"),
	path("maintain-setup-by-pn/",maintain_setup_by_pn,name="maintain_setup_by_pn"),


	path("analysis-equipment-info/",analysis_equipment_info.as_view(),name="analysis_equipment_info"),
	path("analysis-data/",analysis_data,name="analysis_data"),
	path("analysis-setup-data/",analysis_setup_data,name="analysis_setup_data"),
	path("analysis-setup-value/",analysis_setup_value,name="analysis_setup_value"),

]
