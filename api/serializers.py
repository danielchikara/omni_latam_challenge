
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework import serializers
from django.core import exceptions
from api.utils import get_or_none
from api.models import *


class ClientRegisterSerializer(serializers.Serializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)
    password_confirmation = serializers.CharField(required=True)

    def validate(self, data):
        email = data.get("email", None)
        password = data.get("password", None)
        password_confirmation = data.get("password_confirmation", None)
        first_name = data.get("first_name", None)
        last_name = data.get("last_name", None)
        user = get_or_none(User, email=email)
        if user:
            msg = "Este correo electrónico ya está en uso."
            raise exceptions.ValidationError(msg)
        if password != password_confirmation:
            msg = "Las contraseñas no coinciden"

        else:
            user = User.objects.create_user(first_name=first_name, last_name=last_name,
                                            email=email, password=password)
            user.save()
            data["user"] = user
        return data


class ClientUpdateSerializer(serializers.Serializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)

    def update(self, instance, validated_data):
        first_name = validated_data.get("first_name", '')
        last_name = validated_data.get("last_name", '')
        user = instance
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        return instance


class UserClientSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email', 'id', 'first_name', 'last_name')


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        email = data.get("email", "")
        password = data.get("password", "")
        if email and password:
            user = authenticate(email=email, password=password)
            if user:
                data["user"] = user
            else:
                msg = 'Este usuario y contraseña no coinciden, intenta de nuevo.'
                raise exceptions.ValidationError(msg)
        else:
            msg = 'Se deben enviar el email y la contraseña.'
            raise exceptions.ValidationError(msg)
        return data
