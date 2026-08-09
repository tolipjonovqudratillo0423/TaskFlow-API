from pydantic import BaseModel, field_validator, EmailStr


class UserCreate(BaseModel):
    
    username: str
    email: EmailStr
    password: str
    phone_number: str
    first_name: str
    last_name: str
    
    @field_validator("username")
    @classmethod
    def username_validation(cls, value: str) -> str:
        
        if len(value.strip()) <= 3: 
            raise ValueError("Username is too short!")
        
        return value.strip()
    

class UserRead(BaseModel):
    
    id: int
    username: str
    email: EmailStr
    phone_number: str
    first_name: str
    last_name: str
    is_active: bool
    


class Login(BaseModel):
    
    email: EmailStr
    password: str