from fastapi import FastAPI
from controller import book_controller,user_controller
from repositories.base import Base,engine
from core.logging_config import setup_logging,RequestLoggingMiddleware
import logging

app=FastAPI(title="Bookstore API",version="1.0")

# Setup logging once
setup_logging()

# Add middleware
app.add_middleware(RequestLoggingMiddleware)
 
# checking database tables
Base.metadata.create_all(bind=engine)  # creates if not exists
    
#include routes
app.include_router(user_controller.router)
app.include_router(book_controller.router)

@app.get("/")
def root():
    logging.getLogger("app").info("Root endpoint hit")
    return {"message":"Welcome to the Bookstore API"}