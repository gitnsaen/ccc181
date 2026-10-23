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
#   number     – queue ticket number shown to the student
#   name       – student's full name
#   email      – contact email
#   student_id – university ID number (used to look up later)
#   service_id – foreign key into SERVICES list above
#   doc_name   – file reference (FB message / Gmail subject the student sent)
#   pages      – total pages to print
#   print_type – "bw" (black & white) or "color"
#   is_rush    – True if student paid for rush service
#   status     – "waiting" | "called" | "done"
TICKETS = [
    {
        "number": 1,
        "name": "Carlos Garcia",
        "email": "carlos.garcia@campus.edu",
        "student_id": "2023-14022",
        "service_id": 1,
        "doc_name": "Ethics_CaseStudy_Group4.pdf",
        "pages": 12,
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
        "doc_name": "Architecture_Design_Brief.pdf",
        "pages": 45,
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
        "doc_name": "CapStone_Final_Hardbound.pdf",
        "pages": 120,
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
    return render_template("join.html")


@app.post("/join")
def join():
    """Process the join-queue form submission (POST only).
    
    @app.post() is shorthand for @app.route("/join", methods=["POST"]).
    Having a separate function keeps validation logic isolated and readable.
    This is a minimal placeholder; full validation arrives in Part 5.
    """
    name = request.form.get("name", "").strip()
    if not name:
        # flash() stores a one-time message in the session so the next
        # template render can display it.  "danger" is the Bootstrap
        # alert category (maps to a red alert box).
        flash("Please enter your name.", "danger")
        return redirect(url_for("join_form"))

    number = TICKETS[-1]["number"] + 1 if TICKETS else 1
    TICKETS.append({"number": number, "name": name, "status": "waiting"})
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
