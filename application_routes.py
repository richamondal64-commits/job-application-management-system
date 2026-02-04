from flask import Blueprint, request, jsonify
from bson.objectid import ObjectId
from datetime import datetime

application_bp = Blueprint("applications", __name__)
mongo = None

@application_bp.route("/<job_id>/apply", methods=["POST"])
def apply_job(job_id):
    data = request.json

    if not data.get("name") or not data.get("email") or not data.get("resumeLink"):
        return jsonify({"message": "All fields required"}), 400

    job = mongo.db.jobs.find_one({"_id": ObjectId(job_id), "isActive": True})
    if not job:
        return jsonify({"message": "Job not available"}), 404

    candidate = mongo.db.candidates.find_one({"email": data["email"]})
    if not candidate:
        candidate_id = mongo.db.candidates.insert_one({
            "name": data["name"],
            "email": data["email"],
            "resumeLink": data["resumeLink"]
        }).inserted_id
    else:
        candidate_id = candidate["_id"]

    existing = mongo.db.applications.find_one({
        "jobId": ObjectId(job_id),
        "candidateId": candidate_id
    })

    if existing:
        return jsonify({"message": "Already applied"}), 409

    app_id = mongo.db.applications.insert_one({
        "jobId": ObjectId(job_id),
        "candidateId": candidate_id,
        "status": "APPLIED",
        "appliedAt": datetime.utcnow()
    }).inserted_id

    return jsonify({"applicationId": str(app_id), "status": "APPLIED"}), 201


@application_bp.route("/<app_id>", methods=["GET"])
def get_status(app_id):
    app = mongo.db.applications.find_one({"_id": ObjectId(app_id)})
    if not app:
        return jsonify({"message": "Not found"}), 404

    return jsonify({
        "applicationId": str(app["_id"]),
        "status": app["status"]
    }), 200


@application_bp.route("/<app_id>/status", methods=["PUT"])
def update_status(app_id):
    data = request.json
    new_status = data.get("status")

    app = mongo.db.applications.find_one({"_id": ObjectId(app_id)})
    if not app:
        return jsonify({"message": "Not found"}), 404

    valid_flow = {
        "APPLIED": ["SHORTLISTED", "REJECTED"],
        "SHORTLISTED": ["SELECTED", "REJECTED"]
    }

    current = app["status"]
    if current not in valid_flow or new_status not in valid_flow[current]:
        return jsonify({"message": "Invalid status transition"}), 400

    mongo.db.applications.update_one(
        {"_id": ObjectId(app_id)},
        {"$set": {"status": new_status}}
    )

    return jsonify({"message": "Status updated", "newStatus": new_status}), 200
