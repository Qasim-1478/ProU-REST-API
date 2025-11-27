# ProU-REST-API

Lightweight REST API for managing employees and tasks built with FastAPI and SQLModel.

**Status:** Minimal demo API — tables are created at app startup.

**Requirements:** Python >= 3.10

**Tech Stack**
- **Web framework:** `FastAPI`
- **ORM / Models:** `SQLModel` (Pydantic + SQLAlchemy style) 
- **Database:** SQLite (file-based; created at first run)
- **Server:** `uvicorn`


**Setup & Run**

1. Set up a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install "fastapi[standard]" sqlmodel uvicorn
```

3. Start the server:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The app will create the SQLite database and tables at startup (see `app/main.py`).

**API Endpoints**

Note: See endpoints in `app/router/employees.py` and `app/router/tasks.py`.

- **Employees**
  - `POST /employees/` — Create an employee
    - Request body (example):
      ```json
      {
        "name": "Jane Doe",
        "role": "Engineer",
        "email": "jane.doe@example.com"
      }
      ```
    - Response (example):
      ```json
      {
        "id": 1,
        "name": "Jane Doe",
        "role": "Engineer",
        "email": "jane.doe@example.com"
      }
      ```

  - `GET /employees/` — List employees
    - Query params: `offset` (int, default 0), `limit` (int, default 10, max 10)
    - Response: `array` of employee objects (see example above)

  - `GET /employees/{id}` — Get single employee
    - Response: employee object or `404` if not found

  - `PATCH /employees/{id}` — Update employee (partial update)
    - Request body: partial `EmployeeUpdate` (fields optional)
    - Response: updated employee object

  - `DELETE /employees/{id}` — Delete employee
    - Response: `{ "ok": true }` on success

- **Tasks**
  - `POST /tasks/` — Create a task
    - Request body (example):
      ```json
      {
        "title": "Finish report",
        "description": "Complete the quarterly report",
        "assigned_to_id": 1,
        "status": "pending",
        "due_date": "2025-12-01"
      }
      ```
    - Response (example):
      ```json
      {
        "id": 1,
        "title": "Finish report",
        "description": "Complete the quarterly report",
        "assigned_to_id": 1,
        "status": "pending",
        "due_date": "2025-12-01"
      }
      ```

  - `GET /tasks/` — List tasks
    - Query params: `offset` (int, default 0), `limit` (int, default 10, max 10)
    - Response: `array` of task objects

  - `GET /tasks/{id}` — Get single task
    - Response: task object or `404` if not found

  - `PATCH /tasks/{id}` — Update task (partial update)
    - Request body: partial `TaskUpdate` (fields optional)
    - Response: updated task object

  - `DELETE /tasks/{id}` — Delete task
    - Response: `{ "ok": true }` on success

**Models (quick reference)**
- Models live in `app/models.py` and use `SQLModel` (Pydantic-compatible):
  - `Employee`, `EmployeeCreate`, `EmployeeUpdate`, `EmployeePublic`
  - `Task`, `TaskCreate`, `TaskUpdate`, `TaskPublic`

Refer to those files for exact field names and types. Example fields used above: `id`, `name`, `role`, `email` (employees) and `id`, `title`, `description`, `assigned_to_id`, `status`, `due_date` (tasks).

**Observed Issue & Suggested Fix**

While reviewing `app/router/tasks.py` I observed the `PATCH /tasks/{id}` handler contains likely mistakes that will raise runtime errors:

Problems seen (current code):
- `db_task = session.get(task, id)` — incorrect order/arguments; `session.get` expects a model/class and primary-key, e.g. `session.get(Task, id)`.
- `task_data = Task.model_dump(exclude_unset=True)` — calling `model_dump` on the `Task` class rather than the incoming `task` instance. Should call `task.model_dump(...)` or use the provided Pydantic methods on the `TaskUpdate` instance.



**Assumptions & Notes**
- Database: SQLite file is created automatically (no migrations included).
- The project `pyproject.toml` lists `fastapi[standard]>=0.122.0` and `sqlmodel>=0.0.27` (Python `>=3.10`).
- Some endpoints perform existence checks (e.g., creating a task validates the assigned `Employee` exists).

**Quick curl examples**
- Create employee:

```bash
curl -sS -X POST "http://127.0.0.1:8000/employees/" \
  -H "Content-Type: application/json" \
  -d '{"name":"Jane Doe","role":"Engineer","email":"jane.doe@example.com"}'
```

- Create task:

```bash
curl -sS -X POST "http://127.0.0.1:8000/tasks/" \
  -H "Content-Type: application/json" \
  -d '{"title":"Finish report","description":"Complete the quarterly report","assigned_to_id":1,"status":"pending","due_date":"2025-12-01"}'
```

# ProU-REST-API

A project created with FastAPI CLI.

## Quick Start

### Start the development server:

```bash
uv run fastapi dev
```

Visit http://localhost:8000
