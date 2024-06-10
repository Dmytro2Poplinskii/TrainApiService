from datetime import datetime
from django.test import TestCase
from django.contrib.auth.models import User

from train_api.models import (
    Crew,
    TrainType,
    Station,
    Order,
    Train,
    Seat,
    Route,
    Journey,
    Ticket,
)


class CrewModelTestCase(TestCase):
    def setUp(self):
        self.crew = Crew.objects.create(first_name="John", last_name="Doe")

    def test_full_name_property(self):
        expected_full_name = "John Doe"
        self.assertEqual(self.crew.full_name, expected_full_name)

    def test_str_method(self):
        expected_str = "John Doe"
        self.assertEqual(str(self.crew), expected_str)


class TrainTypeModelTestCase(TestCase):
    def setUp(self):
        self.train_type = TrainType.objects.create(name="Express")

    def test_str_method(self):
        expected_str = "Express"
        self.assertEqual(str(self.train_type), expected_str)


class StationModelTestCase(TestCase):
    def setUp(self):
        self.station = Station.objects.create(
            name="Test Station", latitude=0.0, longitude=0.0
        )

    def test_str_method(self):
        expected_str = "Test Station"
        self.assertEqual(str(self.station), expected_str)


class OrderModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="testuser")
        self.order = Order.objects.create(user=self.user)

    def test_str_method(self):
        expected_str = (
            f"Order for {self.user.username}. Date: {self.order.created_date}"
        )
        self.assertEqual(str(self.order), expected_str)


class TrainModelTestCase(TestCase):
    def setUp(self):
        self.train_type = TrainType.objects.create(name="Test Train Type")
        self.train = Train.objects.create(
            name="Test Train",
            carriage_num=5,
            places_in_carriage=50,
            train_type=self.train_type,
        )

    def test_num_seats_property(self):
        expected_num_seats = self.train.carriage_num * self.train.places_in_carriage
        self.assertEqual(self.train.num_seats, expected_num_seats)

    def test_str_method(self):
        expected_str = f"{self.train.name}. {self.train.carriage_num} {self.train.places_in_carriage}"
        self.assertEqual(str(self.train), expected_str)


class SeatModelTestCase(TestCase):
    def setUp(self):
        self.train_type = TrainType.objects.create(name="Test Train Type")
        self.train = Train.objects.create(
            name="Test Train",
            carriage_num=5,
            places_in_carriage=50,
            train_type=self.train_type,
        )
        self.seat = Seat.objects.create(
            train=self.train, seat=1, carriage=1, is_available=True
        )

    def test_str_method(self):
        expected_str = f"{self.train}. {self.seat.seat} - {self.seat.carriage}"
        self.assertEqual(str(self.seat), expected_str)


class RouteModelTestCase(TestCase):
    def setUp(self):
        self.source = Station.objects.create(
            name="Source Station", latitude=0, longitude=0
        )
        self.destination = Station.objects.create(
            name="Destination Station", latitude=1, longitude=1
        )
        self.route = Route.objects.create(
            source=self.source, destination=self.destination
        )

    def test_distance_property(self):
        expected_distance = 2**0.5
        self.assertAlmostEqual(self.route.distance, expected_distance)

    def test_full_route_property(self):
        expected_full_route = f"{self.source.name}-{self.destination.name}"
        self.assertEqual(self.route.full_route, expected_full_route)

    def test_str_method(self):
        expected_str = (
            f"Source: {self.source.name}. Destination: {self.destination.name}"
        )
        self.assertEqual(str(self.route), expected_str)


class JourneyModelTestCase(TestCase):
    def setUp(self):
        self.train_type = TrainType.objects.create(name="Test Train Type")
        self.source = Station.objects.create(
            name="Source Station", latitude=0, longitude=0
        )
        self.destination = Station.objects.create(
            name="Destination Station", latitude=1, longitude=1
        )
        self.route = Route.objects.create(
            source=self.source, destination=self.destination
        )
        self.train = Train.objects.create(
            name="Test Train",
            carriage_num=5,
            places_in_carriage=10,
            train_type=self.train_type,
            image=None,
        )
        self.crew = Crew.objects.create(first_name="John", last_name="Doe")
        self.journey = Journey.objects.create(
            route=self.route,
            train=self.train,
            departure_time=datetime.now(),
            arrival_time=datetime.now(),
        )
        self.journey.crews.add(self.crew)

    def test_str_method(self):
        expected_str = (
            f"Route: {self.route}"
            f"Train: {self.train}"
            f"Departure time: {self.journey.departure_time}"
            f"Arrival time: {self.journey.arrival_time}"
        )
        self.assertEqual(str(self.journey), expected_str)

    def test_crews_relation(self):
        self.assertIn(self.crew, self.journey.crews.all())


class TicketModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="testuser")
        self.train_type = TrainType.objects.create(name="Test Train Type")
        self.source = Station.objects.create(
            name="Source Station", latitude=0, longitude=0
        )
        self.destination = Station.objects.create(
            name="Destination Station", latitude=1, longitude=1
        )
        self.route = Route.objects.create(
            source=self.source, destination=self.destination
        )
        train = Train.objects.create(
            name="Test Train",
            carriage_num=5,
            places_in_carriage=10,
            train_type=self.train_type,
        )
        seat = Seat.objects.create(train=train, seat=1, carriage=1, is_available=True)
        journey = Journey.objects.create(
            route=self.route,
            train=train,
            departure_time=datetime.now(),
            arrival_time=datetime.now(),
        )
        order = Order.objects.create(created_date=datetime.now(), user=self.user)

        self.ticket = Ticket.objects.create(
            train=train, seat=seat, journey=journey, order=order
        )

    def test_ticket_str(self):
        self.assertEqual(
            str(self.ticket),
            f"Cargo: {self.ticket.train}. Seat: {self.ticket.seat}. Journey: {self.ticket.journey}. Order: {self.ticket.order}",
        )
