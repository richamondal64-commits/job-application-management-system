from flask import Flask
from flask_pymongo import PyMongo
from routes import job_bp
from application_routes import application_bp
from config import MONGO_URI

app = Flask(__name__)
app.config["MONGO_URI"] = MONGO_URI

mongo = PyMongo(app)

# make mongo accessible in routes
import routes
import application_routes

routes.mongo = mongo
application_routes.mongo = mongo

app.register_blueprint(job_bp, url_prefix="/jobs")
app.register_blueprint(application_bp, url_prefix="/applications")

if __name__ == "__main__":
    app.run(debug=True)
