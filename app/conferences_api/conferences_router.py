from fastapi import FastAPI, HTTPException, Request, status, Body
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from conferences_service.conferencer import ConferenceCRUD
import json

app = FastAPI()
conference_crud = ConferenceCRUD()


@app.post("/conferences/", response_model=str)
async def create_conference(conference_data: dict = Body(...)):
    try:
        conference_id = conference_crud.create_conference(conference_data)
    except:
        raise HTTPException(
            status_code=400, detail="Conference created unsuccessfully (missing details)")
    return conference_id


@app.get("/get_all")
async def get_all():
    try:
        conferences = conference_crud.read_all()
        # print(conferences)
    except:
        raise HTTPException(
            status_code=400, detail="Some problems")
    return conferences


@app.get("/conferences")
async def read_conference(conference_id: str):
    try:
        conference = conference_crud.read_conference(conference_id)
        if conference:
            return conference
    except:
        raise HTTPException(
            status_code=400, detail="Conference founded unsuccessfully (bad id)")
    raise HTTPException(status_code=404, detail="Conference not found")


@app.put("/conferences")
async def update_conference(conference_id: str, updated_data: dict = Body(...)):
    try:
        updated_count = conference_crud.update_conference(
            conference_id, updated_data)
    except:
        raise HTTPException(
            status_code=400, detail="Conference updated unsuccessfully (bad id)")
    if updated_count:
        return updated_count
    else:
        raise HTTPException(
            status_code=400, detail="Нечего обновлять или конференция не найдена")


@app.delete("/conferences")
async def delete_conference(conference_id: str):
    try:
        deleted_count = conference_crud.delete_conference(conference_id)
        if deleted_count:
            return deleted_count
    except:
        raise HTTPException(
            status_code=400, detail="Conference deleted unsuccessfully (bad id)")
    raise HTTPException(status_code=404, detail="Conference not found")
