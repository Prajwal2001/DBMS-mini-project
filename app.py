from flask import Flask, render_template, redirect, request
from database import Database
from json import dumps

app = Flask(__name__)
db = Database()
isAuthorized = False
user: int


@app.route('/')
def redirect_pg():
    return redirect('/login', code=302)


@app.route('/login', methods=['GET', 'POST'])
def login():
    global isAuthorized, user
    if request.method == 'POST':
        if db.does_user_exist([request.form.get('username'), request.form.get('password')]):
            isAuthorized = True
            user = db.get_user_id_by_user_name(request.form.get('username'))
            return redirect('/home', code=302)
        else:
            isAuthorized = False
            return render_template("index.html", status=False)
    else:
        isAuthorized = False
        return render_template("index.html", status=True)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    global isAuthorized, user
    if request.method == 'POST':
        response = db.add_user([request.form.get('username'),
                                request.form.get('email'),
                                request.form.get('password')])
        user = db.get_user_id_by_user_name(request.form.get('username'))
        return redirect('/home', code=302) if response else render_template("signup.html", status=response)
    else:
        isAuthorized = False
        return render_template("signup.html", status=True)


@app.route("/home")
def home():
    global isAuthorized, user
    if isAuthorized:
        return render_template("home.html", user=user)
    else:
        return redirect('/login', code=302)


@app.route("/home/<int:user_id>/viewtickets")
def viewtickets(user_id):
    global user
    return render_template("tickets.html", tickets=db.get_ticket(user_id), user=user)


if __name__ == '__main__':
    app.run(debug=True, port=4000)
