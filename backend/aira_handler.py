import logging
import requests
import traceback
import time
import sys
from datetime import datetime
from flask import request, g, has_request_context
from config import Config


class RateLimiter:
    """Simple token bucket rate limiter."""
    
    def __init__(self, max_requests=100, time_window=60):
        self.max_requests = max_requests
        self.time_window = time_window
        self.requests = []
    
    def allow_request(self):
        """Check if request is allowed based on rate limit."""
        now = time.time()
        # Remove old requests outside time window
        self.requests = [req for req in self.requests if now - req < self.time_window]
        
        if len(self.requests) < self.max_requests:
            self.requests.append(now)
            return True
        return False


class AIRAHandler(logging.Handler):
    """
    Custom logging handler that sends error logs to AIRA webhook.
    
    Features:
    - Automatic severity classification (P0/P1/P2)
    - Rich contextual information
    - Sensitive data sanitization
    - Rate limiting to prevent spam
    - Retry logic with exponential backoff
    - Non-blocking operation
    """
    
    SENSITIVE_FIELDS = [
        'password', 'password_hash', 'token', 'api_key',
        'secret', 'credit_card', 'cvv', 'ssn', 'authorization'
    ]
    
    def __init__(self):
        super().__init__()
        self.webhook_url = Config.AIRA_WEBHOOK_URL
        self.enabled = Config.AIRA_ENABLED
        self.max_retries = Config.AIRA_MAX_RETRIES
        self.timeout = Config.AIRA_TIMEOUT
        self.rate_limiter = RateLimiter(
            max_requests=Config.AIRA_RATE_LIMIT,
            time_window=60
        )
        
        # Only handle ERROR and above
        self.setLevel(logging.ERROR)
        
        # Debug logging
        print(f"[AIRA] Initializing handler...")
        print(f"[AIRA] Webhook URL: {self.webhook_url}")
        print(f"[AIRA] Enabled: {self.enabled}")
        
        if not self.webhook_url:
            print("[AIRA] WARNING: AIRA webhook URL not configured. Error logging disabled.")
            self.enabled = False
        elif not self.enabled:
            print("[AIRA] WARNING: AIRA is disabled via AIRA_ENABLED setting.")
        else:
            print(f"[AIRA] Successfully initialized. Ready to send errors to {self.webhook_url}")
    
    def emit(self, record):
        """Process and send log record to AIRA."""
        print(f"[AIRA] emit() called - enabled: {self.enabled}, level: {record.levelname}")
        
        if not self.enabled:
            print(f"[AIRA] Skipping - AIRA is disabled")
            return
        
        # Check rate limit
        if not self.rate_limiter.allow_request():
            print(f"[AIRA] Rate limit exceeded, skipping error: {record.getMessage()}")
            return
        
        try:
            print(f"[AIRA] Processing error: {record.getMessage()}")
            
            # Build the payload
            payload = self._build_payload(record)
            print(f"[AIRA] Payload built, sending to {self.webhook_url}")
            
            # Send to AIRA (with retry logic)
            success = self._send_with_retry(payload)
            
            if success:
                print(f"[AIRA] Successfully sent error to AIRA")
            else:
                print(f"[AIRA] Failed to send error to AIRA")
            
        except Exception as e:
            # Don't let AIRA errors break the application
            print(f"AIRA logging failed: {e}")
    
    def _build_payload(self, record):
        """Construct AIRA webhook payload."""
        # Get stack trace if available
        stack_trace = ""
        if record.exc_info:
            stack_trace = ''.join(traceback.format_exception(*record.exc_info))
        
        # Build the payload
        payload = {
            "message": self.format(record),
            "stack_trace": stack_trace,
            "severity": self._get_severity(record.levelno),
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "context": self._get_context(record)
        }
        
        return payload
    
    def _get_context(self, record):
        """Extract request and user context."""
        context = {
            "error_type": record.exc_info[0].__name__ if record.exc_info else "Unknown",
            "module": record.module,
            "function": record.funcName,
            "line_number": record.lineno,
            "python_version": sys.version.split()[0],
        }
        
        # Add request context if available
        if has_request_context():
            try:
                context.update({
                    "user_id": getattr(g, 'user_id', 'anonymous'),
                    "user_email": getattr(g, 'user_email', None),
                    "endpoint": request.endpoint,
                    "method": request.method,
                    "path": request.path,
                    "url": request.url,
                    "remote_addr": request.remote_addr,
                    "user_agent": request.headers.get('User-Agent', 'Unknown'),
                    "query_params": dict(request.args),
                    "request_body": self._sanitize_data(request.get_json(silent=True)),
                })
            except Exception as e:
                context["context_error"] = str(e)
        
        return context
    
    def _get_severity(self, levelno):
        """Map Python log level to AIRA severity."""
        if levelno >= logging.CRITICAL:
            return "P0"
        elif levelno >= logging.ERROR:
            return "P1"
        else:
            return "P2"
    
    def _sanitize_data(self, data):
        """Remove sensitive fields from data."""
        if not data:
            return {}
        
        if isinstance(data, dict):
            sanitized = {}
            for key, value in data.items():
                if any(sensitive in key.lower() for sensitive in self.SENSITIVE_FIELDS):
                    sanitized[key] = '***REDACTED***'
                elif isinstance(value, dict):
                    sanitized[key] = self._sanitize_data(value)
                elif isinstance(value, list):
                    sanitized[key] = [self._sanitize_data(item) if isinstance(item, dict) else item for item in value]
                else:
                    sanitized[key] = value
            return sanitized
        
        return data
    
    def _send_with_retry(self, payload):
        """Send payload to AIRA webhook with exponential backoff retry."""
        headers = {
            'Content-Type': 'application/json'
        }
        
        print(f"[AIRA] Attempting to send to webhook: {self.webhook_url}")
        
        for attempt in range(self.max_retries):
            try:
                print(f"[AIRA] Attempt {attempt + 1}/{self.max_retries}")
                
                response = requests.post(
                    self.webhook_url,
                    json=payload,
                    headers=headers,
                    timeout=self.timeout
                )
                
                print(f"[AIRA] Response status: {response.status_code}")
                
                if response.status_code == 200:
                    return True
                
                # If not successful, wait before retry
                if attempt < self.max_retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff: 1s, 2s, 4s
                
            except requests.exceptions.RequestException as e:
                if attempt == self.max_retries - 1:
                    print(f"AIRA webhook failed after {self.max_retries} attempts: {e}")
                    return False
                time.sleep(2 ** attempt)
        
        return False


def setup_aira_logging(app):
    """Set up AIRA logging for the Flask application."""
    if Config.AIRA_ENABLED:
        # Create AIRA handler
        aira_handler = AIRAHandler()
        
        # Set formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        aira_handler.setFormatter(formatter)
        
        # Add to root logger first - this catches ALL loggers
        root_logger = logging.getLogger()
        root_logger.addHandler(aira_handler)
        root_logger.setLevel(logging.ERROR)  # Ensure root logger captures errors
        
        # Also add to app logger for good measure
        app.logger.addHandler(aira_handler)
        app.logger.setLevel(logging.ERROR)
        
        app.logger.info("AIRA error monitoring initialized")
        print(f"[AIRA] Handler added to root logger and app logger")
    else:
        app.logger.warning("AIRA error monitoring is disabled")

# Made with Bob
