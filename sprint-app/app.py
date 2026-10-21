from flask import Flask, abort, render_template

app = Flask(__name__)

SERVICES = [
    {"id": 1, "name": "Consultation"},
    {"id": 2, "name": "Medical certificate"},
]

TICKETS = [
    {"number": 1, "name": "Ana", "email": "ana@school.edu", "service_id": 1, "status": "waiting"},
    {"number": 2, "name": "Ben", "email": "ben@school.edu", "service_id": 2, "status": "waiting"},
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

@app.route("/hello")
def hello():
    return "Hello, CCC181!"

if __name__ == "__main__":
    app.run(debug=True)
