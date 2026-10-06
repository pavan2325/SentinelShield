from flask import Flask, request, render_template_string
from collections import Counter
import json, os
from rules import check_request
from tracker import is_abusive, is_banned, add_strike
from logger import log_event, LOG_FILE

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    ip = request.remote_addr
    body = request.get_data(as_text=True)

    if is_banned(ip):
        log_event(ip, "Banned IP", "blocked")
        return "Blocked: your IP is temporarily banned", 403

    scan_target = " ".join([
        request.full_path,
        " ".join(request.args.values()),
        body,
        request.headers.get("User-Agent", ""),
        request.headers.get("Cookie", "")
    ])

    detection = check_request(scan_target)
    if detection:
        print(f"ALERT: {detection} detected from {ip}")
        log_event(ip, detection, "blocked")
        if add_strike(ip):
            print(f"ALERT: {ip} flagged and temporarily banned")
            log_event(ip, "IP Flagged (temporary ban)", "flagged")
        return f"Blocked: {detection} detected", 403

    if is_abusive(ip):
        print(f"ALERT: rate limit exceeded by {ip}")
        log_event(ip, "Rate Limit Exceeded", "blocked")
        if add_strike(ip):
            log_event(ip, "IP Flagged (temporary ban)", "flagged")
        return "Blocked: Too many requests (rate limit exceeded)", 429

    log_event(ip, "Normal", "allowed")
    return "Request received", 200


DASHBOARD = """
<html><head><title>SentinelShield Dashboard</title>
<meta http-equiv="refresh" content="5">
<style>
body{font-family:Arial;background:#0f172a;color:#e2e8f0;margin:30px}
.card{background:#1e293b;padding:16px;border-radius:8px;margin-bottom:16px}
.bar{background:#3b82f6;height:16px;border-radius:4px;margin:4px 0 10px}
table{width:100%;border-collapse:collapse}
td,th{padding:6px;border-bottom:1px solid #334155;text-align:left}
</style></head><body>
<h1>SentinelShield Dashboard</h1>
<div class="card">Total events: <b>{{ total }}</b> &nbsp;|&nbsp;
Blocked / flagged: <b>{{ blocked }}</b></div>
<div class="card"><h3>Attacks by category</h3>
{% for name, c in by_cat %}
<div>{{ name }} ({{ c }})</div>
<div class="bar" style="width:{{ (c / maxc * 100)|round }}%"></div>
{% endfor %}</div>
<div class="card"><h3>Top flagged IPs</h3>
<table><tr><th>IP</th><th>Blocked events</th></tr>
{% for ip, c in by_ip %}<tr><td>{{ ip }}</td><td>{{ c }}</td></tr>{% endfor %}
</table></div>
<div class="card"><h3>Recent alerts</h3>
<table><tr><th>Time</th><th>IP</th><th>Category</th><th>Action</th></tr>
{% for e in recent %}
<tr><td>{{ e.timestamp }}</td><td>{{ e.ip }}</td><td>{{ e.category }}</td><td>{{ e.action }}</td></tr>
{% endfor %}</table></div>
</body></html>
"""

@app.route('/dashboard')
def dashboard():
    entries = []
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE) as f:
            entries = [json.loads(l) for l in f if l.strip()]
    alerts = [e for e in entries if e["action"] != "allowed"]
    by_cat = Counter(e["category"] for e in alerts)
    by_ip = Counter(e["ip"] for e in alerts)
    return render_template_string(
        DASHBOARD,
        total=len(entries),
        blocked=len(alerts),
        by_cat=by_cat.most_common(),
        by_ip=by_ip.most_common(5),
        recent=alerts[-10:][::-1],
        maxc=max(by_cat.values(), default=1),
    )

if __name__ == '__main__':
    app.run(debug=True, port=5000)