from django.urls import path
from .views import (index, PredictView, HistoryView, DropdownDataView, SignUpView, LoginAPI, logout_api,)

urlpatterns = [
    path("", index, name="index"),
    path("api/predict/", PredictView.as_view(), name="predict"),
    path("api/history/", HistoryView.as_view(), name="history"),
    path("api/dropdown-data/", DropdownDataView.as_view(), name="dropdown-data"),

    # Authentication APIs
    path("api/signup/", SignUpView.as_view(), name="signup"),
    path("api/login/", LoginAPI.as_view(), name="login"),
    path("api/logout/", logout_api, name="logout"),
]
