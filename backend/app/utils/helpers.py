"""
Utility functions for LogLens/VulnScan Lite.
Common helpers for ID generation, validation, and calculations.
"""

import uuid
import re
import logging
from typing import List, Dict, Tuple

logger = logging.getLogger(__name__)

def generate_scan_id() -> str:
    """Generate unique scan identifier."""
    return f"scan_{uuid.uuid4().hex[:12]}"

def calculate_severity_score(threat_count: int, max_threats: int = 50) -> Tuple[float, str]:
    """
    Calculate severity score (0.0-10.0) and label based on threat count.
    
    Args:
        threat_count:  Number of threats detected
        max_threats:  Threshold for maximum score
        
    Returns:
        Tuple of (score, severity_label)
    """
    score = min((threat_count / max_threats) * 10, 10.0)
    
    if score < 3.0:
        severity = "LOW"
    elif score < 6.5:
        severity = "MEDIUM"
    else:
        severity = "HIGH"
    
    return score, severity

def validate_url(url: str) -> bool:
    """
    Basic URL validation.
    
    Args:
        url: URL string to validate
        
    Returns: 
        True if valid URL format
    """
    url_pattern = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain
        r'localhost|'  # localhost
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # IP address
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    
    return url_pattern.match(url) is not None

def sanitize_log_content(log_content: str, max_length: int = 1000000) -> str:
    """
    Sanitize log content for processing.
    Removes null bytes and limits size.
    
    Args:
        log_content: Raw log text
        max_length:  Maximum allowed length
        
    Returns:
        Sanitized log content
    """
    if not log_content:
        return ""
    
    # Remove null bytes
    sanitized = log_content.replace('\x00', '')
    
    # Limit length
    if len(sanitized) > max_length:
        logger.warning(f"Log content truncated from {len(sanitized)} to {max_length} bytes")
        sanitized = sanitized[:max_length]
    
    return sanitized

def extract_ip_address(log_line: str) -> str:
    """
    Extract IP address from log line (common Apache/Nginx format).
    
    Args:
        log_line:  Single log line
        
    Returns:
        IP address string or empty string if not found
    """
    ip_pattern = re.compile(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')
    match = ip_pattern. match(log_line. strip())
    return match.group(0) if match else ""

def count_ip_occurrences(log_content: str) -> Dict[str, int]:
    """
    Count occurrences of each IP address in logs.
    
    Args:
        log_content: Full log text
        
    Returns:
        Dictionary mapping IPs to occurrence counts
    """
    ip_pattern = re.compile(r'\b(? :\d{1,3}\.){3}\d{1,3}\b')
    ip_matches = ip_pattern.findall(log_content)
    
    ip_counts = {}
    for ip in ip_matches:
        ip_counts[ip] = ip_counts.get(ip, 0) + 1
    
    return ip_counts

def limit_threat_details(threats: List[Dict], limit: int = 10) -> List[Dict]:
    """
    Limit threat details for free tier users.
    
    Args:
        threats: Full threat list
        limit: Maximum threats to return
        
    Returns: 
        Limited threat list
    """
    return threats[:limit]