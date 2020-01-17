from django.urls import path

from .views import MonitorEquipment,setup_parameter,monitor_query_info,visual_data\
	,monitor_equipment_change,monitor_equipment_query_next,setup_before


app_name ="NGrate"

urlpatterns = [
	path("monitor-equipment-info/",MonitorEquipment.as_view(),name="MonitorEquipment"),
	path("setup-parameter/",setup_parameter,name="setup_parameter"),
	path("setup-before-info/",setup_before,name="setup_before"),
	path("monitor-query-info/",monitor_query_info,name="monitor_query_info"),
	path("visual-data/",visual_data,name="visual_data"),
	path("monitor-equipment-change/",monitor_equipment_change,name="monitor_equipment_change"),
	path("monitor-equipment-query-next/",monitor_equipment_query_next,name="monitor_equipment_query_next"),
	# path("visual-data-equipment-page/",visual_data_equipment_page,name="visual_data_equipment_page"),
]
