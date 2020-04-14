from sqlalchemy.orm import Session

# https://fastapi.tiangolo.com/tutorial/sql-databases/
from . import models, schemas
from typing import List, Optional

from sqlalchemy.orm import lazyload

import datetime
from datetime_truncate import truncate

from .config import logger


async def get_metric(db: Session, org: str, id: int) -> models.Metric:
    return (
        db.query(models.Metric)
        .options(lazyload(models.Metric.meters))
        .filter(models.Metric.id == id)
        .filter(models.Metric.org == org)
        .first()
    )


async def get_metrics(db: Session, org: str, limit: int = 100) -> List[models.Metric]:
    # TODO: remove the meters in this; let meters be available only on access by id
    return db.query(models.Metric).filter(models.Metric.org == org).limit(limit).all()


async def get_metric_by_code(
    db: Session, org: str, code: str, meters: bool = False
) -> models.Metric:
    # .order_by(models.Meter.reading_at.desc())
    if meters:
        return (
            db.query(models.Metric)
            .options(lazyload(models.Metric.meters))
            .filter(models.Metric.org == org)
            .filter(models.Metric.code == code)
            .first()
        )
    else:
        return (
            db.query(models.Metric)
            .filter(models.Metric.org == org)
            .filter(models.Metric.code == code)
            .first()
        )


async def create_metric(
    db: Session, org: str, metric: schemas.MetricBase
) -> models.Metric:
    r = await get_metric_by_code(db, org, metric.code)
    if r is not None:
        raise Exception("record already exists")  # TODO: nice it
    # TODO: ensure metric.truncate_reading_to is valid
    db_rec = models.Metric(
        org=org,
        code=metric.code,
        name=metric.name,
        active=True,
        min_reading=metric.min_reading,
        max_reading=metric.max_reading,
        truncate_reading_to=metric.truncate_reading_to,
    )
    db.add(db_rec)
    db.commit()
    db.refresh(db_rec)
    return db_rec


async def update_metric(
    db: Session, org: str, metric: schemas.MetricBase
) -> models.Metric:
    db_rec = await get_metric_by_code(db, org, metric.code)
    if db_rec is not None:
        db_rec.name = metric.name
        db_rec.min_reading = metric.min_reading
        db_rec.max_reading = metric.max_reading
        db_rec.truncate_reading_at = metric.truncate_reading_at
        db.commit()
        db.refresh(db_rec)
    return db_rec


async def delete_metric(db: Session, org: str, code: str) -> models.Metric:
    metric = await get_metric_by_code(db, org, code, meters=True)
    if metric.active:
        raise Exception(
            f"{code}@{org} already has active={active}. Deactivate first before deletion."
        )
    if metric is not None:
        db.delete(metric)
        db.commit()
    return metric


async def update_active_flag(
    db: Session, org: str, code: str, active: bool = True
) -> models.Metric:
    metric = await get_metric_by_code(db, org, code, meters=False)
    if metric.active == active:
        raise Exception(f"{code}@{org} already has active={active}")
    metric.active = active
    db.commit()
    db.refresh(metric)
    return metric


async def create_meter(
    db: Session, metric: schemas.Metric, meter: schemas.MeterBase
) -> models.Meter:
    if metric is None:
        raise Exception("Need a metric before meter")  # TODO: nice it
    if metric.truncate_reading_to is not None:
        meter.reading_at = truncate(
            meter.reading_at, truncate_to=metric.truncate_reading_to
        )
        # FIXME: this can cause exception due to  invalid truncate_reading_to values
    db_rec = (
        db.query(models.Meter)
        .filter(models.Meter.metric_id == metric.id)
        .filter(models.Meter.reading_at == meter.reading_at)
        .first()
    )
    is_reading_changed = False
    if db_rec is not None:
        if db_rec.reading != meter.reading:
            db_rec.reading = meter.reading
            db_rec.recorded_at = datetime.datetime.now()
            is_reading_changed = True
            logger.info(f"{metric.code}@{metric.org} reading overwritten")
    else:
        db_rec = models.Meter(
            metric_id=metric.id,
            reading_at=meter.reading_at,
            reading=meter.reading,
            recorded_at=datetime.datetime.now(),
        )
        db.add(db_rec)
        is_reading_changed = True
    # update last metric values too
    db_metric = await get_metric(db, org=metric.org, id=metric.id)
    if is_reading_changed:
        db_metric.last_reading = db_metric.current_reading
        db_metric.last_reading_at = db_metric.current_reading_at
        db_metric.current_reading = db_rec.reading
        db_metric.current_reading_at = db_rec.reading_at
    db.commit()
    db.refresh(db_rec)
    return db_rec
