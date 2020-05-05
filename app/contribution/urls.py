from django.urls import path

from contribution import views

app_name = 'contribution'

urlpatterns = [
    path('create/', views.CreateContribution.as_view(), name='create'),
]
