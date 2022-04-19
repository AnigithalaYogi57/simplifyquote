from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny
from core.serializers import MyTokenObtainPairSerializer, RegisterSerializer
from rest_framework import generics
from core.models import User
from core.helpers import api_response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status




class MyTokenObtainPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer

class SignUpView(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    queryset = User.objects.all()
    # parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save(request)
            user_data = serializer.data
            user = User.objects.get(email=user_data["email"])

            id = user.id
            token = RefreshToken.for_user(user)
            token["email"] = user.email
            data = {
                "id": id,
                "email": user.email,
                "access_token": str(token.access_token),
                "refresh_token": str(token),
            }
            return api_response(201, "Registration successfully done", data)
        else:
            for key, values in serializer.errors.items():
                error = [value[:] for value in values][0]
            return api_response(status.HTTP_400_BAD_REQUEST, "Invalid data", error)