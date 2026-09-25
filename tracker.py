import time

# Stores request timestamps per IP: { "ip": [timestamp1, timestamp2, ...] }
request_log = {}

# Configuration
TIME_WINDOW = 10      # seconds
MAX_REQUESTS = 5       # allowed requests per window

def is_abusive(ip: str) -> bool:
    now = time.time()

    if ip not in request_log:
        request_log[ip] = []

    # Keep only timestamps within the time window
    request_log[ip] = [t for t in request_log[ip] if now - t < TIME_WINDOW]

    # Add current request
    request_log[ip].append(now)

    # Check threshold
    if len(request_log[ip]) > MAX_REQUESTS:
        return True
    return False
