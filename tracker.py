import time

request_log = {}
BLOCKED_IPS = {}   # ip -> time when the ban ends
STRIKES = {}       # ip -> number of blocked requests

TIME_WINDOW = 10
MAX_REQUESTS = 5
MAX_STRIKES = 3
BAN_SECONDS = 60

def is_abusive(ip: str) -> bool:
    now = time.time()
    request_log.setdefault(ip, [])
    request_log[ip] = [t for t in request_log[ip] if now - t < TIME_WINDOW]
    request_log[ip].append(now)
    return len(request_log[ip]) > MAX_REQUESTS

def is_banned(ip: str) -> bool:
    until = BLOCKED_IPS.get(ip)
    if until and time.time() < until:
        return True
    if until:
        del BLOCKED_IPS[ip]
    return False

def add_strike(ip: str) -> bool:
    STRIKES[ip] = STRIKES.get(ip, 0) + 1
    if STRIKES[ip] >= MAX_STRIKES:
        BLOCKED_IPS[ip] = time.time() + BAN_SECONDS
        STRIKES[ip] = 0
        return True
    return False