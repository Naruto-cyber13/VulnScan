"""
Main FastAPI application entry point for LogLens/VulnScan Lite.
Initializes app, database, and routes.
"""

import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.models.database import engine, Base
from app.api.routes import router

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging. FileHandler(f'{settings.LOG_DIR}/app.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for app startup and shutdown events.
    Creates database tables on startup. 
    """
    # Startup
    logger.info("🚀 Starting VulnScan Lite Backend")
    Base.metadata.create_all(bind=engine)
    logger.info("✅ Database tables initialized")
    
    yield
    
    # Shutdown
    logger.info("🛑 Shutting down VulnScan Lite Backend")

# Initialize FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.DESCRIPTION,
    version=settings.VERSION,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Add CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router)

@app.get("/")
async def root():
    """Root endpoint returning API information."""
    return {
        "project":  settings.PROJECT_NAME,
        "version": settings.VERSION,
        "status": "running",
        "docs":  "/docs",
        "features": [
            "Passive Website Security Scanning",
            "Log File Threat Analysis",
            "Scan History Management",
            "Free vs Premium Tiers"
        ]
    }

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION
    }

if __name__ == "__main__": 
    import uvicorn
    
    logger.info(f"Starting server at {settings.HOST}:{settings.PORT}")
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level=settings. LOG_LEVEL. lower()
    )