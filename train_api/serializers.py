from django.contrib.auth.models import User
from rest_framework import serializers

from train_api.models import Crew, Station, TrainType


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "email")


class CrewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crew
        fields = "__all__"


class StationListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Station
        fields = ("name",)


class StationDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Station
        fields = "__all__"


class TrainTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainType
        fields = "__all__"
