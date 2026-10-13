from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):

    class Role(models.TextChoices):
        CLIENT = "client", "Клиент"
        COURIER = "courier", "Курьер"
        MODERATOR = "moderator", "Модератор"

    full_name = models.CharField("ФИО", max_length=150, blank=True)
    role = models.CharField(
        "Роль",
        max_length=16,
        choices=Role.choices,
        default=Role.CLIENT,
    )
    phone = models.CharField(
        "Телефон",
        max_length=20,
        unique=True,
        null=True,
        blank=True,
    )
    email = models.EmailField("Email", null=True, blank=True)

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
