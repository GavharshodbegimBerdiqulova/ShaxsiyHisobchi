from django.utils.translation import gettext_lazy as _
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import LoginSerializer, RegisterSerializer, UserSerializer


# ---------- Auth ----------

def get_tokens(user):
    # Foydalanuvchi uchun access va refresh token yaratadi
    refresh = RefreshToken.for_user(user)
    return {"access": str(refresh.access_token), "refresh": str(refresh)}


class RegisterView(generics.CreateAPIView):
    # Ro'yxatdan o'tish: login talab qilinmaydi
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        data = UserSerializer(user).data
        data.update(get_tokens(user))
        return Response(data, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    # login (username yoki email) va parol bersa, access va refresh token qaytaradi
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        data = get_tokens(user)
        data["user"] = UserSerializer(user).data
        return Response(data)


class LogoutView(APIView):
    # refresh token blacklist'ga qo'shiladi, shundan keyin u ishlamaydi
    def post(self, request):
        try:
            RefreshToken(request.data.get("refresh")).blacklist()
        except TokenError:
            return Response(
                {"detail": _("Refresh token noto'g'ri yoki muddati o'tgan.")},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response({"detail": _("Tizimdan chiqdingiz.")})


class ProfileView(generics.RetrieveUpdateAPIView):
    # O'zining ma'lumotini ko'rish va o'zgartirish
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user
