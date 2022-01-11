from flask import Flask, render_template, redirect, request, session
from database import Database
from pprint import pprint
from datetime import date

app = Flask(__name__)
app.secret_key = "dbmsminiproject"

db = Database()
passengerDetails = {}


@app.route('/')
def redirect_pg():
    return redirect('/login')


@app.route('/login', methods=['GET', 'POST'])
def login():
    session["user_id"] = None
    if request.method == 'POST':
        if db.does_user_exist([request.form.get('username'), request.form.get('password')]):
            session["user_id"] = db.get_user_id_by_user_name(
                request.form.get('username'))
            return redirect('/home')
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
    return render_template("home.html") if session['user_id'] else redirect('/login', code=302)


@app.route("/home/viewtickets")
def viewtickets():
    return render_template("tickets.html", tickets=db.get_tickets(session['user_id'])) if session['user_id'] else redirect('/login')


@app.route("/home/booktickets", methods=["GET", "POST"])
def booktickets():
    global passengerDetails
    if session['user_id']:
        if request.method == 'POST':
            source = request.form.get('source')
            destination = request.form.get('destination')
            travel_date = request.form.get('travel_date')
            passengerDetails['source'] = source
            passengerDetails['destination'] = destination
            passengerDetails['travel_date'] = travel_date
            return redirect("/home/trains")
        today = date.today()
        return render_template("booktickets.html", stations=db.get_stations(), min_date="%d-%.2d-%.2d" % (today.year, today.month, today.day), max_date="%d-%.2d-%.2d" % (today.year + 1, today.month, today.day))
    return redirect('/login')


@app.route('/home/getalltrainsinfo')
def get_all_trains_info():
    return render_template("trainsinfo.html", trainsinfo=db.get_train_details()) if session['user_id'] else redirect("/login")


@app.route("/home/trains")
def trains():
    global passengerDetails
    if session['user_id']:
        return render_template("trains.html", trains=db.get_trains(passengerDetails['source'], passengerDetails['destination']))
    return redirect('/login')


@app.route("/home/<int:train_no>")
def get_train_no(train_no):
    global passengerDetails
    passengerDetails['train_no'] = train_no
    passengerDetails['passengers'] = []
    passengerDetails['user_id'] = session['user_id']
    return redirect("/home/addpassengers")


@app.route('/home/addpassengers', methods=['GET', 'POST'])
def addpassengers():
    global passengerDetails
    if session['user_id']:
        if request.method == 'POST':
            name = request.form.get('p_name')
            age = int(request.form.get('p_age'))
            passengerDetails['passengers'].append({
                'p_name': name,
                'p_age': age
            })
        return render_template("addpassengers.html", passengers=passengerDetails['passengers'])
    return redirect("/login")


@app.route("/home/reserveticket")
def reserveticket():
    global passengerDetails
    if session['user_id']:
        db.add_passengers_ticket(passengerDetails)
        return redirect("/home/viewtickets")
    return redirect("/login")


@app.route('/home/cancelticket/<int:pnr>')
def cancelticket(pnr):
    db.cancel_ticket(pnr)
    return redirect('/home/viewtickets')


@app.route('/home/payment', methods=['GET', 'POST'])
def payment():
    global passengerDetails
    if session['user_id']:
        if request.method == 'POST':
            return redirect('/home/reserveticket')
        return render_template("payment.html", amount=db.get_totalprice(passengerDetails))
    return redirect("/login")


@app.route("/signout")
def signout():
    session['user_id'] = None
    return redirect('/login')


if __name__ == '__main__':
    app.run(debug=True, port=4000)
