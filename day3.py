#Importing fastapi,pydantic(specifying datatypes),optional
from fastapi import FastAPI , HTTPException
from pydantic import BaseModel
from typing import Optional

#Creating a Fastapi with a title
app=FastAPI(title="In mem tasks API")

#In memory Database
tasks_db=[{"id":1,"title":"Study HTTP basics","completed":True},{"id":2,"title":"Build FastAPI In mem app","completed":False}]

#Pydantic-Data shapes for incoming requests(POST/PUT)
class TaskCreate(BaseModel):
  title:str
  completed: Optional[bool]=False

#GET All tasks(200 OK)
@app.get("/tasks",status_code=200)
def get_tasks():
  return {"data":tasks_db}

#GET a specific task(200 OK or 404 NOT FOUND)
@app.get("/tasks/{task_id}",status_code=200)
def get_task(task_id:int):
  for task in tasks_db:
    if task["id"]==task_id:
      return task
  raise HTTPException(status_code=404,detail="Task not found")

#Add/Create a new task (POST Endpoint)
@app.post("/tasks",status_code=201)

#Parameter data input in Pydantic form
def create_task(task_data:TaskCreate):
  if tasks_db: new_id=tasks_db[-1]["id"]+1
  else: new_id=1
  new_task={"id":new_id,"title":task_data.title,"completed":task_data.completed}
  tasks_db.append(new_task)
  return new_task

#Update a task (PUT Endpoint)
@app.put("/tasks/{task_id}",status_code=200)
def upd_task(task_id:int,task_data:TaskCreate):
  for i,task in enumerate(tasks_db):
    if(task["id"]==task_id):
      upd_task={"id":task_id,"title":task_data.title,"completed":task_data.completed}
      tasks_db[i]=upd_task
      return upd_task
  raise HTTPException(status_code=404,detail="Task not found")


#Delete a task
@app.delete("/tasks/{task_id}",status_code=200)
def del_task(task_id:int):
  for task in tasks_db:
    if(task["id"]==task_id):
      tasks_db.remove(task)
      return {"message" :f"Task {task_id} deleted successfully"}

  raise HTTPException(status_code=404,detail="Task not found")
  