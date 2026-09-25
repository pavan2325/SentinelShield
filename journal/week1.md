# Week 1 Journal — SentinelShield

## Purpose
This week's goal was to set up a basic Flask application and learn how to 
inspect HTTP requests — understanding headers, methods, and payloads as a 
foundation for building security-focused tooling.

## Tools Used
- Python
- Flask
- curl
- Postman
- Git

## Steps Followed
1. Set up a Python virtual environment (`venv`) for the project.
2. Installed Flask (`pip install flask`).
3. Created a basic Flask app with a test route (`/`) to confirm the server runs.
4. Ran the Flask development server and tested it in the browser.
5. Sent test requests using `curl` from the terminal to inspect responses.
6. Used Postman to send GET/POST requests and examine headers, status codes, 
   and response bodies in more detail.
7. Compared request/response structure across curl, Postman, and the browser.

![Flask terminal output](screenshots/flask-terminal.png)
![Postman response](screenshots/postman-response.png)
![curl output](screenshots/curl-output.png)


## What I Learned About Request Structure
- HTTP requests consist of a method (GET, POST, etc.), headers, and 
  optionally a body.
- Postman makes it easy to visually inspect headers and status codes, 
  while curl is faster for quick command-line checks.
- Flask's terminal output logs each incoming request, which is useful 
  for debugging.

# On Flask specifically:

Flask's debug mode (app.run(debug=True)) auto-reloads the server on code changes and gives more detailed error pages — useful during development.
Every request Flask receives shows up in the terminal log with the method, path, and status code, which makes debugging much faster than guessing.

# Tie-in to the security angle of SentinelShield:

Understanding the structure of HTTP requests, including headers, HTTP methods, URLs, parameters, and request bodies, is an important foundation for building SentinelShield's security features. In a normal web application, requests usually follow predictable patterns. By understanding these normal patterns, SentinelShield can later identify requests that behave differently or appear suspicious.

Attackers may manipulate request headers, use unexpected HTTP methods, modify parameters, inject malicious payloads, or send unusually large or repeated requests. These behaviors can be indicators of attacks such as SQL Injection, Cross-Site Scripting (XSS), Command Injection, Local File Inclusion (LFI), and brute-force attempts.

For example, a normal application may commonly receive GET requests to retrieve pages and POST requests to submit form data. If SentinelShield detects an unusual method, suspicious header value, malformed request body, or repeated requests from the same IP address, it can flag the activity for further inspection.

This understanding will be useful when implementing the detection rules, logging, rate limiting, and WAF functionality of SentinelShield. The application can record important request information such as the source IP, HTTP method, requested URL, headers, timestamp, and detected event. These logs can then be analyzed to identify abnormal patterns and generate security alerts.

Therefore, learning how normal HTTP requests work is the first step toward developing a security system that can differentiate legitimate traffic from potentially malicious traffic. This provides the foundation for SentinelShield's future intrusion detection and web-protection capabilities.

