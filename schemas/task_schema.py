def task_response(task):
    return {
        "id": str(task["_id"]),
        "title": task["title"],
        "description": task["description"],
        "completed": task["completed"],
    }

def tasks_response(tasks):
    return [task_response(task) for task in tasks]