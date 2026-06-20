from flask import Flask, render_template, request, redirect, url_for, session
from config import Config
from models import db, ScanHistory
from utils.capability import analyze_query
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter
from flask import send_file

import datetime

app = Flask(__name__)
app.config.from_object(Config)

app.secret_key = Config.SECRET_KEY

db.init_app(app)

with app.app_context():
    db.create_all()


# -------------------------
# SECURITY GATE (NEW)
# -------------------------

ACCESS_CODE = "CODEALPHA-SECURE-2026"


@app.route("/login", methods=["GET", "POST"])
def login():

    error = None

    if request.method == "POST":

        code = request.form.get("code")

        if code == ACCESS_CODE:
            session["authorized"] = True
            return redirect(url_for("index"))
        else:
            error = "Invalid Access Code"

    return render_template("login.html", error=error)


@app.route("/")
def index():

    if not session.get("authorized"):
        return redirect(url_for("login"))

    total = ScanHistory.query.count()

    high = ScanHistory.query.filter_by(result="High").count()

    medium = ScanHistory.query.filter_by(result="Medium").count()

    low = ScanHistory.query.filter_by(result="Low").count()   

    safe = ScanHistory.query.filter_by(result="Safe").count()

    return render_template(
        "index.html",
        result=None,
        total=total,
        high=high,
        medium=medium,
        low=low,
        safe=safe
    )


@app.route("/scan", methods=["POST"])
def scan():

    if not session.get("authorized"):
        return redirect(url_for("login"))

    query = request.form.get("query")

    # run detection engine
    result = analyze_query(query)

    # save to database
    history = ScanHistory(
        sql_query=query,
        result=result["risk"],
        risk_score=result["score"]
    )

    db.session.add(history)
    db.session.commit()

    # log to security file
    with open("security.log", "a") as log_file:
        log_file.write("\n====================\n")
        log_file.write(f"Query: {query}\n")
        log_file.write(f"Risk: {result['risk']}\n")
        log_file.write(f"Score: {result['score']}\n")

        if result["matches"]:
            log_file.write("Matches: " + ", ".join(str(m) for m in result["matches"]) + "\n")

        log_file.write("====================\n")

    return render_template("index.html", result=result)


@app.route("/history")
def history():

    if not session.get("authorized"):
        return redirect(url_for("login"))

    scans = ScanHistory.query.order_by(
        ScanHistory.created_at.desc()
    ).all()

    return render_template("history.html", scans=scans)


@app.route("/logout")
def logout():

    session.clear()
    return redirect(url_for("login"))


@app.route("/dashboard")
def dashboard():

    if not session.get("authorized"):
        return redirect(url_for("login"))

    total = ScanHistory.query.count()
    high = ScanHistory.query.filter_by(result="High").count()
    medium = ScanHistory.query.filter_by(result="Medium").count()
    low = ScanHistory.query.filter_by(result="Low").count()
    safe = ScanHistory.query.filter_by(result="Safe").count()

    return render_template(
        "dashboard.html",
        total=total,
        high=high,
        medium=medium,
        low=low,
        safe=safe
    )

@app.route("/export-report")
def export_report():

    if not session.get("authorized"):
        return redirect(url_for("login"))

    scans = ScanHistory.query.order_by(ScanHistory.created_at.desc()).all()

    file_path = "security_report.pdf"
    doc = SimpleDocTemplate(file_path, pagesize=letter)

    styles = getSampleStyleSheet()
    content = []

    content.append(Paragraph("SQL Injection Security Report", styles["Title"]))
    content.append(Spacer(1, 12))

    for scan in scans[:20]:
        text = f"""
        Query: {scan.sql_query}<br/>
        Risk: {scan.result}<br/>
        Score: {scan.risk_score}<br/>
        """
        content.append(Paragraph(text, styles["Normal"]))
        content.append(Spacer(1, 10))

    doc.build(content)

    return send_file(file_path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)