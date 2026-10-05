import json
from collections import Counter

LOG_FILE = "logs/activity.log"

entries = []
with open(LOG_FILE) as f:
    for line in f:
        line = line.strip()
        if line:
            entries.append(json.loads(line))

total = len(entries)
by_category = Counter(e["category"] for e in entries)
by_action = Counter(e["action"] for e in entries)
by_ip = Counter(e["ip"] for e in entries if e["action"] == "blocked")

print("=== SentinelShield Log Summary ===")
print(f"Total events: {total}\n")

print("Action breakdown:")
for action, count in by_action.items():
    print(f"  {action:10} {count}")

print("\nDistribution by category:")
for category, count in by_category.most_common():
    print(f"  {category:22} {count}")

print("\nIPs with blocked requests:")
for ip, count in by_ip.most_common():
    print(f"  {ip:16} {count} blocked")