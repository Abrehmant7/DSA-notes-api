# DSA Pattern Notes API

This is a simple FastAPI project for saving DSA notes. Notes can be grouped by category, and users must log in before they can use the main API routes.

The project uses:

- FastAPI for the API
- SQLAlchemy for database models
- SQLite as the default local database
- JWT tokens for authentication
- Pydantic for request and response validation

## Project Structure

```text
app/
|-- main.py              # Starts the FastAPI app
|-- core/                # Config, database, security
|-- models/              # SQLAlchemy database tables
|-- schemas/             # Pydantic request/response schemas
|-- routers/             # API endpoints
|-- services/            # Business logic
|-- repositories/        # Database queries
`-- dependencies/        # FastAPI dependencies
```

## Setup

Create a virtual environment:

```powershell
python -m venv .venv
```

Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

Create your local `.env` file:

```powershell
Copy-Item .env.example .env
```

Example `.env` values:

```env
DATABASE_URL=sqlite:///./dsa_notes.db
JWT_SECRET_KEY=replace-this-with-a-long-random-secret-key
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
```

The `.env` file is ignored by Git because it can contain private settings.

## Run the App

```powershell
uvicorn app.main:app --reload
```

Open the API docs in your browser:

```text
http://127.0.0.1:8000/docs
```

FastAPI docs are the easiest way to test the project.

## Authentication Flow

1. Register a user with `POST /auth/register`.
2. Log in with `POST /auth/login`.
3. Copy the returned `access_token`.
4. Click the **Authorize** button in `/docs`.
5. Enter the token like this:

```text
Bearer your_token_here
```

After this, you can use the protected routes.

## API Routes

### Public Routes

| Method | Route | Purpose |
| --- | --- | --- |
| `GET` | `/` | Check if the API is running |
| `POST` | `/auth/register` | Create a new user |
| `POST` | `/auth/login` | Log in and get a JWT token |

### Protected Routes

These routes need a JWT token.

| Method | Route | Purpose |
| --- | --- | --- |
| `GET` | `/auth/me` | Get the logged-in user |
| `POST` | `/categories/` | Create a category |
| `GET` | `/categories/` | List categories |
| `POST` | `/notes/` | Create a note |
| `GET` | `/notes/` | List notes |
| `GET` | `/notes/{note_id}` | Get one note |
| `PUT` | `/notes/{note_id}` | Update a note |
| `DELETE` | `/notes/{note_id}` | Delete a note |

## Example Requests

Register:

```json
{
  "email": "student@example.com",
  "password": "strongpassword123"
}
```

Create a category:

```json
{
  "name": "Sliding Window"
}
```

Create a note:

```json
{
  "question": "Longest Substring Without Repeating Characters",
  "signal": "Contiguous substring with uniqueness constraint",
  "brute_force": "Check every substring",
  "useful_memory": "Move the left pointer when a duplicate appears",
  "pattern": "Sliding Window",
  "key_question": "Can a moving window maintain the condition?",
  "solution_approach": "Use two pointers and track seen characters.",
  "time_complexity": "O(n)",
  "space_complexity": "O(k)",
  "category_id": 1
}
```

## Database Note

The SQLite database file `dsa_notes.db` is created locally when the app runs. It should not be committed to Git.

If you delete the database file, the app will create a fresh one the next time it starts.
