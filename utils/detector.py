import re

PATTERNS = [
    r"(\bor\b\s+\d+=\d+)",
    r"(\band\b\s+\d+=\d+)",
    r"union\s+select",
    r"drop\s+table",
    r"insert\s+into",
    r"delete\s+from",
    r"update\s+\w+\s+set",
    r"--",
    r"/\*",
    r"\*/",
    r"xp_cmdshell",
    r"exec\s",
    r"sleep\s*\(",
    r"benchmark\s*\(",
]

def detect_sql_injection(user_input):

    score = 0
    findings = []

    for pattern in PATTERNS:

        if re.search(pattern, user_input, re.IGNORECASE):

            score += 10
            findings.append(pattern)

    if score == 0:
        risk = "Safe"

    elif score < 30:
        risk = "Low"

    elif score < 60:
        risk = "Medium"

    else:
        risk = "High"

    return {
        "risk": risk,
        "score": score,
        "matches": findings
    }