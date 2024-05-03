from django.urls import path
from .views import (
    UserViewSet,
    CrewViewSet,
    StationViewSet,
    TrainTypeViewSet,
    TrainViewSet,
    RouteViewSet,
    JourneyViewSet,
    OrderViewSet,
    TicketViewSet,
)

urlpatterns = [
    path("users/", UserViewSet.as_view({
            "get": "list",
            "post": "create",
    }), name="user_list"),
    path("users/<int:pk>", UserViewSet.as_view({
        "get": "retrieve",
        "put": "update",
        "patch": "partial_update",
        "delete": "destroy"
    }), name="user_detail"),
    path("crews/", CrewViewSet.as_view({
            "get": "list",
            "post": "create",
    }), name="crew_list"),
    path("crews/<int:pk>", CrewViewSet.as_view({
        "get": "retrieve",
        "put": "update",
        "patch": "partial_update",
        "delete": "destroy"
    }), name="crew_detail"),
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
    }), name="train_types_list"),
    path("train-types/<int:pk>", TrainTypeViewSet.as_view({
        "get": "retrieve",
        "put": "update",
        "patch": "partial_update",
        "delete": "destroy"
    }), name="train_type_detail"),
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
    path("orders/", OrderViewSet.as_view({
        "get": "list",
        "post": "create",
    }), name="order_list"),
    path("orders/<int:pk>", OrderViewSet.as_view({
        "get": "retrieve",
        "put": "update",
        "patch": "partial_update",
        "delete": "destroy",
    }), name="order_detail"),
    path("tickets/", TicketViewSet.as_view({
        "get": "list",
        "post": "create",
    }), name="ticket_list"),
    path("tickets/<int:pk>", TicketViewSet.as_view({
        "get": "retrieve",
        "put": "update",
        "patch": "partial_update",
        "delete": "destroy"
    }), name="ticket_detail"),
]

app_name = "train_api"
