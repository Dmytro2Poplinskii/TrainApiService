from django.urls import path

from users.views import UserViewSet, ManageUserView, LoginUserView, CreateUserView


urlpatterns = [
    path("users/", UserViewSet.as_view({
        "get": "list",
        "post": "create",
    }), name="user_list"),
    path(
        "users/<int:pk>",
        UserViewSet.as_view({
            "get": "retrieve",
            "put": "update",
            "patch": "partial_update",
            "delete": "destroy",
        }),
        name="user_detail",
    ),
    path("me/", ManageUserView.as_view(), name="manage_user"),
    path("login/", LoginUserView.as_view(), name="get_token"),
    path("register/", CreateUserView.as_view(), name="login"),
]

app_name = "users"
