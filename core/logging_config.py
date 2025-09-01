import logging
from logging.handlers import RotatingFileHandler
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

def setup_logging(level:str="INFO",log_file: str = "app.log"):
     # Root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, level.upper(), logging.INFO))

    # Clear existing handlers
    if root_logger.hasHandlers():
        root_logger.handlers.clear()

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    ))

    # File handler
    file_handler = RotatingFileHandler(
        log_file, maxBytes=5*1024*1024, backupCount=3, encoding="utf-8"
    )
    file_handler.setFormatter(logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    ))

    # Add handlers to root logger
    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)

    # Optional: make all child loggers propagate to root
    logging.getLogger("app").propagate = True
     
    logging.basicConfig(
        level=getattr(logging,level.upper(),logging.info),
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

# logger middleware
class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        try:
            logger=logging.getLogger("request")
            logger.info(f"{request.method}{request.url.path}")
            response= await call_next(request)
            return response
        except Exception as ex:
            logger.error(f"Exception from request : {ex}")
            return {
                statuscode:500,
                error_message: "Internal server error"
            }