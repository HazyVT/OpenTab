from pydantic import BaseModel

class NewTab(BaseModel):
    id: int
    title: str