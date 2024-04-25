from rest_framework import routers
from . import views
from django.urls import path, include
from django.views.generic import TemplateView 
from rest_framework import routers


router = routers.DefaultRouter()
router.register('settings', views.AllSettingsViewSet, basename='device-configure')
router.register('active', views.ActiveViewSet)

from django.contrib.auth import views as auth_views


urlpatterns = [
    path("password_reset", views.password_reset_request, name='password_reset'),
    path('reset/<serial_number>/', views.passwordResetConfirm),
] + router.urls