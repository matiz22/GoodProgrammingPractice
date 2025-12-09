from pydantic import BaseModel, constr

class UserCreate(BaseModel):
    username: constr(min_length=3, max_length=150)
    password: constr(min_length=6)

class UserOut(BaseModel):
    id: int
    username: str
    is_admin: bool = False