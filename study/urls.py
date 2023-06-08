from django.urls import path
from django.http import HttpResponse
from . import views 



urlpatterns = [
    path('login/', views.LoginPage.as_view(), name="login"),
    path('register/', views.RegisterPage.as_view(), name="register"),
    path('logout/', views.LogoutUser.as_view(), name="logout"),
    path('', views.Home.as_view(), name="home"),
    path('room/<str:pk>/', views.GetRoom.as_view(), name="room"),
    path('profile/<str:pk>/', views.UserProfile.as_view(), name="user-profile"),
    path('create-room/', views.CreateRoom.as_view(), name="create-room"),
    path('update-room/<str:pk>/', views.UpdateRoom.as_view(), name="update-room"),
    path('delete-room/<str:pk>/', views.DeleteRoom.as_view(), name="delete-room"),
    path('delete-message/<str:pk>/', views.DeleteMessage.as_view(), name="delete-message"),
    path('update-user/', views.UpdateUser.as_view(), name="update-user"),
    path('topics/', views.TopicsPage.as_view(), name="topics"),
    path('activity/', views.ActivityPage.as_view(), name="activity"),

]