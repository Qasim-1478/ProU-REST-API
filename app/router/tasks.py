from fastapi import APIRouter, Query, HTTPException, Depends, Response, status
from ..models import Task, TaskCreate, TaskUpdate, TaskPublic, Employee
from sqlmodel import Session, select
from ..dependencies import get_session
import logging

router = APIRouter(prefix="/tasks")
logger = logging.getLogger("prou")


# 0 Create a new task
@router.post("/", response_model=TaskPublic, status_code=status.HTTP_201_CREATED)
def create_task(task: TaskCreate, session: Session = Depends(get_session)):
    db_task = Task.model_validate(task)
    emp_id = db_task.assigned_to_id
    db_employee = session.get(Employee, emp_id)
    if not db_employee:
        logger.warning("Attempt to create task assigned to missing employee id=%s", emp_id)
        raise HTTPException(status_code=404, detail="Employee not found")
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    logger.info("Created task id=%s title=%s assigned_to=%s", db_task.id, db_task.title, emp_id)
    return db_task


# 1 Get all tasks
@router.get("/", response_model=list[TaskPublic])
def tasks(
    offset: int = 0,
    limit: int = Query(default=10, le=10),
    session: Session = Depends(get_session),
):
    tasks = session.exec(select(Task).offset(offset).limit(limit)).all()
    return tasks


# 2 Get a single task
@router.get("/{id}", response_model=TaskPublic)
def single_task(id: int, session: Session = Depends(get_session)):
    db_task = session.get(Task, id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task


# 3 Update an task
@router.patch("/{id}", response_model=TaskPublic)
def update_task(id: int, task: TaskUpdate, session: Session = Depends(get_session)):
    db_task = session.get(task, id)
    if not db_task:
        logger.warning("Task update failed: not found id=%s", id)
        raise HTTPException(status_code=404, detail="Task not found")
    task_data = Task.model_dump(exclude_unset=True)
    emp_id = db_task.assigned_to_id
    if emp_id is not None:
        db_employee = session.get(Employee, emp_id)
        if not db_employee:
            logger.warning("Task update failed: assigned employee not found id=%s", emp_id)
            raise HTTPException(status_code=404, detail="Employee not found")
    db_task.sqlmodel_update(task_data)
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    logger.info("Updated task id=%s fields=%s", id, list(task_data.keys()))
    return db_task


# 4 Delete an task
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(id: int, session: Session = Depends(get_session)):
    db_task = session.get(Task, id)
    if not db_task:
        logger.warning("Attempt to delete missing task id=%s", id)
        raise HTTPException(status_code=404, detail="Task not found")
    session.delete(db_task)
    session.commit()
    logger.info("Deleted task id=%s", id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
