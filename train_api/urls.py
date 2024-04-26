from django.urls import path
from .views import UserViewSet


urlpatterns = [
    path("users/", UserViewSet.as_view(
        {
            "get": "list",
            "post": "create",
        }
    ), name="users"),
]

app_name = "train_api"
