from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)

# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = (
    "mysql+mysqldb://root:Chan%40quadwave@localhost/blogPost"
)

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
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


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

    return render_template("contact.html")


@app.route("/post")
def post():
    return render_template("post.html")


if __name__ == "__main__":
    app.run(debug=True)
