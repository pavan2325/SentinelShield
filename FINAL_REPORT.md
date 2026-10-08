# SentinelShield — Final Report

## 1. Objective
SentinelShield is a simplified Web Application Firewall and Intrusion 
Detection System built to demonstrate how real-world WAFs detect threats 
using pattern/signature matching, monitor traffic behavior, log events, 
and surface results through a dashboard. This report summarizes the 
final system, its detection accuracy, and lessons learned.

## 2. System Architecture

![Architecture Diagram](report_assets/architecture_diagram.png)

The system intercepts every incoming request, checks it against the rule 
engine (signatures for SQLi, XSS, Directory Traversal, LFI, and Command 
Injection) and a rate-limit check. Based on the result, decision logic 
either allows the request or blocks it. Every event is logged, repeat 
offenders are flagged and temporarily banned, and all results are 
visualized on a live dashboard.

## 3. Tools & Technologies Used
- Python 3.x, Flask
- Regex-based rule engine
- Postman, curl / PowerShell
- Python `requests` library (automated test suite)
- VS Code, Git/GitHub

## 4. Test Summary
- Total attack requests tested: ___
- Total normal requests tested: ___
- Brute-force simulation requests sent: ___

![Test Suite Output](report_assets/final_test_suite_output.png)

## 5. Detection Accuracy — Before vs After Tuning

| Metric            | Before Tuning (Week 4) | After Tuning (Final Phase) |
|--------------------|:-----------------------:|:----------------------------:|
| True Positives      |                        |                              |
| True Negatives      |                        |                              |
| False Positives     |                        |                              |
| False Negatives     |                        |                              |
| **Accuracy (%)**    |                        |                              |

## 6. False Positives & False Negatives

**False Positives found:**
- `O'Brien` (apostrophe) incorrectly flagged as SQL Injection
- `#trending` incorrectly flagged as SQL Injection
- Fixed by requiring the quote/hash to appear near SQL keywords 
  (`or`, `and`, `--`) instead of matching any quote character alone.

![Normal Request Fixed - id=1](report_assets/final_normal_request_id.png)
![Normal Request Fixed - O'Brien](report_assets/final_normal_request_apostrophe_fixed.png)

**False Negatives found:**
- `&& whoami` was not detected as Command Injection
- Fixed by adding `&&` and backtick/`$()` patterns to the Command 
  Injection rule set.

## 7. Rate Limiting & IP Flagging Results
- Rate limit threshold: more than 5 requests in 10 seconds
- After 3 blocked/flagged events, the IP is temporarily banned for 60 seconds
- Confirmed working: sending 3 attack payloads in a row triggered a ban; 
  a subsequent normal request was blocked with "IP temporarily banned"; 
  access was restored after the ban period expired.

![Rate Limit Triggered](report_assets/final_ratelimit_triggered.png)
![IP Banned Response](report_assets/final_ip_banned.png)

## 8. Log Analysis

| Category              | Count |
|-------------------------|:-------:|
| SQL Injection            |    11    |
| XSS                       |    7    |
| Directory Traversal       |   5     |
| Local File Inclusion      |   1      |
| Command Injection         |   3     |
| Rate Limit Exceeded       |   3    |
| IP Flagged (temp ban)     |   5     |
| Normal (allowed)          |   33    |

**Most flagged IP(s):** 127.0.0.1 (local testing environment)

![Log Summary Output](report_assets/final_log_summary.png)

## 9. Dashboard

The live dashboard is available at `http://127.0.0.1:5000/dashboard` and 
auto-refreshes every 5 seconds. It displays total events, a breakdown of 
attacks by category, the top flagged IPs, and the 10 most recent alerts.

![Dashboard - Overview](report_assets/final_dashboard_overview.png)
![Dashboard - After Attack Burst](report_assets/final_dashboard_after_burst.png)

## 10. Observed Patterns & Interpretation
(Write 4-6 sentences: what patterns stood out in the logs, how 
signature-based detection and rate-limiting complement each other, why 
the false positives happened, what the before/after accuracy comparison 
shows about rule tuning.)



## 11. Limitations
- IP tracking and bans are stored in memory and reset when the server restarts
- Regex-based rules can be bypassed by heavily obfuscated or encoded payloads
- Only GET/POST on a single route was tested; a production WAF would need 
  to cover all routes and methods
- Testing was done locally, so all traffic originates from one IP (127.0.0.1)

## 12. Future Improvements
- Persist IP bans and logs in a database instead of memory/flat file
- Add machine-learning-based anomaly detection alongside static rules
- Expand coverage to headers, cookies, and file uploads
- Add authentication to protect the `/dashboard` route

## 13. Conclusion
(2-3 sentences summarizing what the project demonstrated and what you learned.)