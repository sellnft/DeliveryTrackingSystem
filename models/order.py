from sqlalchemy import Integer, String, ForeignKey, DateTime, Numeric, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from models.base import Base

if TYPE_CHECKING:
    from models.user import User
    from models.route import Route


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True)

    client_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=False)

    courier_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=True)

    route_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("routes.id"),
        nullable=False,
        unique=True
    )

    description: Mapped[str] = mapped_column(String, nullable=False)
    total_amount: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now())

    updated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now()
    )

    client: Mapped["User"] = relationship(
        "User",
        back_populates="client_orders",
        foreign_keys=[client_id]
    )

    courier: Mapped[Optional["User"]] = relationship(
        "User",
        back_populates="courier_orders",
        foreign_keys=[courier_id]
    )

    route: Mapped["Route"] = relationship(
        "Route",
        back_populates="order",
        uselist=False
    )
