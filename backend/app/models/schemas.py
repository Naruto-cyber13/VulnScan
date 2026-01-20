"""
Pydantic request/response schemas for LogLens/VulnScan Lite.
Centralized data validation and serialization models.
"""

from pydantic import BaseModel, Field, HttpUrl
from typing import List, Optional, Literal
from datetime import datetime

# ==================== REQUEST SCHEMAS ====================

class URLScanRequest(BaseModel):
    """Request schema for URL scanning."""
    url: HttpUrl = Field(..., description="Target URL to scan")
    premium:  bool = Field(
        default=False,
        description="Premium tier flag for enhanced analysis"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "url": "https://example.com",
                "premium": False
            }
        }

class LogScanRequest(BaseModel):
    """Request schema for log file analysis."""
    log_content: str = Field(..., description="Raw log text or uploaded file content")
    filename: Optional[str] = Field(
        default="uploaded_log.txt",
        description="Identifier for the log source"
    )
    premium: bool = Field(
        default=False,
        description="Premium tier flag for full threat breakdown"
    )

    class Config:
        #orm_mode = True
        json_schema_extra = {
            "example": {
                "log_content": "192.168.1.1 - - [15/Jan/2026:10:00:00 +0000] \"GET / HTTP/1.1\" 200 1234",
                "filename": "access. log",
                "premium": False
            }
        }

# ==================== RESPONSE SCHEMAS ====================

class SecurityHeader(BaseModel):
    """Model for a security header check result."""
    header_name: str
    present: bool
    value: Optional[str] = None
    recommended: str = Field(description="Recommended header value")

class URLScanResult(BaseModel):
    """Response schema for URL scan results."""
    scan_id: str = Field(description="Unique scan identifier")
    target_url: str
    https_enabled: bool
    status_code: int
    server_info: Optional[str]
    security_headers: List[SecurityHeader]
    threat_count: int
    severity:  Literal["LOW", "MEDIUM", "HIGH"]
    severity_score: float = Field(description="Score from 0.0 to 10.0")
    findings: List[str] = Field(description="Detailed findings")
    premium_insights: Optional[List[str]] = Field(
        default=None,
        description="Premium tier specific insights"
    )
    scanned_at: datetime

    class Config:
        json_schema_extra = {
            "example": {
                "scan_id": "scan_abc123",
                "target_url": "https://example.com",
                "https_enabled": True,
                "status_code":  200,
                "server_info": "nginx/1.21.0",
                "security_headers":  [
                    {
                        "header_name":  "Content-Security-Policy",
                        "present": False,
                        "value": None,
                        "recommended": "default-src 'self'"
                    }
                ],
                "threat_count": 2,
                "severity": "MEDIUM",
                "severity_score": 5.5,
                "findings":  [
                    "Missing Content-Security-Policy header",
                    "Server information exposed"
                ],
                "premium_insights": [
                    "Consider implementing CSP to prevent XSS attacks",
                    "Hide server banner to reduce reconnaissance surface"
                ],
                "scanned_at": "2026-01-15T10:30:00"
            }
        }

class ThreatDetection(BaseModel):
    """Model for detected threat in logs."""
    threat_type: str
    severity: Literal["LOW", "MEDIUM", "HIGH"]
    line_number: int
    matched_pattern: str
    details: str

class LogScanResult(BaseModel):
    """Response schema for log scan results."""
    scan_id: str
    filename: str
    total_lines: int
    threat_count: int
    severity:  Literal["LOW", "MEDIUM", "HIGH"]
    severity_score: float = Field(description="Score from 0.0 to 10.0")
    threat_breakdown: dict = Field(description="Threats by category")
    threats_detected: List[ThreatDetection] = Field(
        description="List of detected threats (limited in free tier)"
    )
    premium_insights: Optional[List[ThreatDetection]] = Field(
        default=None,
        description="Full threat list for premium users"
    )
    recommendations: List[str]
    scanned_at: datetime

    class Config:
        orm_mode= True
        json_schema_extra = {
            "example":  {
                "scan_id":  "scan_xyz789",
                "filename": "access.log",
                "total_lines": 1000,
                "threat_count":  15,
                "severity":  "MEDIUM",
                "severity_score": 6.2,
                "threat_breakdown":  {
                    "brute_force": 8,
                    "sql_injection": 4,
                    "xss":  3
                },
                "threats_detected": [
                    {
                        "threat_type":  "brute_force",
                        "severity": "MEDIUM",
                        "line_number": 50,
                        "matched_pattern": "Multiple 401 responses from same IP",
                        "details": "192.168.1.100 attempted login 10 times in 2 minutes"
                    }
                ],
                "recommendations":  [
                    "Implement rate limiting",
                    "Review firewall rules",
                    "Enable security monitoring"
                ],
                "scanned_at": "2026-01-15T10:30:00"
            }
        }

class ScanHistoryItem(BaseModel):
    """Model for scan history record."""
    scan_id: str
    scan_type:  Literal["URL", "LOG"]
    target:  str
    threat_count: int
    severity:  str
    premium:  bool
    scanned_at: datetime

class ScanHistory(BaseModel):
    """Response schema for scan history."""
    total_scans: int
    scans:  List[ScanHistoryItem]

    class Config:
        json_schema_extra = {
            "example": {
                "total_scans": 5,
                "scans": [
                    {
                        "scan_id": "scan_abc123",
                        "scan_type": "URL",
                        "target": "https://example.com",
                        "threat_count": 2,
                        "severity": "MEDIUM",
                        "premium": False,
                        "scanned_at": "2026-01-15T10:30:00"
                    }
                ]
            }
        }

class ErrorResponse(BaseModel):
    """Standard error response."""
    error: str
    detail: str
    status_code: int

    class Config:
        json_schema_extra = {
            "example": {
                "error": "Invalid URL",
                "detail": "The provided URL is not valid",
                "status_code": 400
            }
        }