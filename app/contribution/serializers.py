from rest_framework import serializers

from core.models import Contribution, Authorship, Affiliation, Author


class AffiliationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Affiliation
        fields = [
            'id',
            'institution',
            'department',
            'street_address',
            'city',
            'zip_code',
            'country'
        ]
        read_only_fields = ['id']


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'name']
        

class AuthorshipSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()
    affiliation = AffiliationSerializer(many=True)

    class Meta:
        model = Authorship
        fields = [
            'id',
            'author',
            'is_main_author',
            'affiliation',
        ]
        read_only_fields = [
            'id',
        ]


class ContributionSerializer(serializers.ModelSerializer):
    """Serializer for the contribution's management"""
    authorships = AuthorshipSerializer(many=True)

    class Meta:
        model = Contribution
        fields = ['id', 'title', 'presentation_form', 'authorships']
        read_only_fields = ('id',)
