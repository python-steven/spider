from django.urls import path

from .views import maintain_equipment_info,maintain_setup_info,maintain_setup_by_pn\
	,maintain_query_part_name_data,maintain_query_operation\
	,maintain_query_maintain,maintain_add_equipment,maintain_add_equipment_ex\
	,maintain_equipment_log,maintain_query_log,maintain_add_equipment_log\
	,maintain_query_my_log,maintain_modify_log,maintain_delete_log,maintain_query_SN,maintain_location,setup_maintainer

app_name ="maintain"

urlpatterns = [
	path("maintain-equipment-info/",maintain_equipment_info.as_view(),name="maintain_equipment_info"),
	path("maintain-setup-info/",maintain_setup_info,name="maintain_setup_info"),
	path("maintain-setup-by-pn/",maintain_setup_by_pn,name="maintain_setup_by_pn"),
	path("maintain-query-partname-data/",maintain_query_part_name_data,name="maintain_query_part_name_data"),
	path("maintain-query-SN/",maintain_query_SN,name="maintain_query_SN"),
	path("maintain-query-operation/",maintain_query_operation,name="maintain_query_operation"),
	path("maintain-query-maintain/",maintain_query_maintain,name="maintain_query_maintain"),

	path("maintain-location/",maintain_location,name="maintain_location"),
	path("maintain-add-equipment/",maintain_add_equipment,name="maintain_add_equipment"),
	path("maintain-add-equipment-ex/",maintain_add_equipment_ex,name="maintain_add_equipment_ex"),
	path("maintain-equipment-log/",maintain_equipment_log,name="maintain_equipment_log"),
	path("maintain-query-log/",maintain_query_log,name="maintain_query_log"),
	path("maintain-add-equipment-log/",maintain_add_equipment_log,name="maintain_add_equipment_log"),
	path("maintain-query-my-log/",maintain_query_my_log,name="maintain_query_my_log"),
	path("maintain-modify-log/",maintain_modify_log,name="maintain_modify_log"),
	path("maintain-delete-log/",maintain_delete_log,name="maintain_delete_log"),
	path("setup-maintainer/",setup_maintainer,name="setup_maintainer"),
]
