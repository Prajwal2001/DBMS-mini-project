from flask import Flask, render_template, redirect, request, session
from database import Database
from datetime import date

app = Flask(__name__)
app.secret_key = "dbmsminiproject"

db = Database()


@app.route('/')
def redirect_pg():
    return redirect('/login')


@app.route('/login', methods=['GET', 'POST'])
def login():
    session["user_id"] = ""
    session["user_name"] = ""
    if request.method == 'POST':
        if db.does_user_exist(request.form):
            session["user_id"] = db.get_user_id_by_user_name(
                request.form.get('username'))
            session["user_name"] = request.form.get('username').title()
            return redirect('/home')
        return render_template("index.html", status=False)
    return render_template("index.html", status=True)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        response = db.add_user(request.form)
        return redirect('/login', code=302) if response else render_template("signup.html", status=response)
    return render_template("signup.html", status=True)


@app.context_processor
def general_data():
    return dict(user_name=session.get("user_name"))


@app.route("/home")
def home():
    return render_template("home.html") if session.get("user_id") else redirect('/login', code=302)


@app.route("/home/viewtickets")
def viewtickets():
    return render_template("tickets.html", tickets=db.get_tickets(session.get("user_id"))) if session.get("user_id") else redirect('/login')


@app.route("/home/booktickets", methods=["GET", "POST"])
def booktickets():
    if session.get("user_id"):
        if request.method == 'POST':
            db.passengerDetails['source'] = request.form.get('source')
            db.passengerDetails['destination'] = request.form.get(
                'destination')
            db.passengerDetails['travel_date'] = request.form.get(
                'travel_date')
            return redirect("/home/trains")
        today = date.today()
        min = "%d-%.2d-%.2d" % (today.year, today.month, today.day)
        max = "%d-%.2d-%.2d" % (today.year + 1, today.month, today.day)
        return render_template("booktickets.html", stations=db.get_stations(), min_date=min, max_date=max)
    return redirect('/login')


@app.route('/home/getalltrainsinfo')
def get_all_trains_info():
    return render_template("trainsinfo.html", trainsinfo=db.get_train_details()) if session.get("user_id") else redirect("/login")


@app.route("/home/trains")
def trains():
    if session.get("user_id"):
        return render_template("trains.html", trains=db.get_trains(db.passengerDetails))
    return redirect('/login')


@app.route("/home/<int:train_no>")
def get_train_no(train_no):
    db.passengerDetails['train_no'] = train_no
    db.passengerDetails['passengers'] = []
    db.passengerDetails['user_id'] = session.get("user_id")
    return redirect("/home/addpassengers")


@app.route('/home/addpassengers', methods=['GET', 'POST'])
def addpassengers():
    if session.get("user_id"):
        if request.method == 'POST':
            name = request.form.get('p_name')
            age = int(request.form.get('p_age'))
            db.passengerDetails['passengers'].append({
                'p_name': name,
                'p_age': age
            })
        return render_template("addpassengers.html", passengers=zip(range(1, len(db.passengerDetails.get('passengers')) + 1), db.passengerDetails['passengers']), noOfpassg=len(db.passengerDetails.get('passengers')))
    return redirect("/login")


@app.route("/home/removepassenger/<int:id>")
def removepassenger(id):
    del(db.passengerDetails['passengers'][id - 1])
    return redirect("/home/addpassengers")


@app.route("/home/editpassenger/<int:id>", methods=["GET", "POST"])
def editpassenger(id):
    passenger = db.passengerDetails['passengers'][id - 1]
    if request.method == "POST":
        passenger["p_name"] = request.form.get('p_name')
        passenger["p_age"] = request.form.get('p_age')
        return redirect("/home/addpassengers")
    return render_template("editpassenger.html", passenger=passenger, id=id)


@app.route("/home/reserveticket")
def reserveticket():
    if session.get("user_id"):
        db.add_passengers_ticket(db.passengerDetails)
        return redirect("/home/viewtickets")
    return redirect("/login")


@app.route("/home/cancelticket/<int:pnr>")
def cancelticket(pnr):
    session["pnr"] = pnr
    return render_template("ticketcancelation.html", ticket=db.get_ticket(pnr))


@app.route("/home/cancelpassenger/<int:pId>")
def cancelpassenger(pId):
    return redirect(f"/home/cancelticket/{ session.get('pnr') }") if db.delete_passenger(pId, session.get("pnr")) else redirect("/home/viewtickets")


@app.route('/home/payment', methods=['GET', 'POST'])
def payment():
    if session.get("user_id"):
        if request.method == 'POST':
            return redirect('/home/reserveticket')
        return render_template("payment.html", amount=db.get_totalprice(db.passengerDetails))
    return redirect("/login")


@app.route("/signout")
def signout():
    session["user_id"] = None
    session["user_name"] = None
    return redirect('/login')


if __name__ == '__main__':
    app.run(debug=True, port=4000)
