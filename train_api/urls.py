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
from .constants import DEFAULT_LIST_ACTIONS, DEFAULT_DETAIL_ACTIONS

urlpatterns = [
    path("users/", UserViewSet.as_view(DEFAULT_LIST_ACTIONS), name="user_list"),
    path("users/<int:pk>", UserViewSet.as_view(DEFAULT_DETAIL_ACTIONS), name="user_detail"),

    path("crews/", CrewViewSet.as_view(DEFAULT_LIST_ACTIONS), name="crew_list"),
    path("crews/<int:pk>", CrewViewSet.as_view(DEFAULT_DETAIL_ACTIONS), name="crew_detail"),

    path("stations/", StationViewSet.as_view(DEFAULT_LIST_ACTIONS), name="station_list"),
    path("stations/<int:pk>", StationViewSet.as_view(DEFAULT_DETAIL_ACTIONS), name="station_detail"),

    path("train-types/", TrainTypeViewSet.as_view(DEFAULT_LIST_ACTIONS), name="train_types_list"),
    path("train-types/<int:pk>", TrainTypeViewSet.as_view(DEFAULT_DETAIL_ACTIONS), name="train_type_detail"),

    path("trains/", TrainViewSet.as_view(DEFAULT_LIST_ACTIONS), name="train_list"),
    path("trains/<int:pk>", TrainViewSet.as_view(DEFAULT_DETAIL_ACTIONS), name="train_detail"),
    path(
        "trains/<int:pk>/upload_image/",
        TrainViewSet.as_view({"post": "upload_image"}),
        name="upload_train_image"
    ),

    path("routes/", RouteViewSet.as_view(DEFAULT_LIST_ACTIONS), name="route_list"),
    path("routes/<int:pk>", RouteViewSet.as_view(DEFAULT_DETAIL_ACTIONS), name="route_detail"),

    path("journeys/", JourneyViewSet.as_view(DEFAULT_LIST_ACTIONS), name="journey_list"),
    path("journeys/<int:pk>", JourneyViewSet.as_view(DEFAULT_DETAIL_ACTIONS), name="journey_detail"),

    path("orders/", OrderViewSet.as_view(DEFAULT_LIST_ACTIONS), name="order_list"),
    path("orders/<int:pk>", OrderViewSet.as_view(DEFAULT_DETAIL_ACTIONS), name="order_detail"),

    path("tickets/", TicketViewSet.as_view(DEFAULT_LIST_ACTIONS), name="ticket_list"),
    path("tickets/<int:pk>", TicketViewSet.as_view(DEFAULT_DETAIL_ACTIONS), name="ticket_detail"),
]

app_name = "train_api"
