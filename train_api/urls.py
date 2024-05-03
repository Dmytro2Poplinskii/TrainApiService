from django.urls import path
from .views import (
    UserViewSet,
    CrewViewSet,
    StationViewSet,
    TrainTypeViewSet,
    TrainViewSet, RouteViewSet, JourneyViewSet,
)

urlpatterns = [
    path("users/", UserViewSet.as_view({
            "get": "list",
            "post": "create",
        }), name="users"),
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
    path("routes/", RouteViewSet.as_view({
        "get": "list",
        "post": "create"
    }) , name="route_list"),
    path("routes/<int:pk>", RouteViewSet.as_view({
        "get": "retrieve",
        "put": "update",
        "patch": "partial_update",
        "delete": "destroy"
    }), name="route_detail"),
    path("journeys/", JourneyViewSet.as_view({
        "get": "list",
        "post": "create",
    }), name="journey_list"),
    path("journeys/<int:pk>", JourneyViewSet.as_view({
        "get": "retrieve",
        "put": "update",
        "patch": "partial_update",
        "delete": "destroy"
    }), name="journey_detail"),
]

app_name = "train_api"
