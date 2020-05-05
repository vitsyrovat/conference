from rest_framework.generics import CreateAPIView

# Create your views here.
from contribution.serializers import ContributionSerializer


class CreateContribution(CreateAPIView):
    serializer_class = ContributionSerializer
