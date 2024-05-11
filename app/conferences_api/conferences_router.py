from fastapi import Body, FastAPI, HTTPException
from pydantic import BaseModel
from conferences_service.conferencer import ConferenceCRUD

app = FastAPI()
conference_crud = ConferenceCRUD()


@app.post("/conferences/", response_model=str)
async def create_conference(conference_data: dict = Body(...)):
    conference_id = conference_crud.create_conference(conference_data)
    return conference_id


@app.get("/conferences/{conference_id}/", response_model=dict)
async def read_conference(conference_id: str):
    conference = conference_crud.read_conference(conference_id)
    if conference:
        return conference
    raise HTTPException(status_code=404, detail="Conference not found")


@app.put("/conferences/{conference_id}/", response_model=int)
async def update_conference(conference_id: str, updated_data: dict = Body(...)):
    updated_count = conference_crud.update_conference(
        conference_id, updated_data)
    if updated_count:
        return updated_count
    raise HTTPException(status_code=404, detail="Conference not found")


@app.delete("/conferences/{conference_id}/", response_model=int)
async def delete_conference(conference_id: str):
    deleted_count = conference_crud.delete_conference(conference_id)
    if deleted_count:
        return deleted_count
    raise HTTPException(status_code=404, detail="Conference not found")
