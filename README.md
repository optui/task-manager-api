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

A variety of techniques could be employed to generate task suggestions, including TF-IDF, SentenceTransformers, Clustering, Markov chains, and more. Within this project, we have focused on **two** primary methods:

1. **A Regex-based approach**
2. **An AI-driven approach**

### 1. Regex-based Approach

- **Pattern Recognition**  
  The system looks for task titles of the form:  

  ```text
  Project <ProjectName> Review
  Project <ProjectName> Follow-up Meeting
  Project <ProjectName> Finalization
  ```

- **Sequential Stage Detection**  
  Each "Project ProjectName" can have up to three primary "stages" (review, follow-up, finalization). If the system detects an earlier stage without its subsequent stage—for instance, a review is completed but there is no follow-up meeting scheduled—it will suggest adding that missing stage.

### 2. AI-based Approach

- **Model and Prompt Construction**  
  The AI-based suggestion engine uses the **distilgpt2** model from Hugging Face. The prompt includes up to 10 recent "completed" tasks, followed by a request such as:  

  ```text
  Existing tasks:
  <list of tasks>

  Related new task:
  ```

- **Generating and Filtering Outputs**  
  The model creates text based on the prompt. We then parse and clean the generated output to remove irrelevant content, repeated lines, or extremely short suggestions. Any duplicates of existing tasks are also discarded.  

### Why Two Approaches?

- The **regex-based method** is fast, reliable for standard task sequences, and easy to adapt to well-known patterns.  
- The **AI-based method** handles more varied suggestions and can creatively propose tasks that are not explicitly defined in a pattern library.

## [License](./LICENSE)
