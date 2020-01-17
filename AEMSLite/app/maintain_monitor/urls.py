from django.urls import path

from .views import maintain_monitor_info, maintain_query, maintain_record, maintain_monitor_visual\
	,setup_range_before

app_name ="maintain_monitor"

urlpatterns = [
	path("maintain-monitor-info/",maintain_monitor_info.as_view(),name="maintain_monitor_info"),
	path("setup-range-before/",setup_range_before,name="setup_range_before"),
	path("maintain-query/",maintain_query,name="maintain_query"),
	path("maintain-monitor-visual/",maintain_monitor_visual,name="maintain_monitor_visual"),
	path("maintain-record/",maintain_record,name="maintain_record"),

]