from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView

from . import views

app_name = "users"

urlpatterns = [
    path("signup/", views.SignUpView.as_view(), name="signup"),
    path("login/", TokenObtainPairView.as_view(), name="login"),
    path("genders/", views.GenderListView.as_view(), name="gender-list"),
    path("profile/", views.ProfileView.as_view(), name="profile"),
]
