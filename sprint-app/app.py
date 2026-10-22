from flask import Flask, abort, redirect, render_template, request, url_for

app = Flask(__name__)

# List of services available at the campus print shop
SERVICES = [
    {"id": 1, "name": "Document Printing (B&W / Color)"},
    {"id": 2, "name": "Thesis & Manuscript Binding"},
    {"id": 3, "name": "Large Format Poster & Plan Plotting"},
    {"id": 4, "name": "Scanning & Photocopying"},
]

# Seed queue data representing active print jobs
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


@app.route("/")
def index():
    return render_template("index.html", tickets=TICKETS)


@app.route("/queue/<int:ticket_id>")
def ticket(ticket_id):
    for position, t in enumerate(TICKETS, start=1):
        if t["number"] == ticket_id:
            return render_template("ticket.html", ticket=t, position=position)
    abort(404)


@app.route("/join", methods=["GET", "POST"])
def join():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        if not name:
            return render_template("join.html", error="Please enter your name.")

        number = TICKETS[-1]["number"] + 1 if TICKETS else 1
        TICKETS.append({"number": number, "name": name, "status": "waiting"})
        return redirect(url_for("ticket", ticket_id=number))

    return render_template("join.html")


@app.route("/hello")
def hello():
    return "Hello, CCC181!"


if __name__ == "__main__":
    app.run(debug=True)
