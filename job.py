def job_schema(job):
    return {
        "id": str(job["_id"]),
        "title": job["title"],
        "description": job["description"],
        "location": job["location"],
        "isActive": job["isActive"]
    }
