from flask import Flask, render_template
from wtform_fields import *
from flask_sqlalchemy import SQLAlchemy
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

@app.route("/",methods=['GET','POST'])
def index():
    reg_form = RegistrationForm()
    if reg_form.validate_on_submit():
        username = reg_form.username.data
        password = reg_form.password.data

        with app.app_context():
            # Check if User already exists
            user_object = User.query.filter_by(username=username).first()
            if user_object:
                return "This Username is already taken by another User"
            
            # Add User to Database
            user = User(username=username,password=password)
            db.session.add(user)
            db.session.commit()
            return "Inserted into Database"
    return render_template("index.html", form=reg_form)

if __name__ == "__main__":
    app.run(debug=True)