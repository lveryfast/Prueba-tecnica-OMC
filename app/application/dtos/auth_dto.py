from pydantic import BaseModel, EmailStr


class LoginDto(BaseModel):
    email: EmailStr
    password: str


class LoginResponseDto(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user: dict