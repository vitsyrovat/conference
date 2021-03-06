# from rest_framework.routers import DefaultRouter
from django.urls import path
from user import views
# from rest_framework.authtoken import views as authtoken_views

app_name = 'user'

urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('token/', views.CreateTokenView.as_view(), name='token'),
    path('me/', views.ManageUserView.as_view(), name='me'),
]
