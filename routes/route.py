from bson import ObjectId
from fastapi import APIRouter
from mongodb import task_collection
from schemas import task_schema
from models.tasks import Task

router = APIRouter()

@router.get("/tasks")
async def tasks():
    result = task_collection.find({})
    return task_schema.tasks_response(result)

@router.post('/tasks')
async def create_task(task: Task):
    task_collection.insert_one(task.model_dump())

@router.put('/tasks/{id}')
async def update_task(id: str, task: Task):
    task_collection.update_one({'_id': ObjectId(id)}, {'$set': task.model_dump()})

@router.delete('/tasks/{id}')
async def delete_task(id: str):
    task_collection.delete_one({'_id': ObjectId(id)})
