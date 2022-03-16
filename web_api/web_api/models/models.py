from sqlmodel import SQLModel, Field
from typing import Optional


class MachineModel(SQLModel, table=True):
    __tablename__ = "machine_models"

    id: Optional[int] = Field(default=None, primary_key=True)
    manufacturer: str
    machine_type: str
    machine_model: str


class MachinePart(SQLModel, table=True):
    __tablename__ = "machine_parts"

    id: Optional[int] = Field(default=None, primary_key=True)
    model_id: Optional[int] = Field(default=None, foreign_key="machine_models.id")
    part_number: str
    category: str


def add_query_filters(query_statement, query):
    statement = query_statement

    # Used as a switch case to add WHERE clause to query statement
    add_where_clause = {
        "category": lambda statement, value: statement.where(
            MachinePart.category.ilike(f"%{value}%")
        ),
        "part_number": lambda statement, value: statement.where(
            MachinePart.part_number.ilike(f"%{value}%")
        ),
        "manufacturer": lambda statement, value: statement.where(
            MachineModel.manufacturer.ilike(f"%{value}%")
        ),
        "machine_type": lambda statement, value: statement.where(
            MachineModel.machine_type.ilike(f"%{value}%")
        ),
        "machine_model": lambda statement, value: statement.where(
            MachineModel.machine_model.ilike(f"%{value}%")
        ),
    }

    for key, value in query.items():
        statement = add_where_clause[key](statement, value)

    return statement
