from flask import Flask, abort, redirect, render_template, request, url_for

app = Flask(__name__)

TICKETS = [
    {"number": 12, "name": "Ana"},
    {"number": 14, "name": "Ben"},
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
        TICKETS.append({"number": number, "name": name})
        return redirect(url_for("ticket", ticket_id=number))

    return render_template("join.html")

@app.route("/hello")
def hello():
    return "Hello, CCC181!"

if __name__ == "__main__":
    app.run(debug=True)
