from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# -------------------------
# App & Database Setup
# -------------------------
app = Flask(__name__)

# Use SQLite for now (creates payplan.db file in your server/ folder)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///payplan.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Database object
db = SQLAlchemy(app)

# Migration object
migrate = Migrate(app, db)

# -------------------------
# Example Model
# -------------------------
class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f"<User {self.username}>"

# -------------------------
# Simple Route
# -------------------------
@app.route("/")
def index():
    return "PayPlan Backend is running 🚀"

# -------------------------
# Run App
# -------------------------
if __name__ == "__main__":
    app.run(debug=True)
