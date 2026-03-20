# KanMind Backend API

A RESTful API for a Kanban-style project management application, built with Django and Django REST Framework.

---

## Tech Stack

- **Python** 3.14
- **Django** 6.x
- **Django REST Framework**
- **SQLite** (development)
- **Token Authentication**

---

## Features

- User registration and login with token-based authentication
- Board management (create, read, update, delete)
- Task management with status and priority tracking
- Comment system per task
- Permission-based access control

---

## Project Structure

```
Backend_kanmind/
├── core/               # Project settings, main URLs, wsgi
├── users_app/          # User registration, login, authentication
│   └── api/            # Serializers, views, urls
├── boards_app/         # Board CRUD
│   └── api/
├── tasks_app/          # Tasks and comments
│   └── api/
├── manage.py
├── requirements.txt
└── README.md
```

---

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/your-username/kanmind-backend.git
cd kanmind-backend
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv

# Windows:
.venv\Scripts\activate

# macOS/Linux:
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

Create a `.env` file in the root directory:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
```

### 5. Run migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create a superuser (optional)

```bash
python manage.py createsuperuser
```

### 7. Start the development server

```bash
python manage.py runserver
```

The API will be available at `http://127.0.0.1:8000/`.

---

## API Endpoints

### Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/registration/` | Register a new user |
| POST | `/api/login/` | Login and receive token |

### Boards

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/boards/` | List all boards for the authenticated user |
| POST | `/api/boards/` | Create a new board |
| GET | `/api/boards/{board_id}/` | Retrieve a board |
| PATCH | `/api/boards/{board_id}/` | Update a board |
| DELETE | `/api/boards/{board_id}/` | Delete a board |

### Tasks

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/tasks/assigned-to-me/` | List tasks assigned to the current user |
| GET | `/api/tasks/reviewing/` | List tasks where the current user is reviewer |
| POST | `/api/tasks/` | Create a new task |
| PATCH | `/api/tasks/{task_id}/` | Update a task |
| DELETE | `/api/tasks/{task_id}/` | Delete a task |

### Comments

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/tasks/{task_id}/comments/` | List all comments for a task |
| POST | `/api/tasks/{task_id}/comments/` | Add a comment to a task |
| DELETE | `/api/tasks/{task_id}/comments/{comment_id}/` | Delete a comment |

---

## Authentication

All endpoints (except registration and login) require a token in the request header:

```
Authorization: Token <your-token>
```

---

## Environment Variables

| Variable | Description |
|----------|-------------|
| `SECRET_KEY` | Django secret key |
| `DEBUG` | Debug mode (`True` or `False`) |

---

## Notes

- The SQLite database file (`db.sqlite3`) is excluded from version control.
- The `.env` file is excluded from version control. Never commit sensitive credentials.
- Admin panel is available at `/admin/`.
