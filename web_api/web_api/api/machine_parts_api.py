from typing import List, Optional
from fastapi import APIRouter, Depends, Query, Response

from web_api.services import machine_parts_service
from web_api.models.schemas import QueryOptions, PartResponse

router = APIRouter()


@router.get("/api/parts", response_model=List[PartResponse])
async def get_parts(
    query: QueryOptions = Depends(),
    offset: Optional[int] = Query(0, ge=0),
    limit: Optional[int] = Query(5, ge=1),
):
    try:
        return await machine_parts_service.get_parts(query, offset, limit)
    except Exception as error:
        return Response(content=str(error), status_code=500)
