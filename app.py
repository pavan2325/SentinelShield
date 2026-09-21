from flask import Flask, request
from rules import check_request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    request_data = {
        "url": request.url,
        "path": request.path,
        "args": request.args.to_dict(),
        "headers": dict(request.headers),
        "body": request.get_data(as_text=True)
    }

    # Only scan actual user-controlled input, not the dict structure
    scan_target = request.full_path + " " + " ".join(request.args.values()) + " " + request_data["body"]

    detection = check_request(scan_target)

    if detection:
        print(f"🚨 ALERT: {detection} detected!")
        return f"Blocked: {detection} detected", 403

    print("Request looks clean:", request_data)
    return "Request received", 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)