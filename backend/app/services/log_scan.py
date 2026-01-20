"""
Log File Threat Analysis Service.
Detects security threats in log files using pattern matching.
"""

import logging
import re
from typing import Dict, List, Tuple
from collections import defaultdict
from datetime import datetime

logger = logging.getLogger(__name__)

class LogScanner:
    """Service for analyzing logs and detecting security threats."""
    
    # Threat detection patterns (compiled regex for performance)
    THREAT_PATTERNS = {
        "brute_force": [
            re.compile(r'401|Unauthorized', re.IGNORECASE),
            re.compile(r'invalid password|login failed', re.IGNORECASE),
            re.compile(r'authentication failure', re.IGNORECASE),
        ],
        "sql_injection":  [
            re.compile(r"union.*select|select.*from|insert.*into|delete.*from|drop.*table", re.IGNORECASE),
            re.compile(r"'\s*(or|and)\s*'1'='1", re.IGNORECASE),
            re.compile(r"(\%27)|(\')|(--)|(;)|(\/\*)", re.IGNORECASE),
            re.compile(r"exec\s*\(|execute\s*\(", re. IGNORECASE),
        ],
        "xss": [
            re.compile(r"<script[^>]*>|javascript:|onerror=|onload=", re.IGNORECASE),
            re.compile(r"alert\s*\(|eval\s*\(|expression\s*\(", re.IGNORECASE),
            re.compile(r"(%3Cscript|%3Cimg|%3Ciframe)", re.IGNORECASE),
            re.compile(r"<iframe[^>]*>|<object[^>]*>", re. IGNORECASE),
        ],
        "suspicious_activity": [
            re.compile(r"admin|root|test|debug|backup", re.IGNORECASE),
            re.compile(r"\. \. \/|\.\. \\|%2e%2e", re.IGNORECASE),
            re.compile(r"\/etc\/passwd|\/etc\/shadow|C:\\windows", re.IGNORECASE),
        ]
    }
    
    # Severity mapping for threat types
    THREAT_SEVERITY = {
        "sql_injection": "HIGH",
        "xss": "HIGH",
        "brute_force": "MEDIUM",
        "suspicious_activity":  "MEDIUM"
    }
    
    def __init__(self):
        """Initialize LogScanner."""
        pass
    
    def scan(self, log_content: str, filename: str = "log.txt") -> Dict:
        """
        Scan log content for security threats.
        
        Args:
            log_content: Raw log text
            filename: Log file identifier
            
        Returns:
            Dictionary containing scan results
        """
        logger.info(f"Starting log analysis for {filename}")
        
        # Split into lines and filter empty lines
        log_lines = [line for line in log_content.split('\n') if line.strip()]
        total_lines = len(log_lines)
        
        logger.info(f"Processing {total_lines} log lines from {filename}")
        
        # Initialize results
        results = {
            "filename": filename,
            "total_lines": total_lines,
            "threats_detected": [],
            "threat_breakdown": defaultdict(int),
            "ip_frequency": {}
        }
        results["scanned_at"] = datetime.utcnow()
        results["scanned_at_iso"] = results["scanned_at"].isoformat()


        # Scan each line
        for line_num, line in enumerate(log_lines, 1):
            detected_threats = self._detect_threats_in_line(line, line_num)
            results["threats_detected"].extend(detected_threats)
            
            # Update threat breakdown
            for threat in detected_threats:
                results["threat_breakdown"][threat["threat_type"]] += 1
        
        # Analyze IP addresses for brute force patterns
        ip_threats = self._analyze_ip_patterns(log_lines)
        results["threats_detected"].extend(ip_threats)
        for threat in ip_threats:
            results["threat_breakdown"][threat["threat_type"]] += 1
        
        # Convert defaultdict to regular dict
        results["threat_breakdown"] = dict(results["threat_breakdown"])
        
        return results
    
    def _detect_threats_in_line(self, line: str, line_num: int) -> List[Dict]:
        """
        Detect threats in a single log line.
        
        Args:
            line: Log line to analyze
            line_num: Line number in file
            
        Returns:
            List of detected threats
        """
        threats = []
        
        for threat_type, patterns in self.THREAT_PATTERNS.items():
            for pattern in patterns:
                match = pattern.search(line)
                if match:
                    threat = {
                        "threat_type": threat_type,
                        "severity": self.THREAT_SEVERITY. get(threat_type, "MEDIUM"),
                        "line_number": line_num,
                        "matched_pattern": match.group(0)[:100],  # Limit to 100 chars
                        "details": line[: 200]  # First 200 chars of line
                    }
                    threats.append(threat)
        
        return threats
    
    def _analyze_ip_patterns(self, log_lines: List[str]) -> List[Dict]:
        """
        Analyze IP patterns for brute force detection.
        
        Args:
            log_lines: List of log lines
            
        Returns:
            List of brute force threats detected
        """
        threats = []
        ip_pattern = re.compile(r'\b(?:\d{1,3}\.){3}\d{1,3}\b')
        ip_counts = defaultdict(int)
        ip_status_codes = defaultdict(list)
        
        # Count IP occurrences and track status codes
        for line in log_lines:
            ip_match = ip_pattern.search(line)
            if ip_match: 
                ip = ip_match.group(0)
                ip_counts[ip] += 1
                
                # Extract status code if present (common in Apache/Nginx logs)
                status_match = re.search(r'\s(\d{3})\s', line)
                if status_match:
                    ip_status_codes[ip].append(status_match.group(1))
        
        # Detect suspicious IP patterns
        for ip, count in ip_counts.items():
            if count > 10:  # IP with many requests
                threats.append({
                    "threat_type": "brute_force",
                    "severity": "MEDIUM",
                    "line_number": 0,
                    "matched_pattern": f"IP {ip} - {count} requests",
                    "details": f"IP address {ip} made {count} requests (potential brute force)"
                })
            
            # Check for multiple failed authentication attempts
            statuses = ip_status_codes. get(ip, [])
            failed_auths = statuses.count('401') + statuses.count('403')
            if failed_auths >= 5:
                threats.append({
                    "threat_type": "brute_force",
                    "severity": "MEDIUM",
                    "line_number": 0,
                    "matched_pattern": f"IP {ip} - {failed_auths} auth failures",
                    "details":  f"IP {ip} had {failed_auths} failed authentication attempts"
                })
        
        return threats
    
    def calculate_severity(self, threats: List[Dict]) -> Tuple[int, str, float]: 
        """
        Calculate overall severity from detected threats.
        
        Args:
            threats: List of detected threats
            
        Returns: 
            Tuple of (threat_count, severity_label, severity_score)
        """
        threat_count = len(threats)
        
        # Weight HIGH severity threats more
        weighted_score = 0
        for threat in threats:
            if threat["severity"] == "HIGH":
                weighted_score += 2
            elif threat["severity"] == "MEDIUM":
                weighted_score += 1
        
        # Normalize score to 0-10
        score = min((weighted_score / (threat_count * 2)) * 10, 10.0) if threat_count > 0 else 0.0
        
        if score < 3.0:
            severity = "LOW"
        elif score < 6.5:
            severity = "MEDIUM"
        else:
            severity = "HIGH"
        
        return threat_count, severity, score
    
    def get_recommendations(self, results: Dict) -> List[str]:
        """
        Generate security recommendations based on findings.
        
        Args:
            results: Scan results dictionary
            
        Returns:
            List of recommendations
        """
        recommendations = []
        threat_breakdown = results. get("threat_breakdown", {})
        
        if threat_breakdown. get("brute_force", 0) > 0:
            recommendations.append("🔐 Implement rate limiting to prevent brute force attacks")
            recommendations.append("🚨 Review and harden authentication mechanisms")
            recommendations.append("📋 Consider implementing IP whitelisting for sensitive endpoints")
        
        if threat_breakdown.get("sql_injection", 0) > 0:
            recommendations.append("⚠️  SQL Injection detected!  Use parameterized queries and input validation")
            recommendations.append("🛡️  Implement Web Application Firewall (WAF) rules")
            recommendations.append("🔍 Conduct security code review of database queries")
        
        if threat_breakdown.get("xss", 0) > 0:
            recommendations.append("⚠️  XSS (Cross-Site Scripting) detected!  Implement proper output encoding")
            recommendations.append("🛡️  Enforce Content Security Policy (CSP) headers")
            recommendations.append("✅ Validate and sanitize all user inputs")
        
        if threat_breakdown.get("suspicious_activity", 0) > 0:
            recommendations. append("🔍 Investigate suspicious activity patterns")
            recommendations.append("🚫 Review file system and directory access logs")
            recommendations.append("📊 Consider implementing intrusion detection system (IDS)")
        
        if not recommendations:
            recommendations.append("✅ No major threats detected. Continue monitoring logs regularly.")
        
        return recommendations
    
    def get_premium_detailed_threats(self, threats: List[Dict]) -> List[Dict]:
        """
        Return full threat details for premium users.
        
        Args:
            threats: List of detected threats
            
        Returns:
            Full threat list with detailed analysis
        """
        # Add contextual information to each threat
        enhanced_threats = []
        for threat in threats:
            enhanced_threat = threat.copy()
            
            # Add remediation suggestions based on threat type
            if threat["threat_type"] == "sql_injection":
                enhanced_threat["remediation"] = "Use parameterized queries and ORM frameworks"
            elif threat["threat_type"] == "xss": 
                enhanced_threat["remediation"] = "Implement output encoding and CSP headers"
            elif threat["threat_type"] == "brute_force":
                enhanced_threat["remediation"] = "Implement rate limiting and account lockout"
            else:
                enhanced_threat["remediation"] = "Review access controls and implement monitoring"
            
            enhanced_threats.append(enhanced_threat)
        
        return enhanced_threats