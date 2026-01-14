from django.urls import path

from . import views

app_name = "products"

urlpatterns = [
    path("menus/", views.MenuListCreateView.as_view(), name="menu-list-create"),
]
