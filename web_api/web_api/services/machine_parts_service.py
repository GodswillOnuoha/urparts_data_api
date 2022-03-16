import logging
from typing import Dict
from sqlmodel import select

from web_api.settings import sessionLocal as db
from web_api.models.models import (
    MachineModel,
    MachinePart,
    add_query_filters,
)
from web_api.models.schemas import QueryOptions


async def get_parts(query: QueryOptions, offset: int, limit: int):
    query: Dict = {key: value for key, value in query if value is not None}
    statement = (
        select(MachinePart, MachineModel)
        .where(MachinePart.model_id == MachineModel.id)
        .offset(offset)
        .limit(limit)
    )

    statement = add_query_filters(statement, query)

    try:
        results = db.exec(statement).all()
        return [part.dict() | model.dict() for model, part in results]
    except Exception as error:
        logging.error(f"func_get_parts-{query}:{error}")
        raise Exception("error processing request")
