from fastapi import APIRouter, Query, HTTPException, Depends, Response, status
from ..models import Employee, EmployeeCreate, EmployeeUpdate, EmployeePublic
from sqlmodel import Session, select
from ..dependencies import get_session
import logging

router = APIRouter(prefix="/employees")
logger = logging.getLogger("prou")


# 0 Create a new employee
@router.post("/", response_model=EmployeePublic, status_code=status.HTTP_201_CREATED)
def create_employee(employee: EmployeeCreate, session: Session = Depends(get_session)):
    db_employee = Employee.model_validate(employee)
    session.add(db_employee)
    session.commit()
    session.refresh(db_employee)
    logger.info("Created employee id=%s name=%s", db_employee.id, db_employee.name)
    return db_employee


# 1 Get all employees
@router.get("/", response_model=list[EmployeePublic])
def employees(
    offset: int = 0,
    limit: int = Query(default=10, le=10),
    session: Session = Depends(get_session),
):
    employees = session.exec(select(Employee).offset(offset).limit(limit)).all()
    return employees


# 2 Get a single employee
@router.get("/{id}", response_model=EmployeePublic)
def single_employee(id: int, session: Session = Depends(get_session)):
    employee = session.get(Employee, id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee


# 3 Update an employee
@router.patch("/{id}", response_model=EmployeePublic)
def update_employee(
    id: int, employee: EmployeeUpdate, session: Session = Depends(get_session)
):
    db_employee = session.get(Employee, id)
    if not db_employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    employee_data = employee.model_dump(exclude_unset=True)
    db_employee.sqlmodel_update(employee_data)
    session.add(db_employee)
    session.commit()
    session.refresh(db_employee)
    logger.info("Updated employee id=%s fields=%s", id, list(employee_data.keys()))
    return db_employee


# 4 Delete an employee
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_employee(id: int, session: Session = Depends(get_session)):
    employee = session.get(Employee, id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    session.delete(employee)
    session.commit()
    logger.info("Deleted employee id=%s", id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
