"""
URL configuration for baseball_app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from .import views
from .views import calendar_view

 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('user.urls')),
    path('calendar/', calendar_view, name='calendar'),
    path('add_event/', views.add_event, name='add_event'),
    path('event/<int:event_id>/', views.event_details, name='event_details'),
    path('events/data/', views.get_events, name='events_data'),
    path('event/delete/<int:event_id>/', views.delete_event, name='delete_event'),
    path('event/edit/<int:event_id>/', views.edit_event, name='edit_event'),

]


 





















