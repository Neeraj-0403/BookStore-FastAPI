from dataclasses import dataclass 

@dataclass
class UserEntity:
    email:str = ""
    username:str = ""
    password:str = ""
