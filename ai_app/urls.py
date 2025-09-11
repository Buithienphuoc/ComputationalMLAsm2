from django.urls import path
from .views import index, PredictView, HistoryView

urlpatterns = [
    path("", index, name="index"),
    path("api/predict/", PredictView.as_view(), name="predict"),
    path("api/history/", HistoryView.as_view(), name="history"),
]
