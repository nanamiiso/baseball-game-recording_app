from django .urls import path
from .import views

app_name = 'user'

urlpatterns = [
    path('user_list/', views.user_list, name='user_list'),
    path('index/', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('user_login/', views.user_login, name='login'),
    path('user_logout/', views.user_logout, name='logout'),
    path('settings/', views.settings_view, name='settings'),
    path('change_username/', views.change_username_view, name='change_username'),
    path('change_email/', views.change_email_view, name='change_email'),
    path('change_password/', views.change_password_view, name='change_password'),
]




