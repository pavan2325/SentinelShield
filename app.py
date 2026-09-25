from flask import Flask, request
from rules import check_request
from tracker import is_abusive
from logger import log_event

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    ip = request.remote_addr

    request_data = {
        "url": request.url,
        "path": request.path,
        "args": request.args.to_dict(),
        "headers": dict(request.headers),
        "body": request.get_data(as_text=True)
    }

    scan_target = request.full_path + " " + " ".join(request.args.values()) + " " + request_data["body"]
    detection = check_request(scan_target)

    if detection:
        print(f"🚨 ALERT: {detection} detected from {ip}")
        log_event(ip, detection, "blocked")
        return f"Blocked: {detection} detected", 403

    if is_abusive(ip):
        print(f"⚠️ ALERT: Rate limit exceeded by {ip}")
        log_event(ip, "Rate Limit Exceeded", "blocked")
        return "Blocked: Too many requests (rate limit exceeded)", 429

    log_event(ip, "Normal", "allowed")
    print("Request looks clean:", request_data)
    return "Request received", 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)