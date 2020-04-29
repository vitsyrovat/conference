from django.contrib.auth import get_user_model, password_validation
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
from django.contrib.auth import authenticate


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


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user token authtentication"""
    email = serializers.CharField(label=_("Email"))
    password = serializers.CharField(
        label=_("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        """Validate and authtenticate user"""
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(
                request=self.context.get('request'),
                username=email,
                password=password
            )
            if not user:
                msg = _('Unable to authtenticate with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "email" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs
