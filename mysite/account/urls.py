from django.urls import path
from . import views


urlpatterns = [
    path('', views.home),
	path('register/', views.registerPage, name="register"),
	path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),

    path('home/', views.home, name="home"),

    path('dashboard_professor/', views.dashboard_professor, name="dashboard_professor"),
    path('dashboard_student/', views.dashboard_student, name="dashboard_student"),
    path('create_class/', views.create_class, name='create_class'),
    path('add_class/<str:pk>/', views.add_class, name='add_class'),
    path('remove_class/<str:pk>/', views.remove_class, name='remove_class'),
    path('update_class/<str:pk>/', views.update_class, name='update_class'),
    path('delete_class/<str:pk>/', views.delete_class, name="delete_class"),

]