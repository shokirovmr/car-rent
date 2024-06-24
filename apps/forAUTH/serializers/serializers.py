from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

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
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'fullname',
            "phone",
            'username',
            "password1",
            "password2",
        ]
        extra_kwargs = {
            'fullname': {'write_only': True},
            "phone": {"write_only": True},
            "username": {"required": True},
        }

    def validate(self, attrs):
        password1 = attrs.pop('password1')
        password2 = attrs.pop('password2')

        if password1 != password2:
            raise serializers.ValidationError({"password": "Passwords must match."})

        if len(password1) <= 3:
            raise serializers.ValidationError({"password": "Password must be longer than 3 characters."})

        if User.objects.filter(phone=attrs["phone"]).exists():
            raise serializers.ValidationError({"phone": "User with this phone already exists."})

        if User.objects.filter(username=attrs.get("username")).exists():
            raise serializers.ValidationError({"username": "User with this username already exists."})

        attrs.update({'password': password1})
        return attrs

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = User(**validated_data)

        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()

        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)

        instance.save()
        return instance


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


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        # Add other custom claims if needed

        return token
