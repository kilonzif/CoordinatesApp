# app/serializers.py
from rest_framework import serializers
from app.models import Trilateration

class TrilaterationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trilateration
        fields = '__all__'

