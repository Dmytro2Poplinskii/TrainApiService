from rest_framework import serializers

from train_api.models import Crew, Station, TrainType, Train, Route, Journey, Order, Ticket, Seats
from users.serializers import UserSerializer


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
    train_type = serializers.PrimaryKeyRelatedField(queryset=TrainType.objects.all())
    image = serializers.ImageField()

    class Meta:
        model = Train
        fields = ("id", "name", "carriage_num", "places_in_carriage", "train_type", "image", "num_seats")


class TrainCreateSerializer(serializers.ModelSerializer):
    train_type = serializers.PrimaryKeyRelatedField(queryset=TrainType.objects.all())

    class Meta:
        model = Train
        fields = ("name", "carriage_num", "places_in_carriage", "train_type", "num_seats")


class TrainImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Train
        fields = ("id", "image",)


class RouteListSerializer(serializers.ModelSerializer):
    source = serializers.SlugRelatedField(read_only=True, slug_field="name")
    destination = serializers.SlugRelatedField(read_only=True, slug_field="name")

    class Meta:
        model = Route
        fields = ("distance", "source", "destination",)


class RouteDetailSerializer(serializers.ModelSerializer):
    source = StationDetailSerializer()
    destination = StationDetailSerializer()

    class Meta:
        model = Route
        fields = "__all__"


class RouteCreateSerializer(serializers.ModelSerializer):
    source = serializers.PrimaryKeyRelatedField(queryset=Station.objects.all())
    destination = serializers.PrimaryKeyRelatedField(queryset=Station.objects.all())

    class Meta:
        model = Route
        fields = ("source", "destination", "distance")


class JourneyListSerializer(serializers.ModelSerializer):
    route = serializers.SlugRelatedField(read_only=True, slug_field="full_route")
    train = serializers.SlugRelatedField(read_only=True, slug_field="name")
    crews = serializers.SlugRelatedField(read_only=True, slug_field="full_name", many=True)

    class Meta:
        model = Journey
        fields = ("id", "departure_time", "arrival_time", "route", "train", "crews",)


class JourneyDetailSerializer(serializers.ModelSerializer):
    route = RouteDetailSerializer()
    train = TrainDetailSerializer()
    crews = CrewSerializer(many=True)

    class Meta:
        model = Journey
        fields = ("id", "departure_time", "arrival_time", "route", "train", "crews",)


class JourneyCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Journey
        fields = "__all__"


class OrderListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"


class OrderDetailSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Order
        fields = "__all__"


class TicketListSerializer(serializers.ModelSerializer):
    order_id = serializers.IntegerField(read_only=True, source="order.id")
    journey_route = serializers.CharField(source="journey.route.full_route", read_only=True)

    class Meta:
        model = Ticket
        fields = ("id", "journey_route", "seat", "order_id", "train")


class TicketDetailSerializer(serializers.ModelSerializer):
    journey = JourneyDetailSerializer()
    order = OrderDetailSerializer()

    class Meta:
        model = Ticket
        fields = ("id", "journey", "seat", "order", "train")


class TicketCreateSerializer(serializers.ModelSerializer):
    journey = serializers.PrimaryKeyRelatedField(queryset=Journey.objects.all())
    seat = serializers.PrimaryKeyRelatedField(queryset=Seats.objects.all())
    train = serializers.PrimaryKeyRelatedField(queryset=Train.objects.all())

    class Meta:
        model = Ticket
        fields = ("id", "journey", "seat", "train")


class MultipleTicketCreateSerializer(serializers.Serializer):
    tickets = TicketCreateSerializer(many=True)

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        order = Order.objects.create(user=user)
        tickets_data = validated_data['tickets']
        tickets = []

        for ticket_data in tickets_data:
            seat = ticket_data['seat']
            if seat.is_available:
                ticket = Ticket.objects.create(order=order, **ticket_data)
                seat.is_available = False
                seat.save()
                tickets.append(ticket)
            else:
                raise serializers.ValidationError(f"Seat {seat.id} is not available")

        return tickets
