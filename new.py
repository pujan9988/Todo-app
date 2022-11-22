from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///registrants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Details(db.Model):
    key = db.Column(db.Integer(),primary_key=True)
    name = db.Column(db.String(length=30),nullable=False)
    email = db.Column(db.String(length=50),nullable=False,unique=True)
    password = db.Column(db.String(length=20),nullable=False)
    
    def __repr__(self) -> str:
        return f"{self.email} is registered."

@app.route("/", methods = ["POST","GET"])
def login():
    if request.method == "POST":
        print("Hello world")
    else:
        return render_template("login.html")

@app.route("/registration", methods= ["POST", "GET"])
def registration():
    if request.method == "POST":
        print("Hello world")
    else: 
        return render_template("registration.html",)

@app.route("/home")
def home():
    return render_template("home.html")

if __name__ == "__main__":
    app.run(debug=True)