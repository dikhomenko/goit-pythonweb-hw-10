from pydantic import BaseModel, EmailStr


class UserModel(BaseModel):
    username: str
    password: str
    email: EmailStr


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        orm_mode = True


class TokenModel(BaseModel):
    access_token: str
    token_type: str
