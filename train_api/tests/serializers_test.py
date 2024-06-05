import datetime
from rest_framework.test import APITestCase
from django.test import TestCase
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User

from train_api.models import Crew, Station, TrainType, Train, Seat, Route, Journey, Order, Ticket
from train_api.serializers import (
    CrewSerializer,
    StationListSerializer,
    StationDetailSerializer,
    TrainTypeSerializer,
    TrainListSerializer,
    TrainDetailSerializer,
    TrainCreateSerializer,
    TrainImageSerializer,
    RouteListSerializer,
    RouteDetailSerializer,
    RouteCreateSerializer,
    JourneyListSerializer,
    JourneyDetailSerializer,
    JourneyCreateSerializer,
    OrderListSerializer,
    OrderDetailSerializer,
    TicketListSerializer,
    TicketDetailSerializer,
    TicketCreateSerializer,
    MultipleTicketCreateSerializer,
)


class CrewSerializerTest(APITestCase):
    def setUp(self):
        self.crew_data = {
            "first_name": "John",
            "last_name": "Doe",
        }
        self.crew = Crew.objects.create(**self.crew_data)

    def test_crew_serialization(self):
        serializer = CrewSerializer(self.crew)
        data = serializer.data
        expected_data = self.crew_data.copy()
        expected_data['id'] = self.crew.id

        self.assertEqual(set(data.keys()), set(expected_data.keys()))
        for key in expected_data.keys():
            self.assertEqual(data[key], expected_data[key])

    def test_crew_deserialization(self):
        serializer = CrewSerializer(data=self.crew_data)
        self.assertTrue(serializer.is_valid())
        crew = serializer.save()
        self.assertEqual(crew.first_name, self.crew_data["first_name"])
        self.assertEqual(crew.last_name, self.crew_data["last_name"])


class StationSerializerTest(APITestCase):
    def setUp(self):
        self.station_data = {
            "name": "Station One",
            "latitude": 55.55,
            "longitude": 22.22,
        }
        self.station = Station.objects.create(**self.station_data)

    def test_station_list_serialization(self):
        serializer = StationListSerializer(self.station)
        data = serializer.data
        self.assertEqual(data["name"], self.station_data["name"])

    def test_station_list_deserialization(self):
        serializer = StationDetailSerializer(data=self.station_data)
        self.assertTrue(serializer.is_valid())
        station = serializer.save()
        self.assertEqual(station.name, self.station_data["name"])


class TrainTypeSerializerTest(APITestCase):
    def setUp(self):
        self.train_type_data = {"name": "Freight"}
        self.train_type = TrainType.objects.create(**self.train_type_data)

    def test_train_type_serialization(self):
        serializer = TrainTypeSerializer(self.train_type)
        data = serializer.data
        self.assertEqual(set(data.keys()), set(self.train_type_data.keys()).union({"id"}))
        self.assertEqual(data["name"], self.train_type_data["name"])
        self.assertEqual(data["id"], self.train_type.id)

    def test_train_type_deserialization(self):
        serializer = TrainTypeSerializer(data=self.train_type_data)
        self.assertTrue(serializer.is_valid())
        train_type = serializer.save()
        self.assertEqual(train_type.name, self.train_type_data["name"])


class TrainListSerializerTest(APITestCase):
    def setUp(self):
        self.train_type = TrainType.objects.create(name="Freight")
        self.train = Train.objects.create(
            name="Express",
            carriage_num=10,
            places_in_carriage=20,
            train_type=self.train_type
        )

    def test_train_list_serialization(self):
        serializer = TrainListSerializer(self.train)
        data = serializer.data
        self.assertEqual(data["name"], self.train.name)
        self.assertEqual(data["train_type"], self.train_type.name)


class TrainDetailSerializerTest(APITestCase):
    def setUp(self):
        self.train_type = TrainType.objects.create(name="Freight")
        self.train = Train.objects.create(
            name="Express",
            carriage_num=10,
            places_in_carriage=20,
            train_type=self.train_type,
            image=None
        )
        # Creating seats for the train with seat numbers and carriages
        Seat.objects.bulk_create(
            [Seat(train=self.train, seat=i+1, carriage=1, is_available=True) for i in range(100)]
        )
        Seat.objects.bulk_create(
            [Seat(train=self.train, seat=i+1, carriage=2, is_available=False) for i in range(100)]
        )

    def test_train_detail_serialization(self):
        serializer = TrainDetailSerializer(self.train)
        data = serializer.data
        self.assertEqual(data['name'], self.train.name)
        self.assertEqual(data['carriage_num'], self.train.carriage_num)
        self.assertEqual(data['places_in_carriage'], self.train.places_in_carriage)
        self.assertEqual(data['train_type'], self.train.train_type.id)
        self.assertEqual(data['image'], self.train.image)
        self.assertEqual(data['num_seats'], self.train.num_seats)
        self.assertEqual(data['available_num_seats'], 100)

    def test_train_detail_deserialization(self):
        image = Image.open("train_api/tests/utils/train_test.jpg")

        byte_io = BytesIO()
        image.save(byte_io, format='JPEG')

        image_content = byte_io.getvalue()
        image = SimpleUploadedFile("test_image.jpg", image_content, content_type="image/jpeg")
        train_data = {
            "name": "Express",
            "carriage_num": 10,
            "places_in_carriage": 20,
            "train_type": self.train_type.id,
            "image": image,
        }
        serializer = TrainDetailSerializer(data=train_data)
        is_valid = serializer.is_valid()
        if not is_valid:
            print("Serializer errors:", serializer.errors)
        self.assertTrue(is_valid)
        if is_valid:
            train = serializer.save()
            self.assertEqual(train.name, train_data['name'])
            self.assertEqual(train.carriage_num, train_data['carriage_num'])
            self.assertEqual(train.places_in_carriage, train_data['places_in_carriage'])
            self.assertEqual(train.train_type.id, train_data['train_type'])
            self.assertEqual(train.num_seats, train_data['carriage_num'] * train_data['places_in_carriage'])


class TrainCreateSerializerTest(APITestCase):
    def setUp(self):
        self.train_type = TrainType.objects.create(name="Freight")
        self.train_data = {
            "name": "Express",
            "carriage_num": 10,
            "places_in_carriage": 20,
            "train_type": self.train_type.id,
            "num_seats": 200
        }

    def test_train_create_serialization(self):
        serializer = TrainCreateSerializer(data=self.train_data)
        self.assertTrue(serializer.is_valid())
        train = serializer.save()
        self.assertEqual(train.name, self.train_data['name'])
        self.assertEqual(train.carriage_num, self.train_data['carriage_num'])
        self.assertEqual(train.places_in_carriage, self.train_data['places_in_carriage'])
        self.assertEqual(train.train_type.id, self.train_data['train_type'])
        self.assertEqual(train.num_seats, self.train_data['carriage_num'] * self.train_data['places_in_carriage'])


class TrainImageSerializerTest(APITestCase):
    def setUp(self):
        self.train_type = TrainType.objects.create(name="Passenger")
        self.train = Train.objects.create(
            name="Express",
            carriage_num=10,
            places_in_carriage=20,
            train_type=self.train_type,
            image=None
        )

    def test_train_image_serialization(self):
        serializer = TrainImageSerializer(self.train)
        data = serializer.data
        self.assertEqual(data['id'], self.train.id)
        self.assertEqual(data['image'], self.train.image)


class RouteSerializerTest(TestCase):
    def setUp(self):
        self.station_a = Station.objects.create(name="Station A", latitude=1.0, longitude=2.0)
        self.station_b = Station.objects.create(name="Station B", latitude=3.0, longitude=4.0)
        self.route = Route.objects.create(source=self.station_a, destination=self.station_b)

    def test_route_list_serialization(self):
        serializer = RouteListSerializer(instance=self.route)
        data = serializer.data
        self.assertEqual(data['source'], self.station_a.name)
        self.assertEqual(data['destination'], self.station_b.name)
        self.assertAlmostEqual(data['distance'], self.route.distance, places=2)

    def test_route_detail_serialization(self):
        serializer = RouteDetailSerializer(instance=self.route)
        data = serializer.data
        self.assertEqual(data['source']['name'], self.station_a.name)
        self.assertEqual(data['destination']['name'], self.station_b.name)

    def test_route_create_serialization(self):
        data = {
            "source": self.station_a.id,
            "destination": self.station_b.id,
            "distance": self.route.distance,
        }
        serializer = RouteCreateSerializer(data=data)
        is_valid = serializer.is_valid()
        if not is_valid:
            print("Serializer errors:", serializer.errors)
        self.assertTrue(is_valid)
        if is_valid:
            route = serializer.save()
            self.assertEqual(route.source, self.station_a)
            self.assertEqual(route.destination, self.station_b)
            self.assertAlmostEqual(route.distance, self.route.distance, places=2)


class JourneySerializerTest(TestCase):
    def setUp(self):
        self.station_a = Station.objects.create(name="Station A", latitude=1.0, longitude=2.0)
        self.station_b = Station.objects.create(name="Station B", latitude=3.0, longitude=4.0)
        self.route = Route.objects.create(source=self.station_a, destination=self.station_b)
        self.train_type = TrainType.objects.create(name="Passenger")
        self.train = Train.objects.create(name="Express", carriage_num=10, places_in_carriage=20, train_type=self.train_type)
        self.crew = Crew.objects.create(first_name="John", last_name="Doe")
        self.journey = Journey.objects.create(
            route=self.route,
            train=self.train,
            departure_time="2024-06-01T12:00:00Z",
            arrival_time="2024-06-01T14:00:00Z",
        )
        self.journey.crews.add(self.crew)

    def test_journey_list_serialization(self):
        serializer = JourneyListSerializer(instance=self.journey)
        data = serializer.data
        self.assertEqual(data['id'], self.journey.id)
        self.assertEqual(data['route'], self.route.full_route)
        self.assertEqual(data['train'], self.train.name)
        self.assertEqual(data['crews'], [self.crew.full_name])

    def test_journey_detail_serialization(self):
        serializer = JourneyDetailSerializer(instance=self.journey)
        data = serializer.data
        self.assertEqual(data['id'], self.journey.id)
        self.assertEqual(data['route']['source']['name'], self.station_a.name)
        self.assertEqual(data['route']['destination']['name'], self.station_b.name)
        self.assertEqual(data['train']['name'], self.train.name)

    def test_journey_create_serialization(self):
        data = {
            "route": self.route.id,
            "train": self.train.id,
            "departure_time": "2024-06-01T12:00:00Z",
            "arrival_time": "2024-06-01T14:00:00Z",
            "crews": [self.crew.id],
        }
        serializer = JourneyCreateSerializer(data=data)
        is_valid = serializer.is_valid()
        if not is_valid:
            print("Serializer errors:", serializer.errors)
        self.assertTrue(is_valid)
        if is_valid:
            journey = serializer.save()
            self.assertEqual(journey.route, self.route)
            self.assertEqual(journey.train, self.train)
            self.assertEqual(journey.departure_time.isoformat(), "2024-06-01T12:00:00+00:00")
            self.assertEqual(journey.arrival_time.isoformat(), "2024-06-01T14:00:00+00:00")
            self.assertEqual(list(journey.crews.all()), [self.crew])


class OrderSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="test_user")
        self.order = Order.objects.create(user=self.user)

    def test_order_list_serialization(self):
        serializer = OrderListSerializer(instance=self.order)
        data = serializer.data
        self.assertEqual(data['id'], self.order.id)
        self.assertEqual(datetime.datetime.fromisoformat(data['created_date']), self.order.created_date)
        self.assertEqual(data['user'], self.user.id)

    def test_order_detail_serialization(self):
        serializer = OrderDetailSerializer(instance=self.order)
        data = serializer.data
        self.assertEqual(data['id'], self.order.id)
        self.assertEqual(datetime.datetime.fromisoformat(data['created_date']), self.order.created_date)
        self.assertEqual(data['user']['id'], self.user.id)
        self.assertEqual(data['user']['username'], self.user.username)


class TicketSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.order = Order.objects.create(user=self.user)
        self.train_type = TrainType.objects.create(name="Passenger")
        self.train = Train.objects.create(name="Express", carriage_num=10, places_in_carriage=20, train_type=self.train_type)
        self.station1 = Station.objects.create(name="Station 1", latitude=1.0, longitude=1.0)
        self.station2 = Station.objects.create(name="Station 2", latitude=2.0, longitude=2.0)
        self.route = Route.objects.create(source=self.station1, destination=self.station2)
        self.journey = Journey.objects.create(route=self.route, train=self.train, departure_time="2024-06-05T18:50:25.928493Z", arrival_time="2024-06-06T18:50:25.928493Z")
        self.seat = Seat.objects.create(train=self.train, seat=1, carriage=1, is_available=True)
        self.ticket = Ticket.objects.create(train=self.train, seat=self.seat, journey=self.journey, order=self.order)

    def test_ticket_list_serialization(self):
        serializer = TicketListSerializer(instance=self.ticket)
        data = serializer.data
        self.assertEqual(data['id'], self.ticket.id)
        self.assertEqual(data['journey_route'], self.journey.route.full_route)
        self.assertEqual(data['seat'], self.ticket.seat.id)
        self.assertEqual(data['order_id'], self.order.id)
        self.assertEqual(data['train'], self.ticket.train.id)

    def test_ticket_detail_serialization(self):
        serializer = TicketDetailSerializer(instance=self.ticket)
        data = serializer.data
        self.assertEqual(data['id'], self.ticket.id)
        self.assertEqual(data['seat'], self.ticket.seat.id)
        self.assertEqual(data['order']['id'], self.order.id)
        self.assertEqual(data['train'], self.ticket.train.id)

    def test_ticket_create_serialization(self):
        serializer = TicketCreateSerializer(data={"journey": self.journey.id, "seat": self.seat.id, "train": self.train.id})
        self.assertTrue(serializer.is_valid())
        ticket = serializer.save(order=self.order)
        self.assertEqual(ticket.journey, self.journey)
        self.assertEqual(ticket.seat, self.seat)
        self.assertEqual(ticket.train, self.train)

    def test_multiple_ticket_create_serializer(self):
        multiple_ticket_data = [
            {"journey": self.journey.id, "seat": self.seat.id, "train": self.train.id},
            {"journey": self.journey.id, "seat": self.seat.id, "train": self.train.id},
        ]
        serializer = MultipleTicketCreateSerializer(data={"tickets": multiple_ticket_data}, context={"request": self.order})
        self.assertTrue(serializer.is_valid())
        tickets = serializer.save()
        self.assertEqual(len(tickets), 2)
