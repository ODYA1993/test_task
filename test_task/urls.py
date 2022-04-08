from django.urls import path
from test_task import views

urlpatterns = [
    path('', views.calculate, name='home'),
    path('login/', views.LoginUser.as_view(), name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.RegisterUser.as_view(), name='register'),
    path('history/', views.history, name='history'),
    path('details/<str:acc_id>/', views.details, name='details'),
]