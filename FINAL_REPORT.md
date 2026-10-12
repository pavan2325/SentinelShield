# SentinelShield: Lightweight Web Application Firewall and Intrusion Detection System

**Final Project Report**

| | |
|---|---|
| **Project** | SentinelShield |
| **Student** | Pavan Hegde |
| **Technology** | Python, Flask,Regex-based detection engine |
| **Repository** |https://github.com/pavan2325/SentinelShield|
| **Live Demo** |https://sentinelshield-hypw.onrender.com/dashboard|

---

## Table of Contents

1. Abstract
2. Introduction
3. Objectives
4. Theoretical Background
5. System Design and Architecture
6. Implementation
7. Tools and Technologies
8. Testing Methodology
9. Results and Detection Accuracy
10. False Positives and False Negatives
11. Rate Limiting and IP Flagging Results
12. Log Analysis
13. Dashboard
14. Observed Patterns and Interpretation
15. Limitations
16. Future Improvements
17. Conclusion
18. References

---

## 1. Abstract

SentinelShield is a simplified Web Application Firewall (WAF) and Intrusion Detection System built with Python and Flask. It inspects every incoming HTTP request, detects common web attacks (SQL Injection, Cross-Site Scripting, Directory Traversal, Local File Inclusion, and Command Injection) using signature rules, limits abusive traffic through per-IP rate limiting, temporarily bans repeat offenders, records every decision in structured logs, and presents the results on a live dashboard.

The system was validated with an automated test suite that measures true positives, true negatives, false positives, and false negatives. Rules were tuned based on the errors found, and detection accuracy improved from 29% to 89%. This report describes the theory behind the system, its design and implementation, the testing process, and the results.

---

## 2. Introduction

Web applications are exposed to the open internet, which makes them a constant target. Attackers send specially crafted requests to steal data, take over accounts, or run code on the server. A Web Application Firewall is a security layer that sits in front of an application and examines each request before the application sees it. If a request looks malicious, the WAF blocks it.

Commercial WAFs are complex, but their core ideas are simple: break a request into parts, compare those parts against known attack patterns, watch how often each client sends requests, record what happened, and show the results to a human. SentinelShield implements each of those ideas in a small, readable form so the concepts can be studied and tested hands-on.

The project follows the standard security pipeline:

**Detection → Decision → Logging → Alerting → Dashboarding**

---

## 3. Objectives

The practical objectives of this project were to:

- Understand how WAFs detect threats using patterns, signatures, and rule engines
- Analyze HTTP requests from a security perspective
- Identify common web attacks using manual and automated testing
- Document findings and generate test reports
- Create meaningful logs and summaries
- Understand the full workflow from detection to decision, logging, alerting, and dashboarding
- Demonstrate how rate limiting and traffic behavior analysis help prevent brute-force and flooding attacks

---

## 4. Theoretical Background

### 4.1 Web Application Security and the Role of a WAF

A web application accepts input from users: form fields, URL parameters, cookies, and headers. If the application trusts that input without checking it, an attacker can use it to change what the application does. Most serious web vulnerabilities come from this single mistake, which is why the OWASP Top 10 list of critical web risks is dominated by injection-style flaws.

A Web Application Firewall protects against this by filtering traffic at the HTTP level. It does not fix the underlying vulnerability, but it can stop many exploit attempts before they reach the application. A WAF is best seen as one layer in a defense-in-depth strategy, alongside secure coding, input validation, and patching.

### 4.2 Anatomy of an HTTP Request

To detect attacks, the system must first understand what a request contains:

| Part | Description | Why it matters for security |
|---|---|---|
| **Request line** | Method (GET, POST), path, and HTTP version | The path can contain traversal sequences |
| **Query parameters** | Key-value pairs after `?` in the URL | The most common place for injected payloads |
| **Headers** | Metadata such as `User-Agent`, `Cookie`, `Host` | Attackers hide payloads in headers because many filters ignore them |
| **Body** | Data sent with POST requests | Carries form data and JSON that can contain payloads |

A request is only as safe as its least-inspected part. For this reason SentinelShield scans the URL, parameters, body, User-Agent, and Cookie together.

### 4.3 Common Web Attacks

**SQL Injection (SQLi).** Applications often build database queries from user input. If the input is inserted directly into the query, an attacker can change the query's logic. For example, input such as `1' OR '1'='1` turns a "find this user" query into one that is always true, which can bypass logins or expose entire tables. Typical signatures include a quote followed by `OR`/`AND`, SQL comment markers (`--`, `#`), and keywords such as `UNION SELECT`.

**Cross-Site Scripting (XSS).** The attacker injects JavaScript into a page that other users will view. When the victim's browser loads the page, the script runs with the victim's privileges and can steal session cookies or redirect the user. Signatures include `<script>` tags, event-handler attributes such as `onerror=`, and `javascript:` URLs.

**Directory Traversal.** The attacker uses sequences like `../` to climb out of the folder the application intends to serve and reach other files on the server. Encoded forms such as `%2e%2e%2f` are used to evade simple filters.

**Local File Inclusion (LFI).** The attacker tricks the application into reading or running a file already on the server, such as `/etc/passwd` on Linux or `win.ini` on Windows. LFI often combines with directory traversal and may use wrappers such as `file://` or `php://`.

**Command Injection.** If the application passes user input to an operating-system command, the attacker can append extra commands using separators such as `;`, `&&`, `||`, or `|`, or through command substitution with backticks and `$( )`. A successful attack gives the attacker control of the server.

### 4.4 Signature-Based Detection

Signature-based detection compares input against a library of known attack patterns. Each pattern is a rule, and each rule belongs to an attack category. If a request matches a rule, it is flagged and classified.

SentinelShield expresses signatures as **regular expressions** (regex), which describe text patterns flexibly. For example, a rule can match "a quote, then OR or AND, then another quote or digit" instead of one exact string, so small variations are still caught. Matching is case-insensitive because attackers vary capitalization to evade filters.

The approach has clear strengths: it is fast, predictable, and easy to explain. Its weaknesses are equally important:

- **False positives:** a rule that is too broad blocks legitimate input. A rule flagging every single quote would block the surname O'Brien.
- **False negatives:** a rule that is too narrow misses real attacks, such as a command injection using `&&` when only `;` was covered.
- **Evasion:** attackers can encode, split, or obfuscate payloads to slip past static patterns.

Writing good signatures is therefore a balancing exercise, and rules need continual testing and tuning.

### 4.5 Behavior Monitoring and Rate Limiting

Not every attack contains a malicious payload. A **brute-force attack** tries thousands of password guesses, each of which looks like a normal login request. A **flooding (denial-of-service) attack** overwhelms a server with a high volume of ordinary requests. Signatures cannot catch these because the content is harmless. What is abnormal is the **frequency**.

Rate limiting addresses this by counting requests per client within a time window and rejecting clients that exceed a threshold. Three ideas define it:

- **Request threshold:** the maximum number of requests allowed
- **Time window:** the period over which requests are counted (a sliding window discards old requests as time passes)
- **Client identity:** requests are tracked per IP address

SentinelShield allows up to 5 requests per 10 seconds from one IP. Beyond that, requests are rejected with HTTP status **429 (Too Many Requests)**.

### 4.6 IP Flagging and Temporary Bans

Blocking a single request does not stop a determined attacker. SentinelShield therefore keeps a count of violations ("strikes") per IP. After 3 strikes the IP is flagged and temporarily banned for 60 seconds, during which all of its requests are rejected. This moves the system from reacting to individual requests toward responding to persistent offenders. Temporary bans are used instead of permanent ones to limit harm from false alarms.

### 4.7 Logging, Alerting, and Monitoring

Detection alone is not enough. Security teams need evidence of what happened, so every decision is recorded. Each log entry captures a **timestamp**, the **client IP**, the **detection category**, and the **action taken**. Structured logs (one JSON object per line) are easy for programs to read, which makes later analysis, such as counting attacks per category or finding repeat offenders, straightforward.

An **alert** is an event that deserves attention, such as a blocked attack or a banned IP. Logs preserve the record, and alerts draw attention to it.

### 4.8 Dashboards

A dashboard turns raw logs into a form a person can understand quickly. By summarizing total events, attack categories, flagged IPs, and recent alerts, it supports trend recognition and faster incident response. In real environments such dashboards are fed into Security Information and Event Management (SIEM) systems; SentinelShield provides a small version of the same idea.

### 4.9 Measuring Detection Quality

To judge a detection system objectively, each test result is placed in one of four categories:

| Term | Meaning |
|---|---|
| **True Positive (TP)** | A malicious request that was correctly blocked |
| **True Negative (TN)** | A normal request that was correctly allowed |
| **False Positive (FP)** | A normal request that was wrongly blocked |
| **False Negative (FN)** | A malicious request that was wrongly allowed |

**Accuracy = (TP + TN) / (TP + TN + FP + FN)**

False positives harm legitimate users, while false negatives leave the system exposed. Reporting both, rather than accuracy alone, gives an honest picture of quality.

---

## 5. System Design and Architecture

![Architecture Diagram](report_assets/architecture_diagram.png)

The system is organized as a pipeline. A client request is captured by the interceptor, checked against the ban list, scanned by the rule engine, and evaluated by the rate limiter. The decision logic then allows or blocks the request and may flag the IP. Every outcome is written to the log, and the dashboard reads the log to display live statistics.

**Request flow:**

1. The client sends an HTTP request to the Flask server.
2. The interceptor extracts the URL, query parameters, body, User-Agent, and Cookie.
3. If the IP is banned, the request is rejected with 403.
4. The rule engine scans the combined input against attack signatures. A match returns 403.
5. The rate limiter counts the IP's recent requests. Exceeding the limit returns 429.
6. Blocked requests add a strike to the IP; the third strike triggers a 60-second ban.
7. The event is logged as JSON.
8. The dashboard reads the log and displays the results.

---

## 6. Implementation

| File | Responsibility |
|---|---|
| `app.py` | Request interceptor, decision logic, and the `/dashboard` route |
| `rules.py` | Regex signatures grouped by attack category and the `check_request()` function |
| `tracker.py` | Sliding-window rate limiting, strike counting, and temporary bans |
| `logger.py` | Structured JSON event logging to `logs/activity.log` |
| `test_suite.py` | Automated test requests with TP/TN/FP/FN classification |
| `log_summary.py` | Log analysis producing the summary tables |

**Development phases**

- **Week 1:** Environment setup, architecture design, and a basic Flask app that receives and prints requests.
- **Week 2:** Rule engine built and connected to Flask. A false positive was found and fixed: scanning `str(request_data)` caused every request to contain quote characters from Python's dictionary formatting, so only real user input is scanned now.
- **Week 3:** Rate limiting and structured logging added.
- **Week 4:** Automated test suite and log analysis; measured accuracy and found weaknesses.
- **Final phase:** Rules tuned, LFI and encoded-payload detection added, headers scanned, IP flagging and the dashboard implemented.

---

## 7. Tools and Technologies

| Tool | Purpose |
|---|---|
| Python 3 | Core language |
| Flask | Web framework acting as the request interceptor |
| Regular expressions (`re`) | Attack signature matching |
| Postman and curl | Manual attack and request simulation |
| `requests` library | Automated test suite |
| VS Code | Development environment |
| Git and GitHub | Version control and hosting |
| Render | Cloud deployment |

---

## 8. Testing Methodology

Testing used three approaches:

1. **Manual testing** with Postman and curl, sending normal requests and hand-crafted payloads for each attack category.
2. **Automated testing** with `test_suite.py`, which sends a fixed set of normal and malicious requests and classifies each outcome as TP, TN, FP, or FN.
3. **Brute-force simulation**, sending rapid repeated requests to confirm that rate limiting and banning trigger.

The test set included:

- Normal inputs, including tricky legitimate ones (a name with an apostrophe, text starting with `#`)
- SQL Injection, XSS, Directory Traversal, and Command Injection payloads
- A burst of rapid requests from one IP

Testing was run before and after rule tuning so the improvement could be measured.

- Total attack requests tested: 37
- Total normal requests tested: 20
- Brute-force burst requests sent: 17

![Test Suite Output](report_assets/final_test_suite_output.png)

---

## 9. Results and Detection Accuracy


| Metric          | Before Tuning | After Tuning |
| --------------- | ------------: | -----------: |
| True Positives  |            11 |           12 |
| True Negatives  |             3 |            5 |
| False Positives |             2 |            0 |
| False Negatives |             1 |            0 |
| **Accuracy**    |     **82.4%** |   **100.0%** |


![Normal Request Allowed](report_assets/final_normal_request_id.png)

---

## 10. False Positives and False Negatives

**False positives found**

- `O'Brien` and `#trending` were blocked as SQL Injection because the original rule matched any single quote or `#` character.
- **Fix:** the rule now requires a quote or comment marker to appear alongside SQL logic (such as `OR`, `AND`, or `--`).

![False Positive Fixed: O'Brien](report_assets/final_normal_request_apostrophe_fixed.png)

**False negatives found**

- `&& whoami` was not detected because the Command Injection rule only covered `;` and `|` separators.
- **Fix:** the rule now covers `;`, `&&`, `||`, and `|` followed by common commands, plus backtick and `$( )` substitution.

**Lesson:** broad rules cause false positives and narrow rules cause false negatives. Each fix was verified by re-running the full test suite.

---

## 11. Rate Limiting and IP Flagging Results

- **Rate limit:** more than 5 requests in 10 seconds returns 429.
- **IP flagging:** 3 blocked events lead to a 60-second temporary ban.
- **Observed behavior:** a burst of 7 rapid requests allowed the first 5 and blocked the rest. Three attack payloads in a row triggered a ban, and a harmless request sent afterward was also rejected until the ban expired.

![Rate Limit Triggered](report_assets/final_ratelimit_triggered.png)

![IP Banned](report_assets/final_ip_banned.png)

---

## 12. Log Analysis

Each log entry records a timestamp, IP address, detection category, and action. `log_summary.py` aggregates the log into the tables below.

| Category      |    Count       |
|---|:---:|
| SQL Injection |      3         |
| XSS           |      3         |
| Directory Traversal | 2        |
| Local File Inclusion |   1     |
| Command Injection |    3       |
| Rate Limit Exceeded |   3      |
| IP Flagged (temporary ban)| 15 |
| Normal (allowed) |     12        |

**Most flagged IP:** 127.0.0.1 (all testing was local, so every event comes from one address).

![Log Summary](report_assets/final_log_summary.png)

---

## 13. Dashboard

The dashboard is served at `/dashboard` and refreshes every 5 seconds. It shows total events, attacks by category as bars, the top flagged IPs, and the ten most recent alerts. It completes the pipeline by turning stored logs into something a person can read at a glance.

![Dashboard](report_assets/final_dashboard_overview.png)

---

## 14. Observed Patterns and Interpretation

(Write 5 to 6 sentences in your own words. Cover:
- Which attack category appeared most often in the logs, and why
- How signature detection and rate limiting complement each other (signatures catch bad content, rate limiting catches bad behavior)
- Why the false positives occurred and what the before/after comparison shows about tuning
- What you would change next)

---

## 15. Limitations

- Rate-limit counters and bans are stored in memory, so they reset when the server restarts.
- Regex signatures cannot catch every obfuscated or novel attack.
- Only one route was protected and tested.
- All testing came from one local IP, so multi-client behavior was not observed.
- The `/dashboard` route has no authentication.

---

## 16. Future Improvements

- Store logs and bans in a database for persistence
- Add anomaly-based detection alongside static signatures
- Protect more routes, HTTP methods, and file uploads
- Add authentication to the dashboard
- Use a larger, standard rule set such as the OWASP Core Rule Set as a reference

---

## 17. Conclusion

SentinelShield demonstrates the full security pipeline of a Web Application Firewall: request inspection, signature-based detection, behavior-based rate limiting, IP flagging, structured logging, and dashboard visualization. Testing showed that tuning rules based on measured false positives and false negatives improved accuracy from ___% to ___%.

(Add 2 to 3 sentences on what you learned, for example how rule precision affects false alarms, why content-based and behavior-based detection are both needed, and why measuring your own system's weaknesses matters.)

---

## 18. References

- OWASP Foundation, *OWASP Top 10: Web Application Security Risks*, https://owasp.org/www-project-top-ten/
- OWASP Foundation, *OWASP Core Rule Set*, https://owasp.org/www-project-modsecurity-core-rule-set/
- Flask Documentation, https://flask.palletsprojects.com/
- MDN Web Docs, *HTTP Overview*, https://developer.mozilla.org/en-US/docs/Web/HTTP/Overview
- Python Documentation, *re: Regular expression operations*, https://docs.python.org/3/library/re.html