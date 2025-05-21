from django.urls import path
from . import views

app_name = 'services'

urlpatterns = [
    # Expert authentication
    path('login/', views.expert_login, name='expert_login'),
    path('logout/', views.expert_logout, name='expert_logout'),

    # Expert dashboard and work management
    path('dashboard/', views.expert_dashboard, name='expert_dashboard'),
    path('request/<int:request_id>/', views.request_detail, name='request_detail'),
    path('start/<int:request_id>/', views.start_work, name='start_work'),
    path('complete/<int:request_id>/', views.complete_work, name='complete_work'),
]