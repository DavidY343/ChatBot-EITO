from django.urls import path
from django.contrib import admin
from app.views import (
    home_page, chat_page, dashboard_page,
    VeganUsersView, run_simulation, StatisticsView, chat_api
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_page, name='home'),
    path('chat/', chat_page, name='chat'),
    path('dashboard/', dashboard_page, name='dashboard'),

    # APIs
    path('api/vegans/', VeganUsersView.as_view(), name='vegans'),
    path('api/simulate/', run_simulation, name='simulate'),
    path('api/statistics/', StatisticsView.as_view(), name='statistics'),
    path('api/chat/', chat_api, name='chat_api'),
]