from django.urls import path, include
from rest_framework.routers import DefaultRouter

from train_api.views import (
    CrewViewSet,
    StationViewSet,
    TrainTypeViewSet,
    TrainViewSet,
    RouteViewSet,
    JourneyViewSet,
    OrderViewSet,
    TicketViewSet,
)

router = DefaultRouter()
router.register(r"crews", CrewViewSet)
router.register(r"stations", StationViewSet)
router.register(r"train-types", TrainTypeViewSet)
router.register(r"trains", TrainViewSet)
router.register(r"routes", RouteViewSet)
router.register(r"journeys", JourneyViewSet)
router.register(r"orders", OrderViewSet)
router.register(r"tickets", TicketViewSet)

urlpatterns = router.urls

app_name = "train_api"
