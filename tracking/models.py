from django.db import models
from django.conf import settings


class Route(models.Model):

    origin_address = models.CharField("Откуда", max_length=255)
    delivery_address = models.CharField("Куда", max_length=255)

    class Meta:
        verbose_name = "Маршрут"
        verbose_name_plural = "Маршруты"


class Order(models.Model):

    class Status(models.TextChoices):
        CREATED = "created", "Создан"
        ACCEPTED = "accepted", "Принят курьером"
        IN_TRANSIT = "in_transit", "В пути"
        DELIVERED = "delivered", "Доставлен"
        CANCELLED = "cancelled", "Отменён"

    client = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="client_orders",
        verbose_name="Клиент",
    )
    courier = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="courier_orders",
        null=True,
        blank=True,
        verbose_name="Курьер",
    )
    route = models.OneToOneField(
        "Route",
        on_delete=models.PROTECT,
        related_name="order",
        verbose_name="Маршрут",
    )

    description = models.TextField("Описание", blank=True)
    total_amount = models.DecimalField(
        "Сумма",
        max_digits=10,
        decimal_places=2,
    )
    status = models.CharField(
        "Статус",
        max_length=16,
        choices=Status.choices,
        default=Status.CREATED,
    )

    created_at = models.DateTimeField("Создан", auto_now_add=True)
    updated_at = models.DateTimeField("Обновлён", auto_now=True)

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        ordering = ["-created_at"]
