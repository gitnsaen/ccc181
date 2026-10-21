from flask import Flask, abort, render_template

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

@app.route("/hello")
def hello():
    return "Hello, CCC181!"

if __name__ == "__main__":
    app.run(debug=True)
