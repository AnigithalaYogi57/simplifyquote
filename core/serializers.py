import email
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from core.models import User
from rest_framework import status
from rest_framework import serializers
from django.utils import timezone
from core.helpers import generate_username


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    default_error_messages = {"no_active_account": ("Email / Password Not Matched")}

    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)
        token["email"] = user.email
        token["last_login"] = str(user.last_login)
        return token

    def validate(self, attrs):
        try:
            request = self.context["request"]
        except KeyError:
            pass
        current_user = User.objects.filter(email=request.data.get("username")).first()
        if not current_user:
            raise serializers.ValidationError(
                {"status": status.HTTP_400_BAD_REQUEST, "message": "Account doesn't exist."}
            )
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data["userid"] = current_user.id
        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)
        self.user.last_login = timezone.now()
        self.user.save()
        return data


class RegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "password",
            "name",
            "age",
            "gender",
            "reason",
        )
        extra_kwargs = {
            "password": {"write_only": True, "style": {"input_type": "password"}},
        }

    def validate(self, attrs):
        email = attrs.get("email", None)
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("Email already exists")
        return super().validate(attrs)

    def save(self, request):
        serialized_data = request.data
        email = serialized_data["email"]
        user = User(
            email=self.validated_data["email"],
            username=generate_username(email),
        )
        password = self.validated_data["password"]
        user.set_password(password)
        user.name = serialized_data["name"]
        user.reason = serialized_data["reason"]
        user.save()
        return user
