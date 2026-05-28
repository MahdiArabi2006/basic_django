from . import views
from rest_framework import routers
from django.urls import path,include

app_name = "users-v1"

router = routers.DefaultRouter()
router.register(r"users", views.CustomUserView, basename="user")

urlpatterns = [
    path("users/register/",views.RegisterUserAPIView.as_view(),name="register"),
    path("users/login/",views.LoginAPIView.as_view(),name="login"),
    path("users/logout/",views.LogoutView.as_view(),name="logout"),
]

urlpatterns += router.urls