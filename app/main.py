from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import logging
from app.core.config import settings
from app.services.scheduler import SchedulerService
from app.integrations.mojo_client import MojoClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="AI Mojo Assistant API",
    description="Backend service for AI-powered educational analytics",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

mojo_client = None
scheduler = None

@app.on_event("startup")
async def startup_event():
    global mojo_client, scheduler
    
    logger.info("Starting AI Mojo Assistant...")
    
    mojo_client = MojoClient(
        base_url=settings.MOJO_BASE_URL,
        api_key=settings.MOJO_API_KEY
    )
    
    scheduler = SchedulerService(mojo_client)
    await scheduler.start()
    
    logger.info("AI Mojo Assistant started successfully")

@app.on_event("shutdown")
async def shutdown_event():
    if scheduler:
        await scheduler.stop()
    logger.info("AI Mojo Assistant stopped")

@app.get("/")
async def root():
    return {
        "message": "AI Mojo Assistant API", 
        "status": "running",
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)