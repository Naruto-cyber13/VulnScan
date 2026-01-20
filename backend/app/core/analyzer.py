"""
Analyzer Module.
Post-processing and advanced analysis of scan results.
"""

import logging
from typing import Dict, List

logger = logging.getLogger(__name__)

class ThreatAnalyzer:
    """Analyzes and enriches threat detection results."""
    
    # CVSS-like severity mapping
    SEVERITY_WEIGHTS = {
        "LOW": 1.0,
        "MEDIUM": 5.0,
        "HIGH": 9.0
    }
    
    # Threat category descriptions
    THREAT_DESCRIPTIONS = {
        "brute_force": "Repeated failed login attempts or excessive requests from same source",
        "sql_injection":  "Potential SQL injection attack - malicious SQL command detected",
        "xss": "Cross-Site Scripting attempt - malicious script injection detected",
        "suspicious_activity": "Suspicious system activity - potential reconnaissance or abuse"
    }
    
    @staticmethod
    def enrich_url_scan(scan_result: Dict) -> Dict:
        """
        Enrich URL scan results with additional analysis.
        
        Args:
            scan_result: Raw URL scan result
            
        Returns: 
            Enhanced scan result
        """
        # Add security posture summary
        total_headers = len(scan_result. get("security_headers", []))
        missing_headers = sum(1 for h in scan_result. get("security_headers", []) if not h["present"])
        header_compliance = ((total_headers - missing_headers) / total_headers * 100) if total_headers > 0 else 0
        
        scan_result["header_compliance_percentage"] = round(header_compliance, 2)
        scan_result["risk_summary"] = ThreatAnalyzer._generate_risk_summary(
            scan_result.get("severity", "UNKNOWN")
        )
        
        return scan_result
    
    @staticmethod
    def enrich_log_scan(scan_result:  Dict) -> Dict:
        """
        Enrich log scan results with additional analysis.
        
        Args:
            scan_result:  Raw log scan result
            
        Returns:
            Enhanced scan result
        """
        # Calculate threat density
        total_lines = scan_result.get("total_lines", 1)
        threat_count = scan_result.get("threat_count", 0)
        threat_density = (threat_count / total_lines * 100) if total_lines > 0 else 0
        
        scan_result["threat_density_percentage"] = round(threat_density, 2)
        scan_result["risk_summary"] = ThreatAnalyzer._generate_risk_summary(
            scan_result.get("severity", "UNKNOWN")
        )
        
        # Add threat type descriptions
        for threat in scan_result.get("threats_detected", []):
            threat["description"] = ThreatAnalyzer.THREAT_DESCRIPTIONS.get(
                threat.get("threat_type", "unknown"),
                "Unknown threat type"
            )
        
        return scan_result
    
    @staticmethod
    def _generate_risk_summary(severity: str) -> str:
        """
        Generate human-readable risk summary.
        
        Args:
            severity:  Severity level
            
        Returns: 
            Risk summary string
        """
        summaries = {
            "LOW":  "✅ Low risk detected.  Continue regular monitoring.",
            "MEDIUM":  "⚠️  Medium risk detected. Review findings and implement recommendations.",
            "HIGH": "🚨 High risk detected. Immediate action recommended."
        }
        return summaries.get(severity, "⁉️  Unable to assess risk level")