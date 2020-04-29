from django.contrib.auth import get_user_model, password_validation
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('email', 'password', 'name')
        extra_kwargs = {
            'password': {
                'write_only': True,
                # 'min_length': 8      # this is replaced by validate_password
                }
            }

    # def validate_password(self, value):
    #     if len(value) < 5:
    #         raise serializers.ValidationError(
    #            'Password must have at least 5 characters.')
    #     return value

    def validate_password(self, value):
        try:
            password_validation.validate_password(value)
        except serializers.ValidationError as exception:
            raise serializers.ValidationError(exception)

        return value

    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)
