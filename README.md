# task-manager-api

A RESTful API built using FastAPI, SQLAlchemy, and SQLite for task management.

## Setup

### Prerequisites

- Python 3.10+ and pip
- Docker and Docker Compose installed on your system

### Steps without Docker

1. **Clone the repository:**

   ```bash
   git clone <repository-url>
   cd task-manager-api
   ```

2. **Copy the environment file template:**

   ```bash
   cp .env.example .env
   ```

3. **Create a virtual environment and activate it:**

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

5. **Optionally seed the database:**

   ```bash
   python3 -m src.core.seed
   ```

6. **Run the application:**

   ```bash
   uvicorn src.main:app --reload
   ```

### Steps with Docker

1. **Clone the repository:**

   ```bash
   git clone <repository-url>
   cd task-manager-api
   ```

2. **Copy the environment file template:**

   ```bash
   cp .env.example .env
   ```

3. **Build and run the application with Docker Compose:**

   ```bash
   docker compose up --build
   ```

4. **Optionally seed the database:**

   If you'd like to seed the database, you can run:

   ```bash
   docker compose exec app python3 -m src.core.seed
   ```

   > **Note:** The `data` folder is mounted to the `/app` directory inside the container, ensuring that the SQLite database (`task_manager.db`) persists across container restarts.

### Access the API Documentation

Once the container or server is running, you can access the API docs in your browser:

- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
- ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

## API Endpoints

### CRUD Operations Endpoints

| Method   | Endpoint           | Description                              |
| -------- | ------------------ | ---------------------------------------- |
| `POST`   | `/tasks/`          | Create a new task                        |
| `GET`    | `/tasks/`          | Retrieve all tasks with optional filters |
| `GET`    | `/tasks/{task_id}` | Retrieve details of a specific task      |
| `PUT`    | `/tasks/{task_id}` | Update an existing task                  |
| `DELETE` | `/tasks/{task_id}` | Delete a task                            |

### Smart Task Suggestions Endpoint

| Method | Endpoint                | Description                               |
| ------ | ----------------------- | ----------------------------------------- |
| `GET`  | `/tasks/suggestions`    | Retrieve smart suggestions based on regex |
| `GET`  | `/tasks/suggestions-ai` | Retrieve smart suggestions based on AI    |

## Example Requests & Responses

### `POST` /tasks/ - Create a new task

**Request Body:**

```json
{
  "title": "Project A Review",
  "description": "Review Project A",
  "due_date": "2025-03-10",
  "status": "pending"
}
```

**Response Body:**

```json
{
  "title": "Project A Review",
  "description": "Review Project A",
  "due_date": "2025-03-10",
  "status": "pending",
  "id": 7,
  "creation_date": "2025-03-10"
}
```

### `GET` /tasks/ - Retrieve all tasks with optional filters

**Request URL:** `http://localhost:8000/tasks/?status=pending&due_date=2025-03-10`

**Response Body:**

```json
{
  "title": "Project A Review",
  "description": "Review Project A",
  "due_date": "2025-03-10",
  "status": "pending",
  "id": 7,
  "creation_date": "2025-03-10"
}
```

### `GET` /tasks/{task_id} - Retrieve details of a specific task

**Request URL:** `http://localhost:8000/tasks/7`

**Response Body:**

```json
{
  "title": "Project A Review",
  "description": "Review Project A",
  "due_date": "2025-03-10",
  "status": "pending",
  "id": 7,
  "creation_date": "2025-03-10"
}
```

### `PUT` /tasks/{task_id} - Update an existing task

**Request URL:** `http://localhost:8000/tasks/7`

**Request Body:**

```json
{
  "status": "completed"
}
```

**Response Body:**

```json
{
  "title": "Project A Review",
  "description": "Review Project A",
  "due_date": "2025-03-10",
  "status": "completed",
  "id": 7,
  "creation_date": "2025-03-10"
}
```

### `DELETE` /tasks/{task_id} - Delete a Task

**Request URL:** `http://localhost:8000/tasks/7`

**Response Body:**

```json
"Task with id 7 deleted successfully"
```

### `GET` /tasks/suggestions - Retrieve smart suggestions based on regex

**Response Body:**

```json
[
  "Project Beta Finalization",
  "Project Gamma Follow-up Meeting",
  "Project A Follow-up Meeting"
]
```

### `GET` /tasks/suggestions-ai - Retrieve smart suggestions based on AI

**Response Body:**

```json
[
  "Project Alpha Preview",
  "Project Alpha Follow",
  "Project Alpha Test",
  "Project Beta Preview"
]
```

## Smart Task Suggestions

Multiple viable techniques could've been used such as TF-IDF, SentenceTransformers, Clustering, Markov chains, etc.

This API uses a Regex-based and an AI-based approach.

Regex-based approach:

- The code looks for patterns of the form "Project X Review", "Project X Follow-up Meeting", and "Project X Finalization".
- Identifies the "stages" each project has. If a stage is missing (e.g., no follow-up meeting yet after a review), it suggests that stage.
- Rudimentary pattern-based system. For more generic or flexible tasks, the regex won’t catch them.

AI-based approach:

- Uses distilgpt2 to generate text based on recent “completed” tasks. The prompt is constructed by listing known tasks, then asking the model for a “Related new task.”
- The result is then parsed to remove extraneous lines or duplication.
- Uses Hugging Face Transformers for text generation.
- Extracts up to 10 recently completed tasks (some notion of recency).
- The logic filters out short or duplicate suggestions.

## [License](./LICENSE)
