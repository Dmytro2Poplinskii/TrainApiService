from django.db import models
from django.contrib.auth.models import User

from .utils import train_image_path


class Crew(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class TrainType(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Station(models.Model):
    name = models.CharField(max_length=50)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return self.name


class Order(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Order for {self.user.username}. Date: {self.created_date}"


class Train(models.Model):
    name = models.CharField(max_length=50)
    cargo_num = models.IntegerField(null=True)
    places_in_cargo = models.IntegerField(null=True)
    train_type = models.ForeignKey(TrainType, on_delete=models.CASCADE)
    num_seats = models.IntegerField(null=True)
    image = models.ImageField(upload_to=train_image_path, null=True)

    def __str__(self):
        return f"{self.name}. {self.cargo_num} {self.places_in_cargo}"


class Route(models.Model):
    source = models.ForeignKey(Station, on_delete=models.CASCADE, related_name="source_routes")
    destination = models.ForeignKey(Station, on_delete=models.CASCADE, related_name="destination_routes")
    distance = models.IntegerField()

    @property
    def full_route(self):
        return f"{self.source.name}-{self.destination.name}"

    def __str__(self):
        return f"Source: {self.source.name}. Destination: {self.destination.name}"


class Journey(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    train = models.ForeignKey(Train, on_delete=models.CASCADE)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    crews = models.ManyToManyField(Crew)

    def __str__(self):
        return (
            f"Route: {self.route}"
            f"Train: {self.train}"
            f"Departure time: {self.departure_time}"
            f"Arrival time: {self.arrival_time}"
        )


class Ticket(models.Model):
    cargo = models.IntegerField()
    seat = models.IntegerField()
    journey = models.ForeignKey(Journey, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

    def __str__(self):
        return f"Cargo: {self.cargo}. Seat: {self.seat}. Journey: {self.journey}. Order: {self.order}"
