from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import api_view, permission_classes

from django.contrib.auth.models import User
from django.contrib.auth import login, logout

from .models import Prediction, Player, Team
from .serializers import PredictionSerializer, SignUpSerializer
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
        players = list(Player.objects.values("id", "name").order_by("name"))
        teams = list(Team.objects.values("id", "name").order_by("name"))
        return Response({"players": players, "teams": teams})

class SignUpView(APIView):
    """API endpoint to register a new user."""
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, _ = Token.objects.get_or_create(user=user)
            return Response(
                {"message": "User created successfully", "token": token.key},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPI(ObtainAuthToken):
    """API endpoint to log in and retrieve a token."""

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data["token"])
        return Response({
            "token": token.key,
            "user_id": token.user_id,
            "username": token.user.username
        })


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout_api(request):
    """API endpoint to log out by deleting the user's token."""
    request.user.auth_token.delete()
    logout(request)
    return Response({"message": "Logged out successfully"}, status=200)
