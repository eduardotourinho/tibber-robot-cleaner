from fastapi import FastAPI

from .adapters.api.routes import router as cleaner_router

app = FastAPI()
app.include_router(cleaner_router)
