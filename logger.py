import os
import json
import time

os.makedirs("logs", exist_ok=True)

LOG_FILE = "logs/activity.log"

def log_event(ip, category, action):
    entry = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "ip": ip,
        "category": category,
        "action": action
    }

    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(entry) + "\n")