from rest_framework import viewsets, status, permissions
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.response import Response

from train_api.models import Crew, Station, TrainType, Train, Route, Journey, Order, Ticket
from train_api.serializers import (
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
    OrderDetailSerializer,
    TicketListSerializer,
    TicketDetailSerializer,
    JourneyCreateSerializer,
    TrainImageSerializer, RouteCreateSerializer,
)


class CrewViewSet(viewsets.ModelViewSet):
    queryset = Crew.objects.all()
    serializer_class = CrewSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = [permissions.IsAuthenticated,]


class StationViewSet(viewsets.ModelViewSet):
    queryset = Station.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = [permissions.IsAuthenticated,]

    def get_serializer_class(self):
        if self.action == "list":
            return StationListSerializer
        else:
            return StationDetailSerializer


class TrainTypeViewSet(viewsets.ModelViewSet):
    queryset = TrainType.objects.all()
    serializer_class = TrainTypeSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = [permissions.IsAuthenticated,]


class TrainViewSet(viewsets.ModelViewSet):
    queryset = Train.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = [permissions.IsAuthenticated,]

    def get_serializer_class(self):
        if self.action == "list":
            return TrainListSerializer
        elif self.action == "upload_image":
            return TrainImageSerializer
        else:
            return TrainDetailSerializer

    @action(methods=["POST"], detail=True, url_path="upload-image")
    def upload_image(self, request, pk=None):
        train = self.get_object()
        serializer = self.get_serializer(train, data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = [permissions.IsAuthenticated,]

    def get_serializer_class(self):
        print("self.action", self.action)
        if self.action == "list":
            return RouteListSerializer
        elif self.action in ("create", "update", "partial_update"):
            return RouteCreateSerializer
        else:
            return RouteDetailSerializer


class JourneyViewSet(viewsets.ModelViewSet):
    queryset = Journey.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = [permissions.IsAuthenticated,]

    def get_serializer_class(self):
        if self.action == "list":
            return JourneyListSerializer
        elif self.action in ("create", "update", "partial_update"):
            return JourneyCreateSerializer

        return JourneyDetailSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = [permissions.IsAuthenticated,]

    def get_serializer_class(self):
        if self.action in ("list", "create", "update", "partial_update"):
            return OrderListSerializer

        return OrderDetailSerializer


class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = [permissions.IsAuthenticated,]

    def get_serializer_class(self):
        if self.action in ("list", "create", "update", "partial_update"):
            return TicketListSerializer
        else:
            return TicketDetailSerializer
