from sqlmodel import SQLModel, Field, create_engine
from pydantic import EmailStr


class EmployeeBase(SQLModel):
    name: str
    role: str
    email: EmailStr


class EmployeeCreate(EmployeeBase):
    pass


class EmployeePublic(EmployeeBase):
    id: int


class EmployeeUpdate(SQLModel):
    name: str | None = None
    role: str | None = None
    email: EmailStr | None = None


class Employee(EmployeeBase, table=True):
    id: int = Field(default=None, primary_key=True)


class TaskBase(SQLModel):
    title: str
    description: str
    assigned_to_id: int = Field(foreign_key="employee.id")
    status: str  # e.g., "pending", "in_progress", "completed"
    due_date: str  # ISO format date string


class TaskCreate(TaskBase):
    pass


class TaskPublic(TaskBase):
    id: int


class TaskUpdate(SQLModel):
    title: str | None = None
    description: str | None = None
    assigned_to_id: int | None = None
    status: str | None = None
    due_date: str | None = None


class Task(TaskBase, table=True):
    id: int = Field(default=None, primary_key=True)


sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
