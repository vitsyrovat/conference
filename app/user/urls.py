# from rest_framework.routers import DefaultRouter
from django.urls import path
from user import views

app_name = 'user'

urlpatterns = [
    path('create/', views.UserCreate.as_view(), name='create'),
]
