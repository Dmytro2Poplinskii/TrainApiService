from django.contrib.auth.models import User
from rest_framework import serializers

from train_api.models import Crew, Station, TrainType, Train


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


class TrainListSerializer(serializers.ModelSerializer):
    train_type = serializers.SlugRelatedField(read_only=True, slug_field="name")

    class Meta:
        model = TrainType
        fields = ("name", "train_type")


class TrainDetailSerializer(serializers.ModelSerializer):
    train_type = TrainTypeSerializer(read_only=True)

    class Meta:
        model = Train
        fields = ("id", "name", "cargo_num", "places_in_cargo", "train_type",)
