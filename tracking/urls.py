from django.urls import path
from . import views

app_name = "tracking"

urlpatterns = [
    path("orders/", views.order_list, name="orders-list"),
    path("orders/create/", views.order_create, name="orders-create"),
    path("orders/<int:order_id>/", views.order_detail, name="order-detail"),
    path("orders/<int:order_id>/status/", views.change_status, name="order-change-status"),
]
