from django.urls import path

from . import views

app_name = "products"

urlpatterns = [
    path("menus/", views.MenuListView.as_view(), name="menu-list"),
]
