from fastapi import FastAPI
from src.db.session import engine, Base

# This is for development only. For production, use Alembic migrations.
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI-Mojo Assistant",
    description="AI-ассистент завуча для школ Корифей",
    version="0.1.0",
)


@app.get("/", tags=["Health Check"])
async def root():
    """
    Health check endpoint.
    """
    return {"status": "ok"}

# Routers will be included here later
# from src.api.v1.endpoints import monitoring
# app.include_router(monitoring.router, prefix="/api/v1/monitoring", tags=["Monitoring"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)