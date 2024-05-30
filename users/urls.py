from django.urls import path

from users.constants import DEFAULT_LIST_ACTIONS, DEFAULT_DETAIL_ACTIONS
from users.views import UserViewSet, ManageUserView

urlpatterns = [
    path("users/", UserViewSet.as_view(DEFAULT_LIST_ACTIONS), name="user_list"),
    path("users/<int:pk>", UserViewSet.as_view(DEFAULT_DETAIL_ACTIONS), name="user_detail"),
    path("me/", ManageUserView.as_view(), name="manage_user"),
]

app_name = "users"
