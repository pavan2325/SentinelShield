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

Understanding request structure (headers, methods, bodies) is the foundation for later detecting suspicious or malformed requests — attackers often manipulate headers or send unexpected methods.
Noticing how "normal" requests look now will make it easier to spot anomalies later when building the security rules/logging parts of the app.

