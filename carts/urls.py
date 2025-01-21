from django.urls import path
from . import views

urlpatterns = [
    path("", views.cart, name="cart"),
    path("add_cart/<int:product_id>/", views.add_cart, name="add_cart"),
    path("remove_cart/<int:product_id>/", views.remove_cart, name="remove_cart"),
    path("delete_all_items_in_cart/<int:product_id>/", views.delete_all_items_in_cart, name="delete_all_items_in_cart"),
]