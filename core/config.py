from pydantic_settings import BaseSettings
 
class Settings(BaseSettings):
    APP_NAME: str = "Bookstore API"
    ENV: str = "dev"
    DEBUG: bool = True
    CONNECTION_STRING: str = (
        "Driver={ODBC Driver 17 for SQL Server};"
        "Server=DITSDEV293\\SQLEXPRESS;"
        "Database=BookStore;"
        "Trusted_Connection=yes;"
    )
    DATABASE_URL: str =  "mssql+pyodbc:///?odbc_connect={}".format(CONNECTION_STRING.replace(";", "%3B"))
 
    JWT_SECRET: str = "change_me" # it can be changeable as per our requirement 
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRES_MIN: int = 60


    LOG_LEVEL: str = "INFO" 

    class Config:
        env_file = ".env"


settings = Settings()