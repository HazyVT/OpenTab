from pydantic import BaseModel

class NewTab(BaseModel):
    id: int
    title: str

class UpdatedTab(BaseModel):
    id: int
    title: str
    url: str
    icon: str
    
class ClosedTab(BaseModel):
    id: int