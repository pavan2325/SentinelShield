import re

RULES = {
    "SQL Injection": [
        r"('|%27)\s*(or|and)\s*('|\d|%27)",
        r"('|%27)\s*(--|%2d%2d|#|%23)",
        r"union(\s|%20|\+)+select",
        r"select.+from",
        r"\b(drop|insert|delete)\b\s+(table|into|from)"
    ],
    "XSS": [
        r"<script",
        r"%3Cscript",
        r"\bon\w+\s*=",
        r"javascript:"
    ],
    "Directory Traversal": [
        r"\.\./",
        r"\.\.\\",
        r"%2e%2e(%2f|/|\\)"
    ],
    "Local File Inclusion": [
        r"/etc/(passwd|shadow)",
        r"win\.ini",
        r"(file|php|data|expect)://",
        r"/proc/self"
    ],
    "Command Injection": [
        r"(;|\|\||&&|\|)\s*(ls|cat|whoami|id|pwd|wget|curl|nc)\b",
        r"`[^`]+`",
        r"\$\([^)]+\)"
    ]
}

def check_request(data: str):
    for category, patterns in RULES.items():
        for pattern in patterns:
            if re.search(pattern, data, re.IGNORECASE):
                return category
    return None