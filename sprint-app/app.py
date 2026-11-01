import os
from datetime import timedelta, timezone

from dotenv import load_dotenv
from flask import Flask, abort, flash, redirect, render_template, request, url_for
from flask_migrate import Migrate
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError

from models import Service, Operator, Ticket, db

load_dotenv()

# Philippine time zone (UTC+8, no daylight saving)
PH_TIME = timezone(timedelta(hours=8))

app = Flask(__name__)
app.secret_key = "sprint_dev_flask_secret_key_8d1ee41d"
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["DATABASE_URL"]
app.config["SQLALCHEMY_ECHO"] = os.environ.get("SQLALCHEMY_ECHO") == "1"

db.init_app(app)
migrate = Migrate(app, db)


# Helper: all active services
def all_services():
    return db.session.scalars(db.select(Service).where(Service.is_active == True).order_by(Service.name)).all()


# Helper: position in line
def people_ahead(t):
    """Count tickets still waiting for the same service that joined before t."""
    stmt = (db.select(func.count())
            .select_from(Ticket)
            .where(Ticket.service_id == t.service_id,
                   Ticket.status == "waiting",
                   Ticket.created_at < t.created_at))
    return db.session.scalar(stmt)


# Template filter: local time (Philippine time UTC+8)
@app.template_filter("local")
def local_time(value):
    """Show a database time in Philippine time, e.g. Oct 26, 08:01 AM."""
    return value.astimezone(PH_TIME).strftime("%b %d, %I:%M %p") if value else ""


# Helper: all active services
def all_services():
    return db.session.scalars(db.select(Service).where(Service.is_active == True).order_by(Service.name)).all()


# Home route
@app.route("/")
def index():
    tickets = db.session.scalars(
        db.select(Ticket)
        .where(Ticket.status.in_(["waiting", "called"]))
        .order_by(Ticket.created_at)
    ).all()
    return render_template("index.html", tickets=tickets)


# Join queue routes
@app.get("/join")
def join_form():
    return render_template("join.html", services=all_services(), form={})


@app.post("/join")
def join():
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

    service = db.session.get(Service, service_id) if service_id else None

    errors = {}
    if not name or len(name) > 100:
        errors["name"] = "Enter your name (up to 100 characters)."
    if "@" not in email or len(email) > 255:
        errors["email"] = "Enter a valid email address."
    if not student_id or len(student_id) > 20:
        errors["student_id"] = "Enter your student ID (up to 20 characters)."
    if service is None:
        errors["service_id"] = "Choose a service."
    if sent_via not in ("gmail", "fb"):
        errors["sent_via"] = "Choose how you sent the file (Gmail or FB)."
    if not doc_name:
        errors["doc_name"] = "Enter the document or file reference (e.g., file name sent via FB/Gmail)."

    if pages_type == "all":
        if not pages_count or pages_count <= 0:
            errors["pages"] = "Enter a valid number of pages (must be greater than 0)."
        pages = pages_count
    elif pages_type == "specific":
        if not pages_range:
            errors["pages"] = "Enter the specific page ranges (e.g., 1-2, 5, 9-10, 15)."
        pages = len(pages_range.split(",")) if pages_range else 0
    else:
        errors["pages"] = "Choose whether to print all pages or specific pages."

    if print_type not in ("bw", "color"):
        errors["print_type"] = "Choose a print type (B&W or Color)."

    if errors:
        flash("Please fix the highlighted fields.", "danger")
        return render_template("join.html", services=all_services(), form=form, errors=errors), 400

    # Allocate next ticket number (monotonic)
    max_number = db.session.scalar(db.select(func.max(Ticket.ticket_number)))
    ticket_number = (max_number + 1) if max_number is not None else 1

    ticket = Ticket(
        ticket_number=ticket_number,
        name=name,
        email=email,
        student_id=student_id,
        service=service,
        sent_via=sent_via,
        doc_name=doc_name,
        pages=pages,
        pages_type=pages_type,
        pages_range=pages_range if pages_type == "specific" else None,
        print_type=print_type,
        paper_size="letter",  # Default, can be enhanced later
        is_rush=is_rush,
        status="waiting",
    )
    db.session.add(ticket)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        flash("Something went wrong saving your ticket. Please try again.", "danger")
        return render_template("join.html", services=all_services(), form=form, errors={}), 409

    flash(f"You joined the queue. Your ticket is #{ticket.ticket_number}.", "success")
    return redirect(url_for("ticket", ticket_id=ticket.ticket_number))


# Student ticket views
@app.route("/queue/<int:ticket_id>")
def ticket(ticket_id):
    t = db.session.scalar(db.select(Ticket).where(Ticket.ticket_number == ticket_id))
    if t is None:
        abort(404)

    return render_template("ticket.html", ticket=t, service=t.service, ahead=people_ahead(t))


@app.post("/queue/<int:ticket_id>/leave")
def leave_queue(ticket_id):
    t = db.session.scalar(db.select(Ticket).where(Ticket.ticket_number == ticket_id))
    if t is None:
        abort(404)

    t.status = "no-show"
    db.session.commit()
    flash(f"Ticket #{ticket_id} has been removed from the queue.", "info")
    return redirect(url_for("index"))


@app.get("/queue/<int:ticket_id>/status.json")
def ticket_status(ticket_id):
    t = db.session.scalar(db.select(Ticket).where(Ticket.ticket_number == ticket_id))
    if t is None:
        abort(404)

    return {"status": t.status, "ahead": people_ahead(t)}


# Staff dashboard views
@app.get("/staff")
def staff_dashboard():
    service_id = request.args.get("service_id", type=int)
    query = db.select(Ticket).where(Ticket.status.in_(["waiting", "called"]))
    if service_id:
        query = query.where(Ticket.service_id == service_id)
    queue = db.session.scalars(query.order_by(Ticket.created_at)).all()
    services = all_services()
    return render_template(
        "staff.html", queue=queue, services=services, selected=service_id
    )


@app.post("/staff/tickets/<int:ticket_id>/<action>")
def staff_action(ticket_id, action):
    new_status = {"call": "called", "serve": "served", "no-show": "no-show"}.get(action)
    t = db.session.scalar(db.select(Ticket).where(Ticket.ticket_number == ticket_id))
    if t is None or new_status is None:
        abort(404)
    t.status = new_status
    if new_status == "called":
        t.called_at = func.now()
    elif new_status == "served":
        t.served_at = func.now()
    db.session.commit()
    flash(f"Ticket #{ticket_id} marked {new_status}.", "info")
    return redirect(url_for("staff_dashboard"))


@app.cli.command("seed")
def seed():
    """Add the starting services if they are not there yet."""
    starting = [
        ("Document Printing (B&W / Color)", "print_doc"),
        ("Thesis & Manuscript Binding", "bind_thesis"),
        ("Large Format Poster & Plan Plotting", "plot_poster"),
        ("Scanning & Photocopying", "scan_copy"),
    ]
    for name, code in starting:
        exists = db.session.scalar(db.select(Service).filter_by(name=name))
        if exists is None:
            db.session.add(Service(name=name, code=code))
    db.session.commit()
    print("Services are ready.")


if __name__ == "__main__":
    app.run(debug=True)
