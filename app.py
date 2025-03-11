from flask import Flask, render_template, request, redirect, url_for, session
from dotenv import load_dotenv
import mysql.connector
import os


# Load environment variables
load_dotenv()

# Get username & password from .env file
VALID_USERNAME = os.getenv("USERNAME")
VALID_PASSWORD = os.getenv("PASSWORD")

app = Flask(__name__)

app.secret_key = "your_secret_key"  # Required for session management
db = mysql.connector.connect(
    host="srilakshmim.mysql.pythonanywhere-services.com",
    user="srilakshmim",
    password="Pass@123",
    database="srilakshmim$salon"
)
cursor = db.cursor()
# Home Route
@app.route("/")
def home():
    return render_template("index.html")

# About Route
@app.route("/about")
def about():
    return render_template("about.html")

# Contact Route
@app.route("/contact")
def contact():
    return render_template("contact.html")

# Portfolio Route
@app.route("/portfolio")
def portfolio():
    return render_template("portfolio.html")

# Services Route
@app.route("/services")
def services():
    cursor = db.cursor(dictionary=True)  # Fetch results as dictionary
    cursor.execute("SELECT name, Image, price FROM Service WHERE isactive = 1")
    services = cursor.fetchall()
    cursor.close()

    return render_template("services.html", services=services)

# ✅ New Login Route
@app.route("/login", methods=["GET", "POST"])
def login():
    print(f"Request method: {request.method}") 
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username == VALID_USERNAME and password == VALID_PASSWORD:
            session["user"] = username  # Store session
            return redirect(url_for("dashboard"))  # Redirect to dashboard
        else:
            return render_template("login.html", error="Invalid Credentials")

    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    if "user" in session:
        return render_template("dashboard.html", username=session["user"])
    else:
        return redirect(url_for("login"))


@app.route("/add_service", methods=["GET", "POST"])
def add_service():
    if request.method == "POST":
        name = request.form["name"]
        price = request.form["price"]
        isactive = int(request.form["isactive"])

        # Handling image upload
        image = request.files["image"]
        if image:
            image_path = os.path.join("static/uploads", image.filename)
            image.save(image_path)
        else:
            image_path = None

        # Insert into database
        query = "INSERT INTO Service (name, Image, price, isactive) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (name, image_path, price, isactive))
        db.commit()

        return redirect(url_for("add_service"))

    return render_template("dashboard.html")


if __name__ == "__main__":
    app.run(debug=True)
