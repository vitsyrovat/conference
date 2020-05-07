from rest_framework import serializers

from core.models import Contribution, Author


class ContributionSerializer(serializers.ModelSerializer):
    """Serializer for the contribution's management"""
    authors = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Author.objects.all()
    )

    class Meta:
        model = Contribution
        fields = ['id', 'title', 'authors', 'presentation_form']
        read_only_fields = ('id',)
