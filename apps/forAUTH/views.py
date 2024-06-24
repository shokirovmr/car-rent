from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from apps.forAUTH.models import User
from apps.forAUTH.serializers import ChangePasswordSerializer
from apps.forAUTH.serializers import ResetPasswordSerializer
from apps.forAUTH.serializers.serializers import UserRegisterSerializer, UserSerializer


class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ["put"]

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if not request.user.check_password(
                serializer.validated_data.get("old_password")
        ):
            return Response(
                {"old_password": ["Wrong password."]},
                status=status.HTTP_400_BAD_REQUEST,
            )
        request.user.set_password(serializer.validated_data.get("new_password"))
        request.user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserLogoutView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        return None

    def delete(self, request, *args, **kwargs):
        request.user.auth_token.delete()
        return Response(status=204)


class UserRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]


class ResetPasswordView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = ResetPasswordSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    http_method_names = ["put"]

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user.set_password(serializer.validated_data.get("new_password"))
        user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserDetailView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
