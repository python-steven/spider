from django.urls import path

from .views import LoginView,Logout,Retrieve_password

app_name ="login"

urlpatterns = [
	path("",LoginView.as_view(),name="login"),
	# path("timeout_logout/",timeout_logout,name="timeout_logout"),
	# path("force_logout/",force_logout,name="force_logout"),
	path("logout/",Logout,name="logout"),
    path("Retrieve_password/",Retrieve_password,name="Retrieve_password"),

]