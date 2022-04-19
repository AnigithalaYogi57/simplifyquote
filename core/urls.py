from django.urls import path
from core.models import Quotes
from core.views import MyTokenObtainPairView,SignUpView
from core.quotes import QuotesView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("login", MyTokenObtainPairView.as_view()),
    path("login/refresh", TokenRefreshView.as_view()),
    path("signup", SignUpView.as_view()),
    path("today/quote", QuotesView.as_view()),
]