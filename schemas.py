from pydantic import BaseModel

class UserCreate(BaseModel):
    name: str
    lastname: str
    age: int
    email: str

class UserResponse(UserCreate):
    id: str

    class Config:
        from_attributes  = True
