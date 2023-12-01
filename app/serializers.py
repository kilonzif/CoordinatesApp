# app/serializers.py
from rest_framework import serializers

class TrilaterationSerializer(serializers.Serializer):
    lat1 = serializers.FloatField()
    lon1 = serializers.FloatField()
    lat2 = serializers.FloatField()
    lon2 = serializers.FloatField()
    lat3 = serializers.FloatField()
    lon3 = serializers.FloatField()
    d1 = serializers.FloatField()
    d2 = serializers.FloatField()
    d3 = serializers.FloatField()
