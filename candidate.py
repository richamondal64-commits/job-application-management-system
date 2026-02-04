def candidate_schema(candidate):
    return {
        "id": str(candidate["_id"]),
        "name": candidate["name"],
        "email": candidate["email"],
        "resumeLink": candidate["resumeLink"]
    }
