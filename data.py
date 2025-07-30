from fastapi import HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
from db import task_collection
from pymongo.errors import DuplicateKeyError
from datetime import datetime

class Task(BaseModel):
    id: int = Field(..., example=1)
    title: str = Field(..., example="Task 1")
    description: Optional[str] = Field(None, example="Clean room")
    assignee_id: Optional[int] = Field(None, example=1)
    inProgress: bool = Field(..., example=True)
    progress: int = Field(..., example=1)
    completed: bool = Field(..., example=True)
    due_date: Optional[datetime] = None


# class TaskList(BaseModel):
#     tasks: List[Task]
#     start: int
#     limit: int
#     sort: str

def get_task(task_id: int):
    task = task_collection.find_one({"id": task_id})
    if not task:
        raise HTTPException(status_code=404, detail="Task not found.")
    task.pop("_id", None)  # Remove Mongo's ObjectId
    return Task(**task)

def retrieve_task_list():
    cursor = task_collection.find({}, {"_id": 0})
    task_list = []
    for document in cursor:
        task_list.append(document)
    if not task_list:
        raise HTTPException(status_code=404, detail="No tasks found.")
    return task_list

def insert_tasks(task_list: List[Task]):
    try:
        #result = task_collection.insert_many(task_list)
        for task in task_list:
            task_collection.insert_one(task.__dict__)
        return len(task_list)
    except DuplicateKeyError:
        raise HTTPException(status_code=400, detail="One or more task IDs already exist.")

# def update_task(task_id: int, updated_task: Task):
#     result = task_collection.update_one({"id": task_id}, {"$set": updated_task})
#     if result.matched_count == 0:
#         raise HTTPException(status_code=404, detail=f"Task with {task_id} ID was not found.")
#     return updated_task
#
# def delete_task(task_id: int):
#     result = task_collection.delete_one({"id": task_id})
#     if result.deleted_count == 0:
#         raise HTTPException(status_code=404, detail="Task not found.")
#     return {"message": "Task deleted."}