import os
from datetime import timedelta, timezone

from dotenv import load_dotenv
from flask import Flask, abort, flash, redirect, render_template, request, url_for
from flask_migrate import Migrate
from sqlalchemy import func, or_
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


# Helper: position in line
def people_ahead(t):
    """Count tickets still waiting for the same service that joined before t."""
    stmt = (db.select(func.count())
            .select_from(Ticket)
            .where(Ticket.service_id == t.service_id,
                   Ticket.status == "waiting",
                   or_(
                       Ticket.created_at < t.created_at,
                       (Ticket.created_at == t.created_at)
                       & (Ticket.ticket_number < t.ticket_number),
                   )))
    return db.session.scalar(stmt)


# Template filter: local time (Philippine time UTC+8)
@app.template_filter("local")
def local_time(value):
    """Show a database time in Philippine time, e.g. Oct 26, 08:01 AM."""
    return value.astimezone(PH_TIME).strftime("%b %d, %I:%M %p") if value else ""


def all_services():
    return db.session.scalars(
        db.select(Service).order_by(Service.name)
    ).all()


def active_services():
    return db.session.scalars(
        db.select(Service)
        .where(Service.is_active.is_(True))
        .order_by(Service.name)
    ).all()


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
    return render_template("join.html", services=active_services(), form={})


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
    paper_size = form.get("paper_size", "").strip()
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
    if service is None or not service.is_active:
        errors["service_id"] = "Choose a service."
    if sent_via not in ("gmail", "fb"):
        errors["sent_via"] = "Choose how you sent the file (Gmail or FB)."
    if not doc_name:
        errors["doc_name"] = "Enter the document or file reference (e.g., file name sent via FB/Gmail)."

    if not pages_count or pages_count <= 0:
        errors["pages"] = "Enter a valid total number of pages (must be greater than 0)."
    pages = pages_count
    if pages_type == "specific":
        if not pages_range:
            errors["pages"] = "Enter the specific page ranges (e.g., 1-2, 5, 9-10, 15)."
    elif pages_type != "all":
        errors["pages"] = "Choose whether to print all pages or specific pages."

    if print_type not in ("bw", "color"):
        errors["print_type"] = "Choose a print type (B&W or Color)."
    if paper_size not in ("letter", "a4", "legal"):
        errors["paper_size"] = "Choose a paper size."

    if errors:
        flash("Please fix the highlighted fields.", "danger")
        return render_template("join.html", services=active_services(), form=form, errors=errors), 400

    ticket = Ticket(
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
        paper_size=paper_size,
        is_rush=is_rush,
        status="waiting",
    )
    db.session.add(ticket)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        flash("Something went wrong saving your ticket. Please try again.", "danger")
        return render_template(
            "join.html",
            services=active_services(),
            form=form,
            errors={},
        ), 409

    flash(f"You joined the queue. Your ticket is #{ticket.ticket_number}.", "success")
    return redirect(url_for("ticket", ticket_id=ticket.id))


# Student ticket views
@app.route("/queue/<int:ticket_id>")
def ticket(ticket_id):
    t = db.get_or_404(Ticket, ticket_id)

    return render_template("ticket.html", ticket=t, service=t.service, ahead=people_ahead(t))


@app.post("/queue/<int:ticket_id>/leave")
def leave_queue(ticket_id):
    t = db.get_or_404(Ticket, ticket_id)

    if t.status == "waiting":
        t.status = "left"  # soft delete: row stays for reports
        db.session.commit()
    flash("You left the queue.", "info")
    return redirect(url_for("index"))


@app.get("/queue/<int:ticket_id>/status.json")
def ticket_status(ticket_id):
    t = db.get_or_404(Ticket, ticket_id)

    return {"status": t.status, "ahead": people_ahead(t)}


# Staff dashboard views
@app.get("/staff")
def staff_dashboard():
    service_id = request.args.get("service_id", type=int)
    query = db.select(Ticket).where(Ticket.status.in_(["waiting", "called"]))
    waiting_query = db.select(Ticket).where(Ticket.status == "waiting")
    if service_id:
        query = query.where(Ticket.service_id == service_id)
        waiting_query = waiting_query.where(Ticket.service_id == service_id)
    queue = db.session.scalars(
        query.order_by(Ticket.created_at, Ticket.ticket_number)
    ).all()
    next_ticket = db.session.scalar(
        waiting_query
        .order_by(Ticket.created_at, Ticket.ticket_number)
        .limit(1)
    )
    services = all_services()
    return render_template(
        "staff.html",
        queue=queue,
        services=services,
        selected=service_id,
        next_ticket=next_ticket,
    )


@app.post("/staff/call-next")
def call_next():
    service_id = request.form.get("service_id", type=int)
    query = db.select(Ticket).where(Ticket.status == "waiting")
    if service_id:
        query = query.where(Ticket.service_id == service_id)
    ticket = db.session.scalar(
        query.order_by(Ticket.created_at, Ticket.ticket_number).limit(1)
    )
    if ticket is None:
        flash("There are no waiting tickets to call.", "info")
        return redirect(url_for("staff_dashboard", service_id=service_id))

    ticket.status = "called"
    ticket.called_at = func.now()
    db.session.commit()
    flash(f"Ticket #{ticket.ticket_number} called to the counter.", "info")
    return redirect(url_for("staff_dashboard", service_id=service_id))


STAFF_ACTIONS = {"call": "called", "serve": "served", "no-show": "no-show"}


@app.post("/staff/tickets/<int:ticket_id>/<action>")
def staff_action(ticket_id, action):
    new_status = STAFF_ACTIONS.get(action)
    if new_status is None:
        abort(404)
    t = db.get_or_404(Ticket, ticket_id)
    t.status = new_status
    if new_status == "called":
        t.called_at = func.now()
    elif new_status == "served":
        t.served_at = func.now()
    db.session.commit()
    flash(f"Ticket #{t.ticket_number} marked {new_status}.", "info")
    return redirect(url_for("staff_dashboard"))


@app.post("/staff/tickets/<int:ticket_id>/delete")
def delete_ticket(ticket_id):
    t = db.get_or_404(Ticket, ticket_id)
    db.session.delete(t)  # hard delete: the row is gone for good
    db.session.commit()
    flash(f"Ticket #{t.ticket_number} was deleted.", "warning")
    return redirect(url_for("staff_dashboard"))


# Services management routes
@app.get("/staff/services")
def services_list():
    services = db.session.scalars(db.select(Service).order_by(Service.name)).all()
    return render_template("services.html", services=services)


@app.post("/staff/services")
def service_create():
    name = request.form.get("name", "").strip()
    code = request.form.get("code", "").strip()
    if not name or len(name) > 100 or not code or len(code) > 30:
        flash("Enter a name (up to 100 characters) and a code (up to 30 characters).", "danger")
        return redirect(url_for("services_list"))
    db.session.add(Service(name=name, code=code))
    try:
        db.session.commit()
        flash(f"Service \"{name}\" added.", "success")
    except IntegrityError:
        db.session.rollback()
        flash(f"A service with this name or code already exists.", "danger")
    return redirect(url_for("services_list"))


@app.post("/staff/services/<int:service_id>/edit")
def service_edit(service_id):
    s = db.session.get(Service, service_id)
    if s is None:
        abort(404)
    name = request.form.get("name", "").strip()
    code = request.form.get("code", "").strip()
    if not name or len(name) > 100 or not code or len(code) > 30:
        flash(
            "Enter a name (up to 100 characters) and a code (up to 30 characters).",
            "danger",
        )
        return redirect(url_for("services_list"))
    s.name = name
    s.code = code
    s.is_active = request.form.get("is_active") == "on"
    try:
        db.session.commit()
        flash(f"Service \"{s.name}\" updated.", "success")
    except IntegrityError:
        db.session.rollback()
        flash(f"A service with this name or code already exists.", "danger")
    return redirect(url_for("services_list"))


@app.post("/staff/services/<int:service_id>/delete")
def service_delete(service_id):
    s = db.session.get(Service, service_id)
    if s is None:
        abort(404)
    if s.tickets:
        flash(f"\"{s.name}\" has tickets, so it cannot be deleted. Turn it off instead.", "danger")
        return redirect(url_for("services_list"))
    db.session.delete(s)
    db.session.commit()
    flash(f"Service \"{s.name}\" deleted.", "warning")
    return redirect(url_for("services_list"))


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
