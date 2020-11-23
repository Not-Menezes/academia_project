from django.urls import path
from . import views


urlpatterns = [
    path('', views.home),
	path('register/', views.registerPage, name="register"),
	path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),

    path('home/', views.home, name="home"),

    path('dashboard_professor/', views.dashboard_professor, name="dashboard_professor"),
    path('create_class/', views.create_class, name='create_class'),
    path('update_class/<str:pk>/', views.update_class, name='update_class'),
]