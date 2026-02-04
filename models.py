def application_schema(app):
    return {
        "id": str(app["_id"]),
        "jobId": str(app["jobId"]),
        "candidateId": str(app["candidateId"]),
        "status": app["status"],
        "appliedAt": app["appliedAt"]
    }
