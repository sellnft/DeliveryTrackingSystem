from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from .forms import OrderForm
from .models import Order, Route


@login_required
def order_list(request):
    user = request.user
    if user.role == user.Role.COURIER:
        orders = Order.objects.filter(courier=user)
    else:
        orders = Order.objects.filter(client=user)
    orders = orders.select_related("client", "courier", "route")
    return render(request, "orders/list.html", {"orders": orders})


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(
        Order.objects.select_related("client", "courier", "route"),
        id=order_id,
    )
    return render(request, "orders/detail.html", {"order": order})


@login_required
@require_http_methods(["GET", "POST"])
def order_create(request):
    if request.user.role != request.user.Role.CLIENT:
        messages.error(request, "Только клиент может создать заказ")
        return redirect("orders-list")

    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            amount = Decimal(str(form.cleaned_data["total_amount"]))
            with transaction.atomic():
                route = Route.objects.create(
                    origin_address=form.cleaned_data["origin"],
                    delivery_address=form.cleaned_data["destination"],
                )
                order = Order.objects.create(
                    client=request.user,
                    route=route,
                    description=form.cleaned_data["description"],
                    total_amount=amount,
                )
            messages.success(request, f"Заказ #{order.id} создан")
            return redirect("order-detail", order_id=order.id)
    else:
        form = OrderForm()

    return render(request, "orders/create.html", {"form": form})


@login_required
@require_http_methods(["POST"])
def change_status(request, order_id):
    if request.user.role not in (request.user.Role.COURIER, request.user.Role.MODERATOR):
        messages.error(request, "Нет прав")
        return redirect("order-detail", order_id=order_id)

    order = get_object_or_404(Order, id=order_id)
    new_status = request.POST.get("status")

    valid_statuses = {choice.value for choice in Order.Status}
    if new_status not in valid_statuses:
        messages.error(request, "Некорректный статус")
        return redirect("order-detail", order_id=order_id)

    order.status = new_status
    order.save(update_fields=["status", "updated_at"])

    messages.success(request, f"Статус изменён на «{order.get_status_display()}»")
    return redirect("order-detail", order_id=order.id)
