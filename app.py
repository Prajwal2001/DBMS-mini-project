from flask import Flask, render_template, redirect, request
from database import Database
from json import dumps

app = Flask(__name__)
db = Database()
isAuthorized = False


@app.route('/')
def redirect_pg():
    return redirect('/login', code=302)


@app.route('/login', methods=['GET', 'POST'])
def login():
    global isAuthorized
    if request.method == 'POST':
        if db.does_user_exist([request.form.get('username'), request.form.get('password')]):
            isAuthorized = True
            return redirect('/home', code=302)
        else:
            isAuthorized = False
            return render_template("index.html", status=False)
    else:
        return render_template("index.html", status=True)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        response = db.add_user([request.form.get('username'), request.form.get(
            'email'), request.form.get('password')])
        return redirect('/home', code=302) if response else render_template("signup.html", status=response)
    else:
        return render_template("signup.html", status=True)


@app.route("/home")
def home():
    global isAuthorized
    if isAuthorized:
        isAuthorized = False
        return render_template("home.html")
    else:
        return redirect('/login', code=302)


if __name__ == '__main__':
    app.run(debug=True, port=4000)
