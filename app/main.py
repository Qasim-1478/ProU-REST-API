from fastapi import FastAPI
from .router import employees, tasks
from .models import create_db_and_tables
from contextlib import asynccontextmanager
import logging

# Basic logging configuration for the application
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("prou")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup code
    create_db_and_tables()
    logger.info("Database tables created / verified")
    yield
    # Shutdown code
    logger.info("Shutting down application")

app = FastAPI(lifespan=lifespan)

@app.get("/")
def main():
    return {"message": "Hello World"}

app.include_router(employees.router)
app.include_router(tasks.router)
