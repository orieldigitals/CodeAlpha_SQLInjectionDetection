import re

# ----------------------------
# INTELLIGENT SQL INJECTION ANALYZER
# ----------------------------

PATTERNS = [
    {
        "name": "Authentication Bypass (OR 1=1)",
        "pattern": r"or\s+1=1",
        "score": 40,
        "type": "critical",
        "explanation": "Tautology used to bypass login authentication"
    },
    {
        "name": "Union-based Injection",
        "pattern": r"union\s+select",
        "score": 50,
        "type": "critical",
        "explanation": "Attempts to extract data from other database tables"
    },
    {
        "name": "SQL Comment Injection",
        "pattern": r"--",
        "score": 15,
        "type": "low",
        "explanation": "Used to ignore rest of SQL query"
    },
    {
        "name": "Stacked Query Attack",
        "pattern": r";",
        "score": 20,
        "type": "medium",
        "explanation": "Allows execution of multiple SQL statements"
    },
    {
        "name": "Database Destruction Attempt",
        "pattern": r"drop\s+table",
        "score": 60,
        "type": "critical",
        "explanation": "Attempts to delete entire database table"
    },
    {
        "name": "Data Manipulation Attack",
        "pattern": r"update\s+.*set",
        "score": 35,
        "type": "high",
        "explanation": "Attempts to modify database records"
    },
    {
        "name": "System Command Execution",
        "pattern": r"xp_cmdshell",
        "score": 70,
        "type": "critical",
        "explanation": "Attempts to execute OS-level commands via SQL Server"
    }
]


def analyze_query(query: str):
    if not query:
        return {
            "risk": "Safe",
            "score": 0,
            "matches": [],
            "explanations": []
        }

    query_lower = query.lower()

    total_score = 0
    matches = []
    explanations = []
    severity_hits = {"critical": 0, "high": 0, "medium": 0, "low": 0}

    for item in PATTERNS:
        if re.search(item["pattern"], query_lower):
            total_score += item["score"]
            matches.append(item["name"])
            explanations.append(item["explanation"])
            severity_hits[item["type"]] += 1

    # ----------------------------
    # FINAL RISK DECISION (SMARTER)
    # ----------------------------

    if severity_hits["critical"] >= 1 or total_score >= 70:
        risk = "High"
    elif severity_hits["high"] >= 1 or total_score >= 40:
        risk = "Medium"
    elif total_score > 0:
        risk = "Low"
    else:
        risk = "Safe"

    return {
        "risk": risk,
        "score": total_score,
        "matches": matches,
        "explanations": explanations,
        "severity": severity_hits
    }