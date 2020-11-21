from django.urls import path
from . import views


urlpatterns = [
    path('', views.home),
	path('register/', views.registerPage, name="register"),
	path('login/', views.loginPage, name="login"),
    path('home/', views.loginPage, name="home"),

]