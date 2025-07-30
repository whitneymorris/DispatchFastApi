from contextlib import asynccontextmanager
from fastapi import FastAPI, Header, HTTPException, status, Depends
from auth_config import API_KEY
from db import client, task_collection
from typing import List
from data import Task, get_task, retrieve_task_list, insert_tasks#, update_task, delete_task


# This will run on startup
@asynccontextmanager
async def lifespan(app: FastAPI):

    # Create unique index on 'id' field
    task_collection.create_index("id", unique=True)

    yield  # Run the app

    # This will run on shutdown
    client.close()

def verify_api_key(x_auth_token: str = Header(...)):
    if x_auth_token != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API key",
        )

app = FastAPI(title="Dispatch Task API", version="1.0", lifespan=lifespan, dependencies=[Depends(verify_api_key)])

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/tasks/{task_id}", summary="Retrieve a single task")
async def get_task_by_id(task_id: int):
    return get_task(task_id)


@app.get("/tasks", summary="Retrieve all tasks")
async def get_all_tasks():
    task_list = retrieve_task_list()
    return task_list

@app.post("/tasks", summary="Insert multiple tasks")
async def post_tasks(task_list: List[Task]):
    count = insert_tasks(task_list)
    return {"message": f"{count} tasks inserted."}

# @app.put("/tasks/{task_id}", summary="Update a single task")
# def update_single_task(task_id: int, task: Task):
#     update_task(task_id, task)
#     return {"message": f"Task {task_id} updated."}
#
# @app.delete("/tasks/{task_id}", summary="Delete a single task")
# async def delete_task(task_id: int):
#     return delete_task(task_id)