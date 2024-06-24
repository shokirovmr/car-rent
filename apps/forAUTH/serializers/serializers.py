from apps.forAUTH.models import User

from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers


# -------------------------------------------------------------- ( 1 )
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    new_password_confirm = serializers.CharField(required=True)

    def validate_new_password(self, value):
        if value != self.initial_data["new_password_confirm"]:
            raise serializers.ValidationError("Passwords do not match")
        validate_password(value)
        return value


# -------------------------------------------------------------- ( 2 )

class UserRegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "phone",
            "password",
            "password2",
            "avatar",
            "first_name",
            "last_name",
        ]
        extra_kwargs = {
            "phone": {"write_only": True},
            "password": {"write_only": True},
            "first_name": {"required": True},
            "last_name": {"required": True},
            "avatar": {"required": False},
        }

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError({"password": "Passwords must match."})
        phone = User.objects.filter(phone=attrs["phone"])
        if phone.exists():
            raise serializers.ValidationError(
                {"phone": "User with this phone already exists."}
            )
        email = User.objects.filter(email=attrs["email"])
        if email.exists():
            raise serializers.ValidationError(
                {"email": "User with this email already exists."}
            )
        username = User.objects.filter(username=attrs.get("username"))
        if username.exists():
            raise serializers.ValidationError(
                {"username": "User with this username already exists."}
            )
        return attrs


# -------------------------------------------------------------- ( 3 )

class ResetPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(required=True)
    confirm_new_password = serializers.CharField(required=True)

    def validate_new_password(self, value):
        if value != self.initial_data.get("confirm_new_password"):
            raise serializers.ValidationError("Passwords must match.")
        validate_password(value)
        return value


# -------------------------------------------------------------- ( 4 )


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "phone",
            "avatar",
        ]
