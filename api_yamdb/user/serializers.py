from django.shortcuts import get_object_or_404
from rest_framework import serializers
from .models import User, ROLES
from .token import account_activation_token
from django.core.mail import send_mail
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer,
)
from rest_framework import serializers


class UserRegistrSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "username"]

    def save(self, *args, **kwargs):
        if self.is_valid():
            if self.validated_data["username"] == "me":
                raise serializers.ValidationError("Username wrong!")
            if self.validated_data["username"] == "":
                raise serializers.ValidationError("Username empty!")
            if self.validated_data["email"] == "":
                raise serializers.ValidationError("Email empty!")
            user = User(
                email=self.validated_data["email"],
                username=self.validated_data["username"],
            )
            user.confirmation_code = account_activation_token.make_token(user)
            user.save()
            send_mail(
                "subject",
                user.confirmation_code,
                "email@email.ru",
                [
                    self.validated_data["email"],
                ],
            )
            return user
        raise serializers.ValidationError("Data is invalid!")


class LoginSerializer(TokenObtainPairSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        del self.fields["email"]
        del self.fields["password"]
        self.fields["username"] = serializers.CharField()
        self.fields["confirmation_code"] = serializers.CharField()

    def validate(self, attrs):
        self.user = get_object_or_404(
            User,
            username=attrs["username"],
        )
        if self.user.confirmation_code != attrs["confirmation_code"]:
            raise serializers.ValidationError("confirmation_code is wrong")
        refresh = self.get_token(self.user)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "username"]


class UsersListSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    bio = serializers.CharField(required=False)
    role = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "bio",
            "role",
        ]


class UserNameSerializer(UsersListSerializer):
    username = serializers.CharField(required=False)
    email = serializers.CharField(required=False)
    role = serializers.ChoiceField(choices=ROLES, required=False)


class UserMeSerializer(UsersListSerializer):
    role = serializers.ReadOnlyField()
