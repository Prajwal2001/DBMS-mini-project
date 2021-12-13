from flask import Flask, render_template, redirect, request, session
from database import Database
from json import dumps

app = Flask(__name__)
app.secret_key = "dbmsminiproject"

db = Database()
ticket_details = {}


@app.route('/')
def redirect_pg():
    return redirect('/login', code=302)


@app.route('/login', methods=['GET', 'POST'])
def login():
    session["user_id"] = None
    if request.method == 'POST':
        if db.does_user_exist([request.form.get('username'), request.form.get('password')]):
            session["user_id"] = db.get_user_id_by_user_name(
                request.form.get('username'))
            return redirect('/home', code=302)
        else:
            return render_template("index.html", status=False)
    else:
        return render_template("index.html", status=True)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        response = db.add_user([request.form.get('username'),
                                request.form.get('email'),
                                request.form.get('password')])
        return redirect('/login', code=302) if response else render_template("signup.html", status=response)
    else:
        return render_template("signup.html", status=True)


@app.route("/home")
def home():
    if session['user_id']:
        return render_template("home.html")
    else:
        return redirect('/login', code=302)


@app.route("/home/viewtickets")
def viewtickets():
    if session['user_id']:
        return render_template("tickets.html", tickets=db.get_tickets(session['user_id']))
    else:
        return redirect('/login')


@app.route("/home/booktickets", methods=["GET", "POST"])
def booktickets():
    global ticket_details
    if session['user_id']:
        if request.method == 'POST':
            source = request.form.get('source')
            destination = request.form.get('destination')
            travel_date = request.form.get('travel_date')
            ticket_details['source'] = source
            ticket_details['destination'] = destination
            ticket_details['travel_date'] = travel_date
            return redirect("/home/trains")
        return render_template("booktickets.html", stations=db.get_stations())
    return redirect('/login')


@app.route("/home/trains")
def trains():
    global ticket_details
    return render_template("trains.html", trains=db.get_trains(ticket_details['source'], ticket_details['destination']))


@app.route("/signout")
def signout():
    session['user_id'] = None
    return redirect('/login')


if __name__ == '__main__':
    app.run(debug=True, port=4000)
