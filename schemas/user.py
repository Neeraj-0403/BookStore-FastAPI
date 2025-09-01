from pydantic  import BaseModel,EmailStr

class UserCreate(BaseModel):
    email:EmailStr
    username:str
    password:str

class Token(BaseModel):
    access_token:str
    token_type:str="bearer"

class UserLogin(BaseModel):
    email:EmailStr
    password:str

class UserRead(BaseModel):
    id:int
    email:EmailStr
    username:str

    model_config = {
        "from_attributes":True
    }