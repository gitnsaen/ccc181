from flask import Flask, abort, flash, redirect, render_template, request, url_for

# ── App setup ──────────────────────────────────────────────────────────────────
app = Flask(__name__)

# secret_key is required by Flask whenever you use the session or flash()
# function.  Without it Flask raises a RuntimeError at startup.
# In production this would be a long random string kept in an environment
# variable; for development any string works.
app.secret_key = "sprint-dev-secret"

# ── In-memory data ─────────────────────────────────────────────────────────────

# List of services offered at the campus print shop.
# Each dict has an "id" (used in forms and tickets) and a human-readable "name".
SERVICES = [
    {"id": 1, "name": "Document Printing (B&W / Color)"},
    {"id": 2, "name": "Thesis & Manuscript Binding"},
    {"id": 3, "name": "Large Format Poster & Plan Plotting"},
    {"id": 4, "name": "Scanning & Photocopying"},
]

# Seed queue data representing active print jobs.
# Fields:
#   number       – queue ticket number shown to the student
#   name         – student's full name
#   email        – contact email
#   student_id   – university ID number (used to look up later)
#   service_id   – foreign key into SERVICES list above
#   sent_via     – "gmail" or "fb" (how the file was sent)
#   doc_name     – file reference (FB message / Gmail subject the student sent)
#   pages        – total pages to print
#   pages_type   – "all" or "specific"
#   pages_range  – page range string if pages_type is "specific"
#   print_type   – "bw" (black & white) or "color"
#   is_rush      – True if student paid for rush service
#   status       – "waiting" | "called" | "done"
TICKETS = [
    {
        "number": 1,
        "name": "Carlos Garcia",
        "email": "carlos.garcia@campus.edu",
        "student_id": "2023-14022",
        "service_id": 1,
        "sent_via": "gmail",
        "doc_name": "Ethics_CaseStudy_Group4.pdf",
        "pages": 12,
        "pages_type": "all",
        "pages_range": None,
        "print_type": "bw",
        "is_rush": False,
        "status": "called",
    },
    {
        "number": 2,
        "name": "Janelle Diaz",
        "email": "jdiaz@campus.edu",
        "student_id": "2022-09411",
        "service_id": 1,
        "sent_via": "fb",
        "doc_name": "Architecture_Design_Brief.pdf",
        "pages": 45,
        "pages_type": "all",
        "pages_range": None,
        "print_type": "color",
        "is_rush": True,
        "status": "waiting",
    },
    {
        "number": 3,
        "name": "Marcus Lim",
        "email": "mlim@campus.edu",
        "student_id": "2024-31002",
        "service_id": 2,
        "sent_via": "gmail",
        "doc_name": "CapStone_Final_Hardbound.pdf",
        "pages": 120,
        "pages_type": "all",
        "pages_range": None,
        "print_type": "bw",
        "is_rush": False,
        "status": "waiting",
    },
]


# ── Routes ─────────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    """Home page – shows a welcome message and a button to join the queue."""
    return render_template("index.html", tickets=TICKETS)


@app.get("/join")
def join_form():
    """Show the empty join-queue form (GET only).

    We split GET and POST into separate functions so each has one job.
    Flask's @app.get() decorator is shorthand for
    @app.route("/join", methods=["GET"]).
    The function name 'join_form' is what url_for() uses in templates.
    """
    return render_template("join.html", services=SERVICES, form={})


@app.post("/join")
def join():
    """Process the join-queue form submission (POST only).

    @app.post() is shorthand for @app.route("/join", methods=["POST"]).
    Having a separate function keeps validation logic isolated and readable.
    Full server-side validation for all sPrint-specific fields.
    """
    form = request.form
    name = form.get("name", "").strip()
    email = form.get("email", "").strip().lower()
    student_id = form.get("student_id", "").strip()
    service_id = form.get("service_id", type=int)
    sent_via = form.get("sent_via", "").strip()
    doc_name = form.get("doc_name", "").strip()
    pages_type = form.get("pages_type", "").strip()
    pages_count = form.get("pages_count", type=int)
    pages_range = form.get("pages_range", "").strip()
    print_type = form.get("print_type", "").strip()
    is_rush = form.get("is_rush") == "on"

    errors = {}
    if not name:
        errors["name"] = "Enter your name."
    if "@" not in email:
        errors["email"] = "Enter a valid email address."
    if not student_id:
        errors["student_id"] = "Enter your student ID."
    if service_id not in [s["id"] for s in SERVICES]:
        errors["service_id"] = "Choose a service."
    if not doc_name:
        errors["doc_name"] = "Enter the document or file reference (e.g., file name sent via FB/Gmail)."

    # Validate pages based on type selected
    if pages_type == "all":
        if not pages_count or pages_count <= 0:
            errors["pages"] = "Enter a valid number of pages (must be greater than 0)."
        pages = pages_count
    elif pages_type == "specific":
        if not pages_range:
            errors["pages"] = "Enter the specific page ranges (e.g., 1-2, 5, 9-10, 15)."
        pages = len(pages_range.split(",")) if pages_range else 0  # Approximate count
    else:
        errors["pages"] = "Choose whether to print all pages or specific pages."

    if print_type not in ("bw", "color"):
        errors["print_type"] = "Choose a print type (B&W or Color)."

    if errors:
        flash("Please fix the highlighted fields.", "danger")
        return render_template("join.html", services=SERVICES, form=form, errors=errors), 400

    number = TICKETS[-1]["number"] + 1 if TICKETS else 1
    TICKETS.append({
        "number": number,
        "name": name,
        "email": email,
        "student_id": student_id,
        "service_id": service_id,
        "sent_via": sent_via,
        "doc_name": doc_name,
        "pages": pages,
        "pages_type": pages_type,
        "pages_range": pages_range if pages_type == "specific" else None,
        "print_type": print_type,
        "is_rush": is_rush,
        "status": "waiting"
    })
    flash(f"You joined the queue. Your ticket is #{number}.", "success")
    return redirect(url_for("ticket", ticket_id=number))


@app.route("/queue/<int:ticket_id>")
def ticket(ticket_id):
    """Show a student's personal ticket / queue position page."""
    for position, t in enumerate(TICKETS, start=1):
        if t["number"] == ticket_id:
            return render_template("ticket.html", ticket=t, position=position)
    abort(404)


@app.get("/staff")
def staff_dashboard():
    """Staff dashboard – placeholder for Part 7.
    
    Passes the full TICKETS list and SERVICES list to the template.
    The template will be built out properly in Part 7.
    """
    return render_template("staff.html", tickets=TICKETS, services=SERVICES)


# ── Dev entry point ────────────────────────────────────────────────────────────

if __name__ == "__main__":
    app.run(debug=True)
