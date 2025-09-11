from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from datetime import datetime
import json

with open("config.json", "r") as c:
    params = json.load(c)["params"]

local_server = params["local_server"]

app = Flask(__name__)
app.config.update(
    MAIL_SERVER="smtp.gmail.com",
    MAIL_PORT="465",
    MAIL_USE_SSL=True,
    MAIL_USERNAME=params["gmail_user"],
    MAIL_PASSWORD=params["gmail_password"],
)

mail = Mail(app)

if local_server:
    app.config["SQLALCHEMY_DATABASE_URI"] = params["local_uri"]
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = params["prod_uri"]


db = SQLAlchemy(app)


class Contacts(db.Model):
    __tablename__ = "contacts"

    sno = db.Column(db.Integer, primary_key=True, autoincrement=True)  # ✅
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(45), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    message = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)


@app.route("/")
def home():
    return render_template("index.html", params=params)


@app.route("/about")
def about():
    return render_template("about.html", params=params)


@app.route("/contact", methods=["POST", "GET"])
def contact():
    if request.method == "POST":
        # add entry to the database
        name = request.form.get("name")
        email = request.form.get("email")
        phone_number = request.form.get("phone")
        message = request.form.get("message")
        date = request.form.get("date")

        entry = Contacts(
            name=name,
            phone_number=phone_number,
            message=message,
            email=email,
            date=date,
        )
        db.session.add(entry)
        db.session.commit()
        mail.send_message(
            "New message from " + name,
            sender=email,
            recipients=[params["gmail_user"]],
            body=message + "\n" + phone_number,
        )

    return render_template("contact.html", params=params)


@app.route("/post")
def post():
    return render_template("post.html", params=params)


if __name__ == "__main__":
    app.run(debug=True)
