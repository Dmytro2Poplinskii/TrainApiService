# Generated by Django 5.0.4 on 2024-06-03 06:53

import django.db.models.deletion
import train_api.utils
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Crew",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("first_name", models.CharField(max_length=50)),
                ("last_name", models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name="Route",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Seats",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("seat", models.IntegerField()),
                ("carriage", models.IntegerField()),
                ("is_available", models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name="Station",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=50)),
                ("latitude", models.FloatField()),
                ("longitude", models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name="Train",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=50)),
                ("carriage_num", models.IntegerField(null=True)),
                ("places_in_carriage", models.IntegerField(null=True)),
                (
                    "image",
                    models.ImageField(
                        null=True, upload_to=train_api.utils.train_image_path
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="TrainType",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name="Order",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_date", models.DateTimeField(auto_now_add=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Journey",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("departure_time", models.DateTimeField()),
                ("arrival_time", models.DateTimeField()),
                ("crews", models.ManyToManyField(to="train_api.crew")),
                (
                    "route",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="train_api.route",
                    ),
                ),
                (
                    "train",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="train_api.train",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="route",
            name="destination",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="destination_routes",
                to="train_api.station",
            ),
        ),
        migrations.AddField(
            model_name="route",
            name="source",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="source_routes",
                to="train_api.station",
            ),
        ),
        migrations.CreateModel(
            name="Ticket",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "journey",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="train_api.journey",
                    ),
                ),
                (
                    "order",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="train_api.order",
                    ),
                ),
                (
                    "seat",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="train_api.seats",
                    ),
                ),
                (
                    "train",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="train_api.train",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="seats",
            name="train",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="train_api.train"
            ),
        ),
        migrations.AddField(
            model_name="train",
            name="train_type",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="train_api.traintype"
            ),
        ),
    ]
