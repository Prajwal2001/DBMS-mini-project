from flask import Flask, render_template, redirect, request, session
from database import Database
from json import dumps

app = Flask(__name__)
app.secret_key = "abc"

db = Database()
isAuthorized = False


@app.route('/')
def redirect_pg():
    return redirect('/login', code=302)


@app.route('/login', methods=['GET', 'POST'])
def login():
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
        print(request.form.get('username'))
        response = db.add_user([request.form.get('username'),
                                request.form.get('email'),
                                request.form.get('password')])
        return redirect('/home', code=302) if response else render_template("signup.html", status=response)
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
        return render_template("tickets.html", tickets=db.get_ticket(session['user_id']))
    else:
        return redirect('/login')


@app.route("/signout")
def signout():
    session['user_id'] = None
    return redirect('/login')


if __name__ == '__main__':
    app.run(debug=True, port=4000)
