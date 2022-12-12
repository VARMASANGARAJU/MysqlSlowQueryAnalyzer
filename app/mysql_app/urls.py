from django.urls import path
from .views import auth, fetch


urlpatterns = [
    path('login/',auth.loginPage, name='login'),
    path('logout/',auth.logoutUser, name='logout'),
    path('dashboard/',auth.dashboard, name='dashboard'),

    path('view_instances/',auth.view_instances, name='view_instances'),
    path('view_logs/<str:instance_id>/',auth.view_logs, name='view_logs'),
]