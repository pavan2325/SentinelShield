import requests
import time

URL = "http://127.0.0.1:5000/"

# (name, payload, expected) -> expected is "attack" or "normal"
TESTS = [
    # Normal traffic
    ("Normal id", "1", "normal"),
    ("Normal search", "laptop", "normal"),
    ("Normal name", "Pavan", "normal"),
    ("Name with apostrophe", "O'Brien", "normal"),
    ("Hashtag text", "#trending", "normal"),

    # SQL Injection
    ("SQLi classic", "1' OR '1'='1", "attack"),
    ("SQLi union", "1 UNION SELECT username,password FROM users", "attack"),
    ("SQLi comment", "admin'--", "attack"),

    # XSS
    ("XSS script", "<script>alert(1)</script>", "attack"),
    ("XSS onerror", "<img src=x onerror=alert(1)>", "attack"),
    ("XSS javascript", "javascript:alert(1)", "attack"),

    # Directory Traversal
    ("Traversal basic", "../../etc/passwd", "attack"),
    ("Traversal windows", "..\\..\\windows\\win.ini", "attack"),

    # Command Injection
    ("CMD cat", "; cat /etc/passwd", "attack"),
    ("CMD ls", "; ls -la", "attack"),
    ("CMD whoami pipe", "| whoami", "attack"),
    ("CMD whoami and", "&& whoami", "attack"),
]

results = []

print("=== Running detection tests ===")
for name, payload, expected in TESTS:
    r = requests.get(URL, params={"q": payload})
    blocked = r.status_code in (403, 429)
    outcome = "attack" if blocked else "normal"

    if expected == "attack" and blocked:
        verdict = "TRUE POSITIVE"
    elif expected == "normal" and not blocked:
        verdict = "TRUE NEGATIVE"
    elif expected == "normal" and blocked:
        verdict = "FALSE POSITIVE"
    else:
        verdict = "FALSE NEGATIVE"

    results.append(verdict)
    print(f"{name:25} | status {r.status_code} | {verdict}")
    time.sleep(2.5)  # stay under the rate limit so it doesn't distort results

tp = results.count("TRUE POSITIVE")
tn = results.count("TRUE NEGATIVE")
fp = results.count("FALSE POSITIVE")
fn = results.count("FALSE NEGATIVE")
total = len(results)

print("\n=== Detection Summary ===")
print(f"Total tests:      {total}")
print(f"True Positives:   {tp}")
print(f"True Negatives:   {tn}")
print(f"False Positives:  {fp}")
print(f"False Negatives:  {fn}")
print(f"Accuracy:         {(tp + tn) / total * 100:.1f}%")

print("\n=== Brute-force / rate limit test ===")
print("Waiting 11 seconds for the rate-limit window to reset...")
time.sleep(11)
for i in range(1, 9):
    r = requests.get(URL, params={"id": i})
    print(f"Request {i}: status {r.status_code}")