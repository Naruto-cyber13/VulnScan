"""
SQLAlchemy ORM table definitions for LogLens/VulnScan Lite.
Defines database schema for scan history and results.
"""

from sqlalchemy import Column, String, Integer, Float, DateTime, Boolean, Text, JSON
from sqlalchemy.sql import func
from datetime import datetime
from app.models.database import Base
import uuid

class ScanRecord(Base):
    """
    SQLAlchemy model for storing scan history records.
    Tracks all scans performed by users.
    """
    __tablename__ = "scan_records"
    
    # Primary key
    id = Column(String(36), primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    
    # Scan metadata
    scan_type = Column(String(10), nullable=False)  # "URL" or "LOG"
    target = Column(String(500), nullable=False)     # URL or filename
    premium = Column(Boolean, default=False)
    
    # Results
    threat_count = Column(Integer, default=0)
    severity = Column(String(10), nullable=False)    # "LOW", "MEDIUM", "HIGH"
    severity_score = Column(Float, default=0.0)
    
    # Detailed results (stored as JSON)
    scan_results = Column(JSON, nullable=True)       # Full scan details
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    scanned_at = Column(DateTime, nullable=False)
    
    # User tracking (extensible for future auth)
    user_ip = Column(String(45), nullable=True)      # IPv4 or IPv6
    
    def to_history_dict(self):
        """Convert to scan history dictionary."""
        return {
            "scan_id": self.id,
            "scan_type": self.scan_type,
            "target": self.target,
            "threat_count": self.threat_count,
            "severity": self.severity,
            "premium": self.premium,
            "scanned_at": self.scanned_at.isoformat()
        }