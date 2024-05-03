from django.contrib.auth.models import User
from rest_framework import viewsets

from train_api.models import Crew, Station, TrainType, Train, Route, Journey, Order, Ticket
from train_api.serializers import (
    UserSerializer,
    CrewSerializer,
    StationListSerializer,
    StationDetailSerializer,
    TrainTypeSerializer,
    TrainListSerializer,
    TrainDetailSerializer,
    RouteListSerializer,
    RouteDetailSerializer,
    JourneyListSerializer,
    JourneyDetailSerializer,
    OrderListSerializer,
    OrderDetailSerializer, TicketListSerializer, TicketDetailSerializer, JourneyCreateSerializer,
)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by("-date_joined")
    serializer_class = UserSerializer


class CrewViewSet(viewsets.ModelViewSet):
    queryset = Crew.objects.all()
    serializer_class = CrewSerializer


class StationViewSet(viewsets.ModelViewSet):
    queryset = Station.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return StationListSerializer
        else:
            return StationDetailSerializer


class TrainTypeViewSet(viewsets.ModelViewSet):
    queryset = TrainType.objects.all()
    serializer_class = TrainTypeSerializer


class TrainViewSet(viewsets.ModelViewSet):
    queryset = Train.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return TrainListSerializer
        else:
            return TrainDetailSerializer


class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return RouteListSerializer
        else:
            return RouteDetailSerializer


class JourneyViewSet(viewsets.ModelViewSet):
    queryset = Journey.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return JourneyListSerializer
        elif self.action in ("create", "update", "partial_update"):
            return JourneyCreateSerializer

        return JourneyDetailSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()

    def get_serializer_class(self):
        if self.action in ("list", "create", "update", "partial_update"):
            return OrderListSerializer

        return OrderDetailSerializer


class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return TicketListSerializer
        else:
            return TicketDetailSerializer
