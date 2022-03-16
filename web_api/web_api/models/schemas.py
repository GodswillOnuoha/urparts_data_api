from typing import Optional
from pydantic import BaseModel
from web_api.models.models import MachineModel, MachinePart


class PartResponse(MachineModel, MachinePart):
    pass


class QueryOptions(BaseModel):
    category: Optional[str] = None
    manufacturer: Optional[str] = None
    machine_type: Optional[str] = None
    part_number: Optional[str] = None
    machine_model: Optional[str] = None
