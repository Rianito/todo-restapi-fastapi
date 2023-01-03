def task_serializer(task) -> dict:
    return {
        "id": str(task["_id"]),
        "title": task["title"],
        "description": task["description"],
        "created_at": task["created_at"].isoformat(),
        "finished": task["finished"]
    }
