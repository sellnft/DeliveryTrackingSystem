from sqlalchemy import Integer, String, Boolean, DateTime, func, Enum
from sqlalchemy.orm import relationship, Mapped, mapped_column

import enum
from datetime import datetime
from typing import TYPE_CHECKING

from models.base import Base

if TYPE_CHECKING:
    from models.order import Order


class UserRole(str, enum.Enum):
    CLIENT = "client"
    COURIER = "courier"
    MODERATOR = "moderator"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(
        String, unique=True, nullable=False, index=True)
    password_hash: Mapped[str] = mapped_column(String, nullable=False)
    full_name: Mapped[str] = mapped_column(String, nullable=False)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole, values_callable=lambda x: [
                                               e.value for e in x]), default=UserRole.CLIENT, nullable=False)

    email: Mapped[str | None] = mapped_column(
        String, unique=True, nullable=True)
    phone: Mapped[str | None] = mapped_column(
        String, unique=True, nullable=True)

    is_active: Mapped[bool] = mapped_column(
        Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), nullable=False)

    client_orders: Mapped[list["Order"]] = relationship(
        "Order",
        back_populates="client",
        foreign_keys="[Order.client_id]"
    )

    courier_orders: Mapped[list["Order"]] = relationship(
        "Order",
        back_populates="courier",
        foreign_keys="[Order.courier_id]"
    )
