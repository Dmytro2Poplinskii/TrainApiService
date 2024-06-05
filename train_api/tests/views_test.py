from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.core.files.uploadedfile import SimpleUploadedFile

from train_api.models import Crew, Station, TrainType, Train, Route, Journey, Order, Seat, Ticket


class CrewViewSetTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.token = Token.objects.create(user=self.user)
        Crew.objects.create(first_name='John', last_name='Doe')

    def test_list_crew(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.get('/api/v1/crews/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['first_name'], 'John')
        self.assertEqual(response.data[0]['last_name'], 'Doe')

    def test_create_crew(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        data = {'first_name': 'Jane', 'last_name': 'Doe'}
        response = self.client.post('/api/v1/crews/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Crew.objects.count(), 2)
        self.assertEqual(Crew.objects.last().first_name, 'Jane')
        self.assertEqual(Crew.objects.last().last_name, 'Doe')


class StationViewSetTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.token = Token.objects.create(user=self.user)
        Station.objects.create(name='Station 1', latitude=1.0, longitude=1.0)
        Station.objects.create(name='Station 2', latitude=2.0, longitude=2.0)

    def test_list_stations(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.get('/api/v1/stations/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), Station.objects.count())

    def test_retrieve_station(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        station_id = Station.objects.first().id
        response = self.client.get(f'/api/v1/stations/{station_id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], Station.objects.first().name)
        self.assertEqual(response.data['latitude'], Station.objects.first().latitude)
        self.assertEqual(response.data['longitude'], Station.objects.first().longitude)


class TrainTypeViewSetTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.token = Token.objects.create(user=self.user)
        TrainType.objects.create(name='Passenger')
        TrainType.objects.create(name='Cargo')

    def test_list_train_types(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.get('/api/v1/train-types/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), TrainType.objects.count())

    def test_retrieve_train_type(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        train_type_id = TrainType.objects.first().id
        response = self.client.get(f'/api/v1/train-types/{train_type_id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], TrainType.objects.first().name)


class TrainViewSetTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.token = Token.objects.create(user=self.user)
        self.train_type = TrainType.objects.create(name='Passenger')
        self.train = Train.objects.create(name="Test Train", carriage_num=5, places_in_carriage=10, train_type=self.train_type)

    def test_list_train(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.get('/api/v1/trains/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_train(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        train_id = self.train.id
        response = self.client.get(f'/api/v1/trains/{train_id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_train(self):
        image_path = "train_api/tests/utils/train_test.jpg"
        with open(image_path, "rb") as image_file:
            image_data = SimpleUploadedFile(image_path, image_file.read(), content_type="image/jpeg")

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        new_train_data = {
            'name': 'New Train',
            'carriage_num': 3,
            'places_in_carriage': 15,
            "train_type": 1,
            "num_seats": 2,
            "image": image_data
        }
        response = self.client.post('/api/v1/trains/', new_train_data, format='multipart')
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], new_train_data['name'])
        self.assertEqual(response.data['carriage_num'], new_train_data['carriage_num'])
        self.assertEqual(response.data['places_in_carriage'], new_train_data['places_in_carriage'])


class RouteViewSetTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.route1 = Route.objects.create(source=Station.objects.create(name='Station 1', latitude=1.0, longitude=1.0),
                                           destination=Station.objects.create(name='Station 2', latitude=2.0, longitude=2.0))
        self.route2 = Route.objects.create(source=Station.objects.create(name='Station 2', latitude=2.0, longitude=2.0),
                                           destination=Station.objects.create(name='Station 3', latitude=3.0, longitude=3.0))

    def test_list_routes(self):
        response = self.client.get('/api/v1/routes/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), Route.objects.count())

    def test_retrieve_route(self):
        route_id = self.route1.id
        response = self.client.get(f'/api/v1/routes/{route_id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['source']['name'], self.route1.source.name)
        self.assertEqual(response.data['destination']['name'], self.route1.destination.name)


class JourneyViewSetTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.route = Route.objects.create(source=Station.objects.create(name='Station 1', latitude=1.0, longitude=1.0),
                                           destination=Station.objects.create(name='Station 2', latitude=2.0, longitude=2.0))
        self.train_type = TrainType.objects.create(name="Passenger")
        self.train = Train.objects.create(name="Express", carriage_num=10, places_in_carriage=20, train_type=self.train_type)
        self.crew = Crew.objects.create(first_name='John', last_name='Doe')
        self.journey = Journey.objects.create(route=self.route, train=self.train, departure_time="2024-06-05T18:50:25.928493Z", arrival_time="2024-06-06T18:50:25.928493Z")
        self.journey.crews.add(self.crew)

    def test_list_journeys(self):
        response = self.client.get('/api/v1/journeys/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), Journey.objects.count())

    def test_retrieve_journey(self):
        journey_id = self.journey.id
        response = self.client.get(f'/api/v1/journeys/{journey_id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['route']['source']['name'], self.journey.route.source.name)
        self.assertEqual(response.data['route']['destination']['name'], self.journey.route.destination.name)
        self.assertEqual(response.data['train']['name'], self.journey.train.name)
        self.assertEqual(response.data['departure_time'], "2024-06-05T18:50:25.928493Z")
        self.assertEqual(response.data['arrival_time'], "2024-06-06T18:50:25.928493Z")


class OrderViewSetTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.order = Order.objects.create(user=self.user)

    def test_list_orders(self):
        response = self.client.get('/api/v1/orders/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), Order.objects.count())

    def test_retrieve_order(self):
        order_id = self.order.id
        response = self.client.get(f'/api/v1/orders/{order_id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user']['username'], self.order.user.username)


class TicketViewSetTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.train_type = TrainType.objects.create(name="Passenger")
        self.train = Train.objects.create(name="Express", carriage_num=10, places_in_carriage=20, train_type=self.train_type)
        self.station1 = Station.objects.create(name="Station 1", latitude=1.0, longitude=1.0)
        self.station2 = Station.objects.create(name="Station 2", latitude=2.0, longitude=2.0)
        self.route = Route.objects.create(source=self.station1, destination=self.station2)
        self.journey = Journey.objects.create(route=self.route, train=self.train, departure_time="2024-06-05T18:50:25.928493Z", arrival_time="2024-06-06T18:50:25.928493Z")
        self.seat = Seat.objects.create(train=self.train, seat=1, carriage=1, is_available=True)
        self.order = Order.objects.create(user=self.user)
        self.ticket1 = Ticket.objects.create(train=self.train, seat=self.seat, journey=self.journey, order=self.order)
        self.ticket2 = Ticket.objects.create(train=self.train, seat=self.seat, journey=self.journey, order=self.order)

    def test_list_tickets(self):
        response = self.client.get('/api/v1/tickets/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_ticket(self):
        ticket_id = self.ticket1.id
        response = self.client.get(f'/api/v1/tickets/{ticket_id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
