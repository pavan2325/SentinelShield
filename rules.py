import re

RULES = {
    "SQL Injection": [
        r"(\%27)|(\')|(\-\-)|(\%23)|(#)",
        r"union\s+select",
        r"select.+from"
    ],
    "XSS": [
        r"<script.*?>",
        r"onerror\s*=",
        r"javascript:"
    ],
    "Directory Traversal": [
        r"\.\./",
        r"\.\.\\"
    ],
    "Command Injection": [
        r";\s*ls",
        r";\s*cat",
        r"\|\s*whoami"
    ]
}

def check_request(data: str):
    for category, patterns in RULES.items():
        for pattern in patterns:
            if re.search(pattern, data, re.IGNORECASE):
                return category
    return None