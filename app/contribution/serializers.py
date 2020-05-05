from rest_framework import serializers

from core.models import Contribution


class ContributionSerializer(serializers.ModelSerializer):
    """Serializer for the contribution's management"""
    class Meta:
        model = Contribution
        fields = ['title','presentation_form']
