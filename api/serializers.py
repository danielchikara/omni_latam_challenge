
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework import serializers
from django.core import exceptions
from api.utils import get_or_none
from api.models import *


class TokenSerializer(serializers.Serializer):
    token = serializers.CharField()

    def validate(self, data):
        key_token = data.get("token", "")
        if key_token:
            token = get_or_none(Token, key=key_token)
            if token:
                data["user"] = token.user
            else:
                msg = 'El token es inválido.'
                raise exceptions.ValidationError(msg)
        else:
            msg = 'Se debe enviar el token.'
            raise exceptions.ValidationError(msg)
        return data


class ClientRegisterSerializer(serializers.Serializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)

    def validate(self, data):
        email = data.get("email", None)
        password = data.get("password", None)
        first_name = data.get("first_name", None)
        last_name = data.get("last_name", None)
        user = get_or_none(User, email=email)
        print(user,"asdasdadada")
        if user:
            msg = "Este correo electrónico ya está en uso."
            raise exceptions.ValidationError(msg)
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
