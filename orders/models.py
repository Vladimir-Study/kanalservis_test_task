from pydantic import BaseModel
from datetime import date
from sqlalchemy import Table, MetaData, Integer, Float, DateTime
from sqlalchemy.orm import Session, DeclarativeBase, Mapped, mapped_column
from datetime import datetime
import sqlalchemy as db

engine = db.create_engine(f"postgresql+psycopg2://admin:"
                          f"admin@db:"
                          f"5432/orders")

metadata = MetaData()
session = Session(bind=engine)


class Base(DeclarativeBase):
    pass


class OrdersDb(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    order_number: Mapped[int] = mapped_column(Integer)
    price_dollar: Mapped[float] = mapped_column(Float)
    price_rur: Mapped[float] = mapped_column(Float)
    delivery_date: Mapped[datetime] = mapped_column(DateTime)

    def __repr__(self) -> str:
        return f"[{self.id}, {self.order_number}, {self.price_dollar}, {self.price_rur}, {self.delivery_date}]"


class OrdersApi(BaseModel):
    order_number: int
    price_dollar: float
    price_rur: float
    delivery_date: date


if __name__ == "__main__":
    pass
