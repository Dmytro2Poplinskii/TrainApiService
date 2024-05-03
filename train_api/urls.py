from django.urls import path
from .views import (
    UserViewSet,
    CrewViewSet,
    StationViewSet,
    TrainTypeViewSet,
    TrainViewSet,
)

urlpatterns = [
    path("users/", UserViewSet.as_view(
        {
            "get": "list",
            "post": "create",
        }
    ), name="users"),
    path("crews/", CrewViewSet.as_view({
            "get": "list",
            "post": "create",
        }), name="crews"),
    path("stations/", StationViewSet.as_view({
            "get": "list",
            "post": "create",
    }), name="station_list"),
    path("stations/<int:pk>", StationViewSet.as_view({
        "get": "retrieve",
        "put": "update",
        "patch": "partial_update",
        "delete": "destroy"
    }), name="station_detail"),
    path("train-types/", TrainTypeViewSet.as_view({
            "get": "list",
            "post": "create",
    }), name="train_types"),
    path("trains/", TrainViewSet.as_view({
        "get": "list",
        "post": "create",
    }), name="train_list"),
    path("trains/<int:pk>", TrainViewSet.as_view({
        "get": "retrieve",
        "put": "update",
        "patch": "partial_update",
        "delete": "destroy"
    }), name="train_detail"),
]

app_name = "train_api"
