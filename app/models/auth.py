from pydantic import BaseModel, Field, EmailStr, ValidationInfo, field_validator

class Login(BaseModel):
    email: EmailStr
    password: str = Field(...,min_length=6, max_length=128)


class Register(BaseModel):
    name: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(...,min_length=6, max_length=128)
    confirm_password: str = Field(...,min_length=6, max_length=128)


    @field_validator("confirm_password")
    @classmethod
    def password_match(cls, value, info: ValidationInfo):
        if "password" in info.data and value != info.data["password"]:
            raise ValueError("Password do not match")
        return value
    
