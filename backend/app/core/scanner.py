"""
Core Scanner Dispatcher.
Routes scan requests to appropriate service and orchestrates scanning.
"""

import logging
from typing import Dict, Optional
from datetime import datetime
from app.services.url_scan import URLScanner
from app. services.log_scan import LogScanner
from app.utils.helpers import generate_scan_id, limit_threat_details
from app. models.tables import ScanRecord
from app.models.database import SessionLocal

logger = logging.getLogger(__name__)

class ScanDispatcher:
    """Orchestrates scanning operations and result handling."""
    
    def __init__(self):
        """Initialize dispatcher with scanner services."""
        self.url_scanner = URLScanner()
        self.log_scanner = LogScanner()
    
    async def scan_url(self, url: str, premium:  bool = False) -> Dict:
        """
        Execute URL security scan. 
        
        Args:
            url: Target URL
            premium: Premium tier flag
            
        Returns: 
            Complete scan result
        """
        logger.info(f"Initiating URL scan for {url} (Premium: {premium})")
        scan_id = generate_scan_id()
        
        try: 
            # Perform scan
            raw_results = await self.url_scanner. scan(url)
            
            # Calculate severity
            threat_count, severity, severity_score = self.url_scanner.calculate_threat_score(raw_results)
            
            # Get premium insights
            premium_insights = None
            if premium:
                premium_insights = self.url_scanner.get_premium_insights(raw_results)
            
            # Build response
            result = {
                "scan_id": scan_id,
                "target_url": raw_results["target_url"],
                "https_enabled": raw_results["https_enabled"],
                "status_code": raw_results["status_code"],
                "server_info": raw_results["server_info"],
                "security_headers":  raw_results["security_headers"],
                "threat_count": threat_count,
                "severity": severity,
                "severity_score": severity_score,
                "findings": raw_results["findings"],
                "premium_insights": premium_insights,
                "scanned_at": datetime.utcnow()
            }
            
            # Store in database
            self._store_scan(
                scan_id=scan_id,
                scan_type="URL",
                target=url,
                threat_count=threat_count,
                severity=severity,
                severity_score=severity_score,
                premium=premium,
                scan_results=result
            )
            
            logger.info(f"URL scan completed:  {scan_id} - Severity: {severity}")
            return result
        
        except Exception as e: 
            logger.error(f"URL scan failed for {url}: {str(e)}", exc_info=True)
            raise
    
    async def scan_log(self, log_content: str, filename: str = "log.txt", premium: bool = False) -> Dict:
        """
        Execute log file threat analysis.
        
        Args:
            log_content: Raw log text
            filename: Log file identifier
            premium: Premium tier flag
            
        Returns:
            Complete scan result
        """
        logger.info(f"Initiating log scan for {filename} (Premium: {premium})")
        scan_id = generate_scan_id()
        
        try:
            # Perform scan
            raw_results = self.log_scanner.scan(log_content, filename)
            
            # Calculate severity
            threat_count, severity, severity_score = self.log_scanner.calculate_severity(
                raw_results["threats_detected"]
            )
            
            # Get recommendations
            recommendations = self.log_scanner.get_recommendations(raw_results)
            
            # Handle threat details based on tier
            threats_to_return = raw_results["threats_detected"]
            premium_threats = None
            
            if not premium:
                # Free tier: limit to 10 threats
                threats_to_return = limit_threat_details(raw_results["threats_detected"], limit=10)
            else:
                # Premium:  return all with enhanced details
                premium_threats = self.log_scanner.get_premium_detailed_threats(
                    raw_results["threats_detected"]
                )
            
            # Build response
            result = {
                "scan_id":  scan_id,
                "filename": filename,
                "total_lines": raw_results["total_lines"],
                "threat_count": threat_count,
                "severity": severity,
                "severity_score": severity_score,
                "threat_breakdown": raw_results["threat_breakdown"],
                "threats_detected": threats_to_return,
                "premium_detailed_threats": premium_threats,
                "recommendations": recommendations,
                "scanned_at": datetime. utcnow()
            }
            
            # Store in database
            self._store_scan(
                scan_id=scan_id,
                scan_type="LOG",
                target=filename,
                threat_count=threat_count,
                severity=severity,
                severity_score=severity_score,
                premium=premium,
                scan_results=result
            )
            
            logger.info(f"Log scan completed: {scan_id} - Threats: {threat_count}")
            return result
        
        except Exception as e: 
            logger.error(f"Log scan failed for {filename}: {str(e)}", exc_info=True)
            raise
    
    def _store_scan(self, scan_id: str, scan_type: str, target:  str,
                   threat_count: int, severity: str, severity_score: float,
                   premium: bool, scan_results: Dict) -> None:
        """
        Store scan result in database.
        
        Args:
            scan_id:  Unique scan identifier
            scan_type:  Type of scan (URL or LOG)
            target:  Target URL or filename
            threat_count: Number of threats detected
            severity: Severity label
            severity_score: Severity score (0-10)
            premium: Premium tier flag
            scan_results:  Full scan result dictionary
        """
        try:
            db = SessionLocal()
            record = ScanRecord(
                id=scan_id,
                scan_type=scan_type,
                target=target,
                threat_count=threat_count,
                severity=severity,
                severity_score=severity_score,
                premium=premium,
                scan_results=scan_results,
                scanned_at=datetime.utcnow()
            )
            db.add(record)
            db.commit()
            logger.info(f"Scan stored in database: {scan_id}")
        except Exception as e:
            logger.error(f"Failed to store scan:  {str(e)}")
        finally:
            db.close()
    
    def get_scan_history(self, limit: int = 50) -> Dict:
        """
        Retrieve scan history from database.
        
        Args:
            limit: Maximum number of records to return
            
        Returns: 
            Dictionary with scan history
        """
        try:
            db = SessionLocal()
            records = db.query(ScanRecord).order_by(ScanRecord.created_at.desc()).limit(limit).all()
            
            scans = [record.to_history_dict() for record in records]
            
            return {
                "total_scans": len(scans),
                "scans":  scans
            }
        except Exception as e:
            logger.error(f"Failed to retrieve scan history: {str(e)}")
            return {"total_scans": 0, "scans": []}
        finally:
            db.close()