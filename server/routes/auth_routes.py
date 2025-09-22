#!/usr/bin/env python3

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

# Local imports
from config import app, db
from routes.auth_routes import auth_bp  # auth blueprint

# Database & migration setup
migrate = Migrate(app, db)

# JWT setup
app.config["JWT_SECRET_KEY"] = "super-secret-key"
jwt = JWTManager(app)

# Register blueprints
app.register_blueprint(auth_bp)

# Root route
@app.route("/")
def index():
    return "<h1>Project Server Running...</h1>"

# Run app
if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # optional; Flask-Migrate handles migrations
    app.run(port=5555, debug=True)

