from django.urls import path
from .views import (index, PredictView, HistoryView, DropdownDataView, SignUpView, LoginAPI, logout_api,)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path("", index, name="index"),
    path("api/predict/", PredictView.as_view(), name="predict"),
    path("api/history/", HistoryView.as_view(), name="history"),
    path("api/dropdown-data/", DropdownDataView.as_view(), name="dropdown-data"),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    # Authentication APIs
    path("api/signup/", SignUpView.as_view(), name="signup"),
    path("api/login/", LoginAPI.as_view(), name="login"),
    path("api/logout/", logout_api, name="logout"),
]
