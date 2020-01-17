from django.urls import path

from .views import analysis_equipment_info,analysis_data,analysis_setup_data\
    ,analysis_setup_value,analysis_query_data,analysis_query_info,analysis_tab_data\
	,analysis_query_tab_info,analysis_delete_data,analysis_visul_data,analysis_vi_part,analysis_upload_file_excle


app_name ="analysis"

urlpatterns = [
	path("analysis-equipment-info/",analysis_equipment_info.as_view(),name="analysis_equipment_info"),
	path("analysis-data/",analysis_data,name="analysis_data"),
	path("analysis-setup-data/",analysis_setup_data,name="analysis_setup_data"),
	path("analysis-setup-value/",analysis_setup_value,name="analysis_setup_value"),
	path("analysis-query-data/",analysis_query_data,name="analysis_query_data"),
	path("analysis-query-info/",analysis_query_info,name="analysis_query_info"),
	path("analysis-tab-data/",analysis_tab_data,name="analysis_tab_data"),
	path("analysis-query-tab-info/",analysis_query_tab_info,name="analysis_query_tab_info"),
	path("analysis-delete-data/",analysis_delete_data,name="analysis_delete_data"),
	path("analysis-visual-data/",analysis_visul_data,name="analysis_visual_data"),
	path("analysis-vi-part/",analysis_vi_part,name="analysis_vi_part"),
	path("analysis-upload-file-excle/",analysis_upload_file_excle,name="analysis_upload_file_excle"),
]