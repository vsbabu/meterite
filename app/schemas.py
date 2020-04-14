from typing import List, Optional
from pydantic import BaseModel, Field, validator
import datetime


class MeterBase(BaseModel):
    reading: int
    reading_at: Optional[datetime.datetime] = None

    if False:
        pass
        # import dataclasses
        # from pydantic.dataclasses import dataclass
        # =   dataclasses.field(default_factory=datetime.datetime.now)
        # = Field(default_factory=datetime.datetime.now)
        # setting default is easy like above once we upgrade pydantic

    @validator("reading_at", pre=True, always=True)
    def set_reading_at_now(cls, v):
        return v or datetime.datetime.now()


class Meter(MeterBase):
    metric_id: int
    recorded_at: datetime.datetime = datetime.datetime.now()

    class Config:
        orm_mode = True


class MetricBase(BaseModel):
    code: str
    name: str
    min_reading: int = -9999999
    max_reading: int = 9999999
    truncate_reading_to: Optional[str] = Field(
        None,
        description="Given reading time is truncated to this and upserted. See https://pypi.org/project/datetime_truncate/ for values.",
    )

    @validator("code")
    def code_must_be_good(cls, v: str):
        if not v.strip().upper().isascii():
            raise ValueError("must contain only alphanumeric and _")
        return v.strip().upper()


class Metric(MetricBase):
    id: int
    org: str
    active: bool = Field(
        True,
        description="Only active metrics can have meters; and it has to be deactivated before deletion.",
    )
    current_reading: Optional[int]
    current_reading_at: Optional[datetime.datetime]
    last_reading: Optional[int]
    last_reading_at: Optional[datetime.datetime]

    meters: Optional[List[Meter]]

    class Config:
        orm_mode = True
