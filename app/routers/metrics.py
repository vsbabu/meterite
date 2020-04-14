from fastapi import APIRouter, Depends, HTTPException
from fastapi.security.api_key import APIKey

from typing import List
from sqlalchemy.orm import Session

from .. import crud, models, schemas
from ..database import get_db
from ..security import get_api_key

from ..config import logger

router = APIRouter()


@router.get("/", response_model=List[schemas.Metric])
async def read_metrics(
    limit: int = 100, org: APIKey = Depends(get_api_key), db: Session = Depends(get_db)
) -> List[schemas.Metric]:
    return await crud.get_metrics(db, org=org, limit=limit)


@router.post("/", response_model=schemas.Metric)
async def create_metric(
    metric: schemas.MetricBase,
    org: APIKey = Depends(get_api_key),
    db: Session = Depends(get_db),
) -> schemas.Metric:
    db_rec = await crud.get_metric_by_code(db, org=org, code=metric.code)
    if db_rec:
        logger.error(f"{metric.code}@{org} is already registered")
        raise HTTPException(status_code=409, detail="Metric already registered")
    return await crud.create_metric(db=db, org=org, metric=metric)


@router.post("/{code}/activate", response_model=schemas.Metric)
async def activate_metric(
    code: str, org: APIKey = Depends(get_api_key), db: Session = Depends(get_db)
) -> schemas.Metric:
    metric = await crud.update_active_flag(db=db, org=org, code=code, active=True)
    return metric


@router.post("/{code}/deactivate", response_model=schemas.Metric)
async def deactivate_metric(
    code: str, org: APIKey = Depends(get_api_key), db: Session = Depends(get_db)
) -> schemas.Metric:
    metric = await crud.update_active_flag(db=db, org=org, code=code, active=False)
    return metric


@router.put("/{code}", response_model=schemas.Metric)
async def modify_metric(
    metric: schemas.MetricBase,
    org: APIKey = Depends(get_api_key),
    db: Session = Depends(get_db),
) -> schemas.Metric:
    metric = await crud.update_metric(db=db, org=org, metric=metric, active=False)
    return metric


@router.delete("/{code}", response_model=schemas.Metric)
async def delete_metric(
    code: str, org: APIKey = Depends(get_api_key), db: Session = Depends(get_db)
) -> schemas.Metric:
    metric = await crud.delete_metric(db=db, org=org, code=code)
    logger.info(f"{metric.code}@{org} is deleted")
    return metric


@router.get("/{code}", response_model=schemas.Metric)
async def get_metric(
    code: str, org: APIKey = Depends(get_api_key), db: Session = Depends(get_db)
) -> schemas.Metric:
    return await crud.get_metric_by_code(db=db, org=org, code=code, meters=True)
