from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page, name='home'),
    path('chat/', views.chat_page, name='chat'),
    path('dashboard/', views.dashboard_page, name='dashboard'),
    path('api/vegans/', views.VeganUsersView.as_view(), name='api-vegans'),
    path('api/chat/', views.chat_api, name='chat_api'),
]