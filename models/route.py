from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.order import Order


class Route(Base):
    __tablename__ = "routes"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True)

    order_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("orders.id", ondelete="CASCADE"),
        nullable=False,
        unique=True
    )

    origin_address: Mapped[str] = mapped_column(String, nullable=False)
    delivery_address: Mapped[str] = mapped_column(String, nullable=False)

    order: Mapped["Order"] = relationship(
        "Order",
        back_populates="route"
    )
