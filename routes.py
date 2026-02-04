from flask import Blueprint, jsonify

job_bp = Blueprint("jobs", __name__)
mongo = None

@job_bp.route("/", methods=["GET"])
def get_active_jobs():
    jobs = mongo.db.jobs.find({"isActive": True})
    result = []
    for job in jobs:
        result.append({
            "id": str(job["_id"]),
            "title": job["title"],
            "description": job["description"],
            "location": job["location"],
            "isActive": job["isActive"]
        })
    return jsonify(result), 200
