from rest_framework import serializers
from .models import Prediction

class PredictionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prediction
        fields = ["id", "user", "input_data", "result", "created_at"]
        read_only_fields = ["user", "result", "created_at"]
