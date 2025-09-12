from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Prediction, Player, Team
from .serializers import PredictionSerializer
from .ml_model import predict


def index(request):
    return render(request, "ai_app/index.html")


class PredictView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        input_data = request.data.get("input_data")
        if input_data is None:
            return Response({"error": "Missing input_data"}, status=400)
        try:
            result = predict(input_data)
        except Exception as e:
            return Response({"error": f"Prediction failed: {e}"}, status=400)
        pred = Prediction.objects.create(user=request.user, input_data=input_data, result=result)
        serializer = PredictionSerializer(pred)
        return Response(serializer.data, status=201)

class HistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        qs = Prediction.objects.filter(user=request.user).order_by("-created_at")[:50]
        serializer = PredictionSerializer(qs, many=True)
        return Response(serializer.data)

class DropdownDataView(APIView):
    """Return players and teams for populating dropdown menus."""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        players = list(Player.objects.values("id", "name"))
        teams = list(Team.objects.values("id", "name"))
        return Response({"players": players, "teams": teams})
