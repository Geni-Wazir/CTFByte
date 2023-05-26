from flask import Flask, redirect, render_template, url_for
from passlib.hash import pbkdf2_sha256
from flask_login import LoginManager, current_user, login_user, login_required, logout_user
from wtform_fields import *
from models import *

app = Flask(__name__)
app.secret_key = 'secret#Text'

# Configuring Database
db_user = "postgres"
db_pass = "postgres%40123"
db_host = "localhost"
db_port = "5432"
db_name = "postgres"
conn_link = "postgresql://" + db_user + ":" + db_pass + "@" + db_host + ":" + db_port + "/" + db_name

app.config['SQLALCHEMY_DATABASE_URI'] = conn_link
db.init_app(app)

# Configuring Login Manager
login = LoginManager(app)
login.init_app(app)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.route("/",methods=['GET','POST'])
def index():
    reg_form = RegistrationForm()
    if reg_form.validate_on_submit():
        username = reg_form.username.data
        password = reg_form.password.data
        hash_pw = pbkdf2_sha256.hash(password)

        with app.app_context():
            # Add User to Database
            user = User(username=username,password=hash_pw)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('login'))
    return render_template("index.html", form=reg_form)

@app.route("/login",methods=['GET','POST'])
def login():
    login_form = LoginForm()

    if login_form.validate_on_submit():
        user_object = User.query.filter_by(username=login_form.username.data).first()
        login_user(user_object)
        return redirect(url_for('chat'))

    return render_template("login.html",form=login_form)

@app.route("/chat",methods=['GET','POST'])
def chat():
    if not current_user.is_authenticated:
        return "Please Log In before trying to access the chat"

    return "Chat with Me!"

@app.route("/logout",methods=['GET'])
def logout():
    logout_user()
    return "Logged Out Successfully!!"

if __name__ == "__main__":
    app.run(debug=True)