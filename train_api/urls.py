from django.urls import path
from .views import UserViewSet, CrewViewSet, StationViewSet

urlpatterns = [
    path("users/", UserViewSet.as_view(
        {
            "get": "list",
            "post": "create",
        }
    ), name="users"),
    path("crews/", CrewViewSet.as_view({
            "get": "list",
            "post": "create",
        }), name="crews"),
    path("stations/", StationViewSet.as_view({
            "get": "list",
            "post": "create",
    }), name="stations"),
    path("stations/<int:pk>", StationViewSet.as_view({
        "get": "retrieve",
        "put": "update",
        "patch": "partial_update",
        "delete": "destroy"
    }))
]

app_name = "train_api"
