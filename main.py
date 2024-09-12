from enum import Enum
from typing import Annotated

from fastapi import FastAPI, HTTPException, Body
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, ConfigDict

from lis_service import lis_service, LisServiceObjectNotFound

app = FastAPI()


class CollectionResult(str, Enum):
    filled = "filled"
    partial_filled = "partial_filled"
    empty = "empty"


class ProcedureResult(str, Enum):
    success = "success"
    partial_success = "partial_success"
    failure = "failure"


class Patient(BaseModel):
    id: int


class Collector(BaseModel):
    id: int
    sequence: int
    collection_result: CollectionResult


class BaseProcedure(BaseModel):
    id: int
    subject: Patient


class DetailedProcedure(BaseProcedure):
    collectors: list[Collector]
    collection_result: ProcedureResult


class ProcedureInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    collectors: list[Collector] | None = None
    collection_result: ProcedureResult | None = None


@app.get("/collectors/{tube_id}/procedure-info")
def get_procedure_info(tube_id: int):
    try:
        procedure_json = lis_service.get_procedure_by_collector_id(tube_id)
        return {"procedure": BaseProcedure(**procedure_json)}
    except LisServiceObjectNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.get("/procedures/{procedure_id}/collection-info")
def get_collection_info(procedure_id: int):
    try:
        procedure_json = lis_service.get_procedure_by_procedure_id(procedure_id)
        return {"procedure": DetailedProcedure(**procedure_json)}
    except LisServiceObjectNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.patch("/procedures/{procedure_id}/collection-info")
def patch_procedure_collection_info(procedure_id: int, procedure: Annotated[ProcedureInput, Body(embed=True)]):
    # Assume LIS system doesn't support partial updates but only complete overrides
    try:
        procedure_json = lis_service.get_procedure_by_procedure_id(procedure_id)
        procedure_obj = DetailedProcedure(**procedure_json)

        update_data = procedure.model_dump(exclude_defaults=True)

        updated_procedure = procedure_obj.model_copy(update=update_data)

        updated_procedure_json = lis_service.update_procedure(procedure_id, jsonable_encoder(updated_procedure))

        return {"procedure": DetailedProcedure(**updated_procedure_json)}
    except LisServiceObjectNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))
