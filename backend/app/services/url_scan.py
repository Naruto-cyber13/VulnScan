"""
URL Security Scanning Service - Passive Only.
Performs passive security checks on target URLs.
"""

import logging
import httpx
from typing import Dict, List, Tuple, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

class URLScanner:
    """Service for passive URL security scanning."""
    
    # Security headers that should be present
    SECURITY_HEADERS = {
        "Content-Security-Policy": "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'",
        "X-Frame-Options": "DENY",
        "X-Content-Type-Options": "nosniff",
        "Strict-Transport-Security": "max-age=31536000; includeSubDomains"
    }
    
    # HTTP status code categories
    STATUS_WARNINGS = {
        401: "Unauthorized",
        403: "Forbidden",
        404: "Not Found",
        500: "Internal Server Error",
        502: "Bad Gateway",
        503: "Service Unavailable"
    }
    
    def __init__(self, timeout: int = 10):
        """
        Initialize URLScanner.
        
        Args:
            timeout: HTTP request timeout in seconds
        """
        self.timeout = timeout
    
    async def scan(self, url: str) -> Dict:
        """
        Perform passive security scan on URL.
        
        Args:
            url: Target URL to scan
            
        Returns:
            Dictionary containing scan results
        """
        logger.info(f"Starting passive scan for URL: {url}")
        
        # Ensure URL has protocol
        if not url.startswith(('http://', 'https://')):
            url = f"https://{url}"
        
        results = {
            "target_url": url,
            "https_enabled": url.startswith("https://"),
            "status_code": None,
            "server_info": None,
            "security_headers": [],
            "threats": [],
            "findings": []
        }
        
        try:
            # Perform HTTP request
            async with httpx.AsyncClient(timeout=self.timeout, follow_redirects=True) as client:
                response = await client.head(url, timeout=self.timeout)
                results["status_code"] = response.status_code
                
                # Extract server info
                server_header = response.headers.get("Server")
                if server_header:
                    results["server_info"] = server_header
                    results["threats"].append("Server information exposed")
                    results["findings"].append(f"Server header exposed: {server_header}")
                
                # Check security headers
                for header_name, recommended_value in self.SECURITY_HEADERS.items():
                    header_present = header_name in response.headers
                    header_value = response.headers.get(header_name)
                    
                    header_check = {
                        "header_name":  header_name,
                        "present": header_present,
                        "value": header_value,
                        "recommended": recommended_value
                    }
                    
                    results["security_headers"].append(header_check)
                    
                    if not header_present:
                        results["threats"].append(f"Missing {header_name} header")
                        results["findings"].append(f"Security header '{header_name}' is not set")
                
                # Check HTTP status
                if results["status_code"] in self.STATUS_WARNINGS:
                    warning = self.STATUS_WARNINGS[results["status_code"]]
                    results["threats"].append(f"HTTP Status Warning: {warning}")
                    results["findings"].append(f"Server returned HTTP {results['status_code']} ({warning})")
                
                # Check HTTPS
                if not results["https_enabled"]:
                    results["threats"].append("HTTPS not enabled")
                    results["findings"].append("Website does not use HTTPS encryption")
        
        except httpx.TimeoutException:
            logger.warning(f"Timeout scanning {url}")
            results["findings"].append("Request timed out - website may be slow or unreachable")
            results["threats"].append("Connection timeout")
        except httpx.ConnectError:
            logger.warning(f"Connection error for {url}")
            results["findings"].append("Unable to connect to website")
            results["threats"].append("Connection failed")
        except Exception as e: 
            logger.error(f"Error scanning URL {url}: {str(e)}")
            results["findings"].append(f"Scan error: {str(e)}")
            results["threats"].append("Scan error occurred")
        
        return results
    
    def calculate_threat_score(self, results: Dict) -> Tuple[int, str, float]:
        """
        Calculate threat count and severity from scan results.
        
        Args:
            results: Scan results dictionary
            
        Returns:
            Tuple of (threat_count, severity_label, severity_score)
        """
        threat_count = len(results. get("threats", []))
        
        # Score calculation
        score = min((threat_count / 10) * 10, 10.0)  # 10 threats = max score
        
        if score < 3.0:
            severity = "LOW"
        elif score < 6.5:
            severity = "MEDIUM"
        else: 
            severity = "HIGH"
        
        return threat_count, severity, score
    
    def get_premium_insights(self, results: Dict) -> List[str]:
        """
        Generate premium tier insights for scan results.
        
        Args:
            results: Scan results dictionary
            
        Returns:
            List of premium insights
        """
        insights = []
        
        if not results.get("https_enabled"):
            insights.append("🔐 HTTPS is critical for protecting user data.  Implement SSL/TLS immediately.")
        
        missing_headers = [h for h in results["security_headers"] if not h["present"]]
        if missing_headers:
            insights. append(
                f"⚠️  Missing {len(missing_headers)} security headers.  "
                f"These headers prevent common web vulnerabilities like XSS and clickjacking."
            )
        
        if results. get("server_info"):
            insights.append(
                "🕵️  Your server information is visible to attackers. "
                "Consider disabling or masking the Server header."
            )
        
        if results.get("status_code") and results["status_code"] >= 500:
            insights.append(
                "⛔ Your server is returning 5xx errors. "
                "This may indicate configuration issues or vulnerabilities."
            )
        
        if not insights:
            insights.append("✅ Your website demonstrates good security practices!")
        
        return insights