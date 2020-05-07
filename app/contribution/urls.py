from django.urls import path, include
from rest_framework.routers import DefaultRouter

from contribution import views

app_name = 'contribution'

router = DefaultRouter()
router.register('contribution', views.ContributionViewSet)

urlpatterns = [
    path('', include(router.urls))
]

# urlpatterns = [
#     path('create/', views.CreateContribution.as_view(), name='create'),
# ]
