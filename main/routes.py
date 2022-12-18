from main import app,request,render_template,db,bcrypt,redirect,flash,url_for
from main.dbmodels import Details,Todo
from main.forms import RegistrationForm,LoginForm,TodoForm
from flask_login import login_user,current_user,logout_user,login_required

@app.route("/", methods = ["POST","GET"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = LoginForm()
    if (request.method == "POST" and form.validate_on_submit()):
        user = Details.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for("home"))
        else:
            flash("Invalid credentials ! Try again.","danger")
    return render_template("login.html",form=form)


@app.route("/registration", methods= ["POST", "GET"])
def registration():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = RegistrationForm()
    if (request.method == "POST") and (form.validate_on_submit()):
        name = form.name.data
        email = form.email.data
        password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = Details(name = name, email= email, password = password)
        db.session.add(user)
        db.session.commit()
        flash("You are successfully registered !",'success')
    return render_template("registration.html",form=form)

@app.route("/home", methods= ["POST", "GET"])
@login_required
def home():
    form = TodoForm()
    user = Details.query.filter_by(email=current_user.email).first() 
    todos = Todo.query.all()
    if (form.validate_on_submit()) and (request.method=="POST"):
        todo = Todo(title=form.title.data, description = form.description.data, details_id=current_user.id)
        db.session.add(todo)
        db.session.commit()
        user = Details.query.filter_by(email=current_user.email).first()
        todos = Todo.query.all()
        return render_template('home.html',todos=todos,form=form,user=user)
    return render_template("home.html",form=form,todos=todos,user=user)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("login"))


@app.route("/account")
def account():
    return render_template("account.html")
