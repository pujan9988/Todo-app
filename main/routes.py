from main import app,request,render_template,db,bcrypt,redirect,flash,url_for,mail
from main.dbmodels import Details,Todo
from main.forms import RegistrationForm,LoginForm,TodoForm,ResetRequestForm,ResetPassword
from flask_login import login_user,current_user,logout_user,login_required
from flask_mail import Message

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
    user = Details.query.filter_by(email=current_user.email).first() 
    todos = Todo.query.all()
    return render_template("home.html",todos=todos,user=user)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("login"))


@app.route("/account")
def account():
    return render_template("account.html")

@app.route("/home/todo/<int:todo_id>",methods=["POST","GET"])
@login_required
def todo(todo_id):
    form = TodoForm()
    todo = Todo.query.get_or_404(todo_id)
    if(form.validate_on_submit() and request.method=="POST"):
        todo.title = form.title.data
        todo.description = form.description.data
        db.session.commit()
        return redirect(url_for("home"))
    form.title.data =  todo.title
    form.description.data = todo.description
    return render_template("todo.html",todo=todo,form=form)

@app.route("/home/addtodo", methods= ["POST", "GET"])
@login_required
def addtodo():
    form = TodoForm()
    if (form.validate_on_submit()) and (request.method=="POST"):
        todo = Todo(title=form.title.data, description = form.description.data,author=current_user) 
        db.session.add(todo)
        db.session.commit()
        user = Details.query.filter_by(email=current_user.email).first()
        todos = Todo.query.all()
        return render_template('home.html',todos=todos,user=user)
    return render_template("addtodo.html",form=form)

@app.route("/home/deletetodo/<int:todo_id>",methods=["POST","GET"])
@login_required
def delete_todo(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("home"))

def send_reset_email(user):
    #get the token from the method of details class
    token = user.get_reset_token()
    #the first parameter is the subject,
    msg = Message("PASSWORD RESET REQUEST", sender="noreply@gmail.com",recipients=[user.email])
    msg.body = f'''To reset your password; visit the following link:
    {url_for("reset_token", token=token, _external=True)}

    If you did not make this then simple ignore this email and no changes will be made
    '''
    mail.send(msg)

@app.route("/reset_request",methods=["GET","POST"])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = ResetRequestForm()
    if form.validate_on_submit():
        user = Details.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash("An email has been sent with instructions to reset your password","info")
        return redirect(url_for("login"))
    return render_template("reset_request.html",form= form)
    
@app.route("/reset_password/<token>",methods=["GET","POST"])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = Details.verify_reset_token(token)
    if user is None:
        flash("That is invalid or expired token!","warning")
        return redirect(url_for("reset_request"))
    form = ResetPassword()
    if (request.method == "POST") and (form.validate_on_submit()):
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash("Your password has been updated. Now you can login with your new password")
        return redirect(url_for("login"))
    return render_template("reset_token.html",form=form)

