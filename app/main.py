from fastapi import FastAPI
from app.api.endpoints import router as router

app=FastAPI()
app.include_router(router,prefix="/apiwhisper")