from pydantic import BaseModel


class Report(BaseModel):
    title: str
    type: str
    text: str
    author_id: int
