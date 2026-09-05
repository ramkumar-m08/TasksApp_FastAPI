
from typing import Optional,List
from fastapi import FastAPI,HTTPExceptiom,status,Depends
from pydantic import BaseModel
from sqlalchemy import create_engine,Column,Integer,String,Boolean
from sqlalchemy.orm import DeclarativeBase,sessionmaker,Mapped,Session,mapped_column

db_url="sqlite:///./tasks.db"
engine=create_engine(db_url,connect_args={"check_same_thread":False})
Session_Local-sessionmaker(autocommit=False,autoFlush=False,bind=engine)

#SQLAlchemy 2.0 Base class
class Base(DeclarativeBase):
  pass

#SQLAlchemy Model(DB Table)
class TaskModel(Base):
  __tablename__="tasks"

  id:Mapped[int]=mapped_column(primary_key=True,index=True)
  title:Mapped[str]=mapped_column(String(50),nullable=False,unique=True)
  completed:Mapped[bool]=mapped_column(default=False)

#Auto-create SQLite DB tables on startup
Base.metadata.create_all(bind=engine)

#Pydantic for specific operations
class TaskCreate(BaseModel):
  title:str
  completed=Optional[bool]=False

class TaskUpdate(BaseModel):
  title:Optional[str]=None
  completed:Optional[bool]=None

class TaskResponse(BaseModel):
  id:int
  title:str
  completed:bool

  class Config:
    from_attributes=True

#Dependancy to manage Db Session per request
def get_db():
  db=Session_Local()
  try:
    yield db
  finally:
    db.close()

#FastAPI Setup
app=FastAPI(title="Tasks API (SQLAlchemy 2.0)")

#Endpoints
@app.post("/tasks",response_model=TaskResponse,status_code=status.HTTP_201_CREATED)
def create_task(t:TaskCreate,db:Session=Depends(get_db)):
  db_task=TaskModel(title=t.title,completed=t.completed)
  db.add(db_task)
  db.commit()
  db.refresh(db_task)
  return db_task

@app.get("/tasks",response_model=List[TaskResponse])
def get_tasks(db:Session=Depends(get_db)):
  st=select(TaskModel)
  return db.scalars(st).all()

@app.get("/tasks/{t_id}",response_model=TaskResponse)
def get_t(t_id:int,db:Session=Depends(get_db)):
  st=select(TaskModel).where(TaskModel.id==t_id)
  db_task=db.scalar(st)
  if not db_task:
    raise HTTPException(status_code=404,detail="Task not found")
  else: 
    return db_task

@app.delete("/tasks/{t_id}",status_code=status.HTTP_204_NO_CONTENT)
def del_task(t_id:int,db:Session=Depends(get_db)):
  st=select(TaskModel).where(TaskModel.id==t_id)
  db_task=db.scalar(st)
  if not db_task:
    raise HTTPException(status_code=404,detail="Task nt found")
  else:
    db.delete(db_task)
    db.commit()
    return None

@app.patch("/tasks/{t_id}",response_model=TaskResponse)
def update_task(t_id:int,t:TaskUpdate,db:Session=Depends(get_db)):
  st=select(TaskModel).where(TaskModel.id==t_id)
  db_task=db.scalar(st)
  if not db_task:
    raise HTTPException(status_code=404,detail="Task nt found")
  else:
    upd_data=task_update.model_dump(exclude_unset=True)
    if not upd_data:
      raise HTTPException(status_code=400, detail="No fields provided for update")
    for key,value in upd_data.items():
      setattr(db_task,key,value)
    db.commit()
    db.refresh(db_task)
    return db_task