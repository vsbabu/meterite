from sqlalchemy import (
    Column,
    Index,
    ForeignKey,
    UniqueConstraint,
    Boolean,
    Integer,
    String,
    DateTime,
)
from sqlalchemy.orm import relationship, backref

from .database import Base


class Metric(Base):
    __tablename__ = "metric"

    id = Column(Integer, primary_key=True, index=True)
    org = Column(String(32), index=True)
    code = Column(String(32))
    name = Column(String(96))
    active = Column(Boolean, default=True)
    min_reading = Column(Integer, default=-99999999)
    max_reading = Column(Integer, default=99999999)
    truncate_reading_to = Column(String(32))
    current_reading = Column(Integer)
    current_reading_at = Column(DateTime)
    last_reading = Column(Integer)
    last_reading_at = Column(DateTime)

    meters = relationship(
        "Meter",
        cascade="all,delete",
        back_populates="metric",
        lazy="noload",
        order_by="Meter.reading_at.desc()",
    )


class Meter(Base):
    __tablename__ = "meter"

    id = Column(Integer, primary_key=True, index=True)
    metric_id = Column(Integer, ForeignKey("metric.id"), index=True)
    reading = Column(Integer)
    reading_at = Column(DateTime)
    recorded_at = Column(DateTime)

    metric = relationship("Metric", backref=backref("meter", cascade="all,delete"))

    __table_args__ = (
        Index("idx_meter_reading", "metric_id", "reading_at"),
        UniqueConstraint("metric_id", "reading_at"),
    )
