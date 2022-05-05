from django.contrib.auth import authenticate, get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        min_length=5,
        style={'input_type': 'password'}
    )

    class Meta:
        model = get_user_model()
        fields = ('email', 'password', 'name')

    def create(self, validated_data):
        '''Creates and returns a new user'''
        return get_user_model().objects.create_user(
            **validated_data
        )

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user


class AuthTokenSerializer(serializers.Serializer):
    '''Serializer for the user authentication object'''
    email = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False,
    )

    def validate(self, attrs):
        '''Validate and authenticate user'''
        email = attrs.get('email')
        password = attrs.get('password')
        if email and password:
            user = authenticate(
                request=self.context.get('request'),
                username=email,
                password=password
            )
            if not user:
                msg = _('Incorrect username or password')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Username and password fields are required')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs
