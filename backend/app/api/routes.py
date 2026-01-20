'''from fastapi import APIRouter

router = APIRouter()

@router.get("/health")
def health_check():
    return {"status": "ok"}'''
"""
API Routes for LogLens/VulnScan Lite. 
Defines all HTTP endpoints and request handlers.
"""

import logging
from fastapi import APIRouter, HTTPException, Query, Request
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from datetime import datetime

from app.models.schemas import (
    URLScanRequest, URLScanResult,
    LogScanRequest, LogScanResult,
    ScanHistory, ErrorResponse
)
from app.core.scanner import ScanDispatcher
from app.core.analyzer import ThreatAnalyzer
from app.config import settings
from fastapi import Depends
from app.models.database import get_db
from app.models.tables import ScanRecord

logger = logging.getLogger(__name__)

# Initialize router and dispatcher
router = APIRouter(prefix="/api/v1", tags=["Security Scans"])
dispatcher = ScanDispatcher()

# ==================== URL SCANNING ENDPOINTS ====================
@router.post(
    "/scan/url",
    response_model=URLScanResult,
    summary="Scan URL for Security Vulnerabilities",
    description="Performs passive security analysis on a target URL"
)
async def scan_url(request: URLScanRequest, req: Request, db=Depends(get_db)):
    try:
        logger.info(f"URL scan request:  {request.url}")

        # Perform scan
        result = await dispatcher.scan_url(
            url=str(request.url),
            premium=request.premium
        )
        result = ThreatAnalyzer.enrich_url_scan(result)
        # Convert datetime objects to ISO strings before saving
        if isinstance(result.get("scanned_at"), datetime):
            result["scanned_at"] = result["scanned_at"].isoformat()


        # Store scan in DB
        record = ScanRecord(
            scan_type="URL",
            target=str(request.url),
            premium=request.premium,
            threat_count=result["threat_count"],
            severity=result["severity"],
            severity_score=result["severity_score"],
            scan_results=result,
            scanned_at=datetime.fromisoformat(result["scanned_at"]),
            user_ip=req.client.host if req.client else None
        )
        db.add(record)
        db.commit()

        # Attach scan ID and timestamp to response
        result["scan_id"] = record.id
        #result["scanned_at"] = result["scanned_at"].isoformat()
        #if isinstance(result.get("scanned_at"), datetime):
            #result["scanned_at"] = result["scanned_at"].isoformat()


        return result

    except ValidationError as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Scan error: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="An error occurred during scanning"
        )

'''
@router. post(
    "/scan/url",
    response_model=URLScanResult,
    summary="Scan URL for Security Vulnerabilities",
    description="Performs passive security analysis on a target URL"
)
async def scan_url(request: URLScanRequest, req: Request):
    """
    Endpoint for URL security scanning.
    
    - **url**: Target URL to scan (required)
    - **premium**: Enable premium analysis (optional)
    
    Returns comprehensive security analysis including SSL/TLS status,
    security headers, and threat assessment.
    """
    try:
        logger.info(f"URL scan request:  {request.url}")
        
        # Execute scan
        result = await dispatcher.scan_url(
            url=str(request.url),
            premium=request.premium
        )
        
        # Enrich results
        result = ThreatAnalyzer. enrich_url_scan(result)
        
        # Convert datetime to ISO format for JSON serialization
        result["scanned_at"] = result["scanned_at"].isoformat()
        
        return result
    
    except ValidationError as e:
        logger. error(f"Validation error:  {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e: 
        logger.error(f"Scan error: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="An error occurred during scanning"
        )
'''
@router.post(
    "/scan/log",
    response_model=LogScanResult,
    summary="Analyze Log File for Threats",
    description="Performs threat detection and analysis on log file content"
)
async def scan_log(request: LogScanRequest, req: Request, db=Depends(get_db)):
    """
    Endpoint for log file threat analysis.
    
    - **log_content**: Raw log text to analyze (required)
    - **filename**:  Log file identifier (optional)
    - **premium**: Enable premium detailed analysis (optional)
    
    Returns threat detection results with severity assessment and
    security recommendations.
    """
    try:
        logger.info(f"Log scan request: {request.filename}")
        
        # Validate log content
        if not request.log_content or len(request.log_content.strip()) == 0:
            raise HTTPException(
                status_code=400,
                detail="Log content cannot be empty"
            )
        
        # Execute scan
        result = await dispatcher.scan_log(
            log_content=request.log_content,
            filename=request.filename,
            premium=request.premium
        )
        
        # Enrich results
        result = ThreatAnalyzer.enrich_log_scan(result)
        
        # Convert datetime to ISO format
        result["scanned_at"] = result["scanned_at"].isoformat()
        scanned_at_dt = datetime.fromisoformat(result["scanned_at"])
        record = ScanRecord(
            scan_type="LOG",
            target=request.filename or "unknown.log",
            premium=request.premium,
            threat_count=result["threat_count"],
            severity=result["severity"],
            severity_score=result["severity_score"],
            scan_results=result,
            scanned_at=scanned_at_dt,
            user_ip=req.client.host if req.client else None
        )
        #db = get_db()
        db.add(record)
        db.commit()

        result["scan_id"] = record.id
        
        return result
    
    except ValidationError as e:
        logger.error(f"Validation error:  {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e: 
        logger.error(f"Scan error: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="An error occurred during scanning"
        )

# ==================== HISTORY ENDPOINTS ====================

@router.get(
    "/scans/history",
    response_model=ScanHistory,
    summary="Retrieve Scan History",
    description="Returns list of all previous scans"
)
async def get_scan_history(
    limit: int = Query(50, ge=1, le=1000, description="Maximum scans to return")
):
    """
    Retrieve scan history from database.
    
    - **limit**: Maximum number of records to return (1-1000, default 50)
    
    Returns paginated scan history with metadata.
    """
    try:
        if not settings.ENABLE_HISTORY:
            raise HTTPException(
                status_code=403,
                detail="Scan history is disabled"
            )
        
        history = dispatcher.get_scan_history(limit=limit)
        return history
    
    except Exception as e:
        logger.error(f"Error retrieving history: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Failed to retrieve scan history"
        )

# ==================== INFORMATION ENDPOINTS ====================

@router.get(
    "/info/features",
    summary="Get Available Features",
    description="Returns information about available scanning features"
)
async def get_features():
    """
    Returns list of available security scanning features.
    """
    return {
        "features": [
            {
                "name": "URL Security Scanning",
                "description": "Passive analysis of website security posture",
                "endpoint": "/scan/url",
                "checks": [
                    "HTTPS enforcement",
                    "Security headers",
                    "Server information",
                    "HTTP status validation"
                ]
            },
            {
                "name": "Log Threat Analysis",
                "description":  "Detect security threats in log files",
                "endpoint": "/scan/log",
                "threats":  [
                    "Brute force attempts",
                    "SQL injection",
                    "XSS attacks",
                    "Suspicious activity"
                ]
            },
            {
                "name":  "Scan History",
                "description": "Access previous scan results",
                "endpoint": "/scans/history"
            }
        ]
    }

@router.get(
    "/info/tiers",
    summary="Get Tier Information",
    description="Returns information about free and premium tiers"
)
async def get_tier_info():
    """
    Returns information about service tiers.
    """
    return {
        "tiers": {
            "free": {
                "name": "Free Tier",
                "cost": "$0/month",
                "features": [
                    "Basic URL security scanning",
                    "Standard log analysis",
                    "Limited threat details (10 max)",
                    "Scan history access",
                    "Basic recommendations"
                ],
                "limitations": [
                    "Limited threat breakdown",
                    "No premium insights",
                    "Standard severity assessment"
                ]
            },
            "premium": {
                "name": "Premium Tier",
                "cost": "$9.99/month (simulated)",
                "features": [
                    "All free tier features",
                    "Full threat breakdown",
                    "Premium security insights",
                    "Detailed threat explanations",
                    "Advanced recommendations",
                    "Unlimited threat details",
                    "Priority support"
                ],
                "benefits": [
                    "Complete threat visibility",
                    "Actionable security recommendations",
                    "Enhanced risk assessment"
                ]
            }
        }
    }

# ==================== ERROR HANDLERS ====================

@router.get("/error-test")
async def error_test():
    """Test error handling (development only)."""
    raise HTTPException(
        status_code=500,
        detail="This is a test error"
    )