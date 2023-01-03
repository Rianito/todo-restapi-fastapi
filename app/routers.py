from fastapi import APIRouter, Request, HTTPException, status
from fastapi.responses import JSONResponse
from .schemas import task_serializer
from .models import UpdateTaskModel, CreateTaskModel
from datetime import datetime
from bson.objectid import ObjectId

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("/", response_description="Add a new task")
async def create_task(request: Request, task: CreateTaskModel):
    task = task.dict()
    task["created_at"] = datetime.utcnow()
    task["finished"] = False
    new_task = await request.app.mongodb["tasks"].insert_one(task)
    created_task = await request.app.mongodb["tasks"].find_one({"_id": new_task.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=task_serializer(created_task))


@router.get("/", response_description="List all tasks")
async def read_tasks(request: Request, skip: int):
    tasks = []
    async for task in request.app.mongodb["tasks"].find(skip=skip, limit=20):
        tasks.append(task_serializer(task))
    return tasks


@router.get("/{id}", response_description="Get a single task")
async def read_task(request: Request, id: str):
    if (task := await request.app.mongodb["tasks"].find_one({"_id": ObjectId(id)})) is not None:
        return task_serializer(task)
    raise HTTPException(status_code=404, detail=f"Task {id} not found")


@router.put("/{id}", response_description="Update a task")
async def update_task(request: Request, id: str, task: UpdateTaskModel):
    task = {k: v for k, v in task.dict().items() if v is not None}

    if len(task) >= 1:
        update_result = await request.app.mongodb["tasks"].update_one(
            {"_id": ObjectId(id)}, {"$set": task}
        )
        if update_result.modified_count == 1:
            if (
                updated_task := await request.app.mongodb["tasks"].find_one({"_id": ObjectId(id)})
            ) is not None:
                return task_serializer(updated_task)

    if (
        existing_task := await request.app.mongodb["tasks"].find_one({"_id": ObjectId(id)})
    ) is not None:
        return task_serializer(existing_task)
    raise HTTPException(status_code=404, detail=f"Task {id} not found")


@router.delete("/{id}", response_description="Delete a task")
async def delete_task(request: Request, id: str):
    delete_result = await request.app.mongodb["tasks"].delete_one({"_id": ObjectId(id)})

    if delete_result.deleted_count == 1:
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"Task {id} not found")
