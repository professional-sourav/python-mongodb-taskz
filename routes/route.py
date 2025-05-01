from bson import ObjectId
from fastapi import APIRouter, HTTPException
from mongodb import task_collection
from schemas import task_schema
from models.tasks import Task
from models.user import UserCreate, UserAuth, create_user, get_user_by_email
from auth import create_access_token, verify_password

router = APIRouter()

@router.post("/register")
def register(user: UserCreate):
    try:
        new_user = create_user(user)

        return {
            "message": "User created successfully.",
            "user": new_user
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login")
def login(user: UserAuth):
    db_user = get_user_by_email(user.email)

    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not verify_password(user.password, db_user.hashed_password):
        print(
            f"Invalid password for user {db_user.email}. "
            f"Expected: {user.password} "
            f"Actual: {db_user.hashed_password}"
        )
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(
        data={"sub": db_user.email}
    )

    return {"access_token": token, "token_type": "bearer"}

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
