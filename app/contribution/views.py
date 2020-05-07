from rest_framework.viewsets import ModelViewSet
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

# Create your views here.
from contribution import serializers
from core.models import Contribution


class ContributionViewSet(ModelViewSet):
    """Manage Contributions in the db"""
    serializer_class = serializers.ContributionSerializer
    queryset = Contribution.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# class CreateContribution(CreateAPIView):
#     serializer_class = ContributionSerializer
