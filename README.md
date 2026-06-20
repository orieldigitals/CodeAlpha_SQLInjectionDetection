# SQL Injection Detection System

## Overview

The SQL Injection Detection System is a web-based security application developed with Flask that analyzes SQL queries and identifies potential SQL injection attacks using a rule-based detection engine with intelligent risk scoring.

The application enables users to submit SQL queries, evaluate their security posture, classify them into different risk levels, maintain a history of previous scans, visualize security analytics through an interactive dashboard, generate downloadable PDF security reports, and maintain audit logs for security monitoring.

This project was developed as part of the CodeAlpha Cloud Computing Internship to demonstrate secure application development, cybersecurity fundamentals, backend development, data persistence, reporting, and dashboard visualization.

---

## Problem Statement

SQL Injection remains one of the most common web application vulnerabilities. Poorly validated SQL queries can allow attackers to:

* Bypass authentication
* Read sensitive database information
* Modify or delete records
* Execute administrative database commands
* Compromise entire applications

Manually identifying suspicious SQL statements can be time-consuming.

This project provides an automated solution that analyzes SQL queries, detects potentially dangerous patterns, assigns a risk score, explains why the query is considered risky, and records every scan for future analysis.

---

## Features

### SQL Query Analysis

* Scan SQL statements for suspicious injection patterns
* Analyze queries using a custom rule-based detection engine
* Detect common SQL injection techniques

### Intelligent Risk Classification

Queries are classified into four categories:

* Safe
* Low Risk
* Medium Risk
* High Risk

Each scan also receives a numerical risk score based on the detected patterns.

---

### Security Explanations

Instead of only displaying a risk level, the system explains why the query is considered suspicious.

Example explanations include:

* Detected SQL comment sequence
* UNION-based injection detected
* Boolean-based authentication bypass detected
* Dangerous SQL command identified
* Command execution pattern detected

---

### Dashboard Analytics

The dashboard provides a visual overview of system activity, including:

* Total scans performed
* High-risk detections
* Medium-risk detections
* Low-risk detections
* Safe queries

Interactive charts provide quick insight into the security posture of analyzed queries.

---

### Scan History

Every scan is permanently stored in the SQLite database, including:

* SQL query
* Risk level
* Risk score
* Date and time scanned

This provides an audit trail for future review.

---

### Security Logging

Each scan is also written to a dedicated security log file.

The log contains:

* Submitted SQL query
* Risk classification
* Risk score
* Detected attack patterns

This simulates real-world security event logging.

---

### PDF Security Report Generator

The application can generate downloadable PDF reports containing previously scanned SQL queries and their corresponding security analysis.

The generated report includes:

* SQL query
* Risk level
* Risk score

This feature demonstrates automated reporting commonly found in enterprise security solutions.

---

### Access Control

The application is protected using a simple access code authentication mechanism before users can access the detection system.

Although intentionally lightweight for demonstration purposes, this simulates an initial security layer before accessing administrative functionality.

---

## Detection Techniques

The detection engine analyzes SQL statements for multiple suspicious patterns, including:

* SQL comments
* UNION injection
* Boolean-based injection
* DROP statements
* DELETE statements
* INSERT statements
* UPDATE statements
* EXEC statements
* xp_cmdshell execution
* Information schema access
* Sleep/time-delay attacks
* Hexadecimal encoding
* OR-based authentication bypass
* Multiple statement execution

Each detected pattern contributes to the final security score.

---

## Technology Stack

### Backend

* Python
* Flask
* Flask SQLAlchemy

### Database

* SQLite

### Frontend

* HTML5
* CSS3
* Bootstrap 5
* JavaScript
* Chart.js

### Reporting

* ReportLab

---

## Project Structure

```
SQL-Injection-Detection-System/
│
├── app.py
├── config.py
├── models.py
├── requirements.txt
├── security.log
│
├── database/
│   └── scan_history.db
│
├── utils/
│   └── capability.py
│
├── templates/
│   ├── base.html
│   ├── login.html
│   ├── index.html
│   ├── history.html
│   └── dashboard.html
│
├── static/
│   ├── css/
│   └── images/
│
└── README.md
```

---

## Installation

Clone the repository.

```bash
git clone https://github.com/yourusername/sql-injection-detection-system.git
```

Navigate into the project.

```bash
cd sql-injection-detection-system
```

Create a virtual environment.

Windows

```bash
python -m venv venv
venv\Scripts\activate
```

Linux/macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

Install the required dependencies.

```bash
pip install -r requirements.txt
```

Run the application.

```bash
python app.py
```

Open your browser.

```
http://127.0.0.1:5000
```

---

## Sample Test Queries

### Safe

```sql
SELECT * FROM users;
```

```sql
SELECT name FROM customers WHERE id = 5;
```

---

### Low Risk

```sql
SELECT * FROM users WHERE id=1 OR 1=1;
```

```sql
SELECT * FROM products -- fetch all products
```

---

### Medium Risk

```sql
DROP TABLE users;
```

```sql
SELECT * FROM users UNION SELECT username,password FROM admin;
```

---

### High Risk

```sql
'; DROP TABLE users; --
```

```sql
SELECT * FROM users WHERE id=1; EXEC xp_cmdshell('dir');
```

---

## Screenshots

The following screenshots demonstrate the application.

* Login Screen
* SQL Scanner
* Scan Results
* Security Explanation
* Dashboard
* History Page
* PDF Report

(Add screenshots after deployment.)

---

## Future Improvements

Possible future enhancements include:

* Machine learning-based detection
* Natural language attack explanations
* User authentication with database accounts
* Role-based access control
* REST API
* Email security alerts
* Export to CSV and Excel
* Docker support
* PostgreSQL integration
* Cloud deployment
* Threat intelligence integration
* Detection confidence scoring
* Real-time monitoring dashboard
* JWT authentication
* CI/CD pipeline integration

---

## Learning Outcomes

This project demonstrates practical experience with:

* Flask application development
* Backend architecture
* SQL injection detection concepts
* Cybersecurity fundamentals
* Secure coding principles
* SQLite database management
* ORM using SQLAlchemy
* Dashboard development
* PDF generation
* Logging and auditing
* Data visualization
* Authentication
* Web application deployment

---

## Author

**Hope Fanwi Bongnwi**

Cloud Engineer | DevOps Enthusiast | Backend Developer | Cybersecurity Learner

GitHub: https://github.com/yourusername

LinkedIn: www.linkedin.com/in/hope-bongnwi

---

## License

This project was developed for educational purposes as part of the CodeAlpha Cloud Computing Internship.

It may be used as a reference for learning, experimentation, and portfolio demonstration.
