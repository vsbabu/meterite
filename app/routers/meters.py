from fastapi import APIRouter, Depends
from fastapi.security.api_key import APIKey

from sqlalchemy.orm import Session

from .. import crud, models, schemas
from ..database import get_db
from ..security import get_api_key

router = APIRouter()


@router.post("/{code}", response_model=schemas.Meter)
async def record_meter(
    code: str,
    meter: schemas.MeterBase,
    org: APIKey = Depends(get_api_key),
    db: Session = Depends(get_db),
) -> schemas.Meter:
    metric = await crud.get_metric_by_code(db, org=org, code=code)
    if not metric:
        raise HTTPException(status_code=404, detail="Metric is not found")
    return await crud.create_meter(db, metric, meter)
