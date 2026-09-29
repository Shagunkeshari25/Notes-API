# Notes API

A backend REST API for creating, managing, and securely accessing personal notes. The project is built with **FastAPI** and uses **PostgreSQL** for persistent storage, **Redis** for caching, **JWT** for authentication, and **Docker** for containerized services.

## Features

* User registration and login
* JWT-based authentication
* Protected API endpoints
* User-specific notes
* Create, read, update, and delete notes
* Search notes by title or body
* Pagination using `limit` and `skip`
* Redis caching for note listing
* Automatic cache invalidation when notes are created, updated, or deleted
* PostgreSQL database
* Dockerized PostgreSQL and Redis services
* Automated API tests using Pytest
* Validation and HTTP error handling

## Tech Stack

| Technology | Purpose                      |
| ---------- | ---------------------------- |
| Python     | Backend programming          |
| FastAPI    | REST API framework           |
| PostgreSQL | Relational database          |
| SQLAlchemy | ORM and database interaction |
| Redis      | Caching                      |
| JWT        | Authentication               |
| Pydantic   | Request/response validation  |
| Docker     | Containerized services       |
| Pytest     | Automated testing            |

## Project Structure

```text
Notes-API/
│
├── Note/
│   ├── database.py
│   ├── hashing.py
│   ├── main.py
│   ├── models.py
│   ├── oauth2.py
│   ├── redis_client.py
│   ├── schemas.py
│   ├── token.py
│   │
│   ├── repository/
│   │   ├── notes.py
│   │   └── user.py
│   │
│   └── routers/
│       ├── authentication.py
│       ├── notes.py
│       └── user.py
│
├── tests/
│   ├── conftest.py
│   ├── test_auth.py
│   └── test_notes.py
│
├── docker-compose.yml
└── requirements.txt
```

## Authentication

The API uses **JWT Bearer authentication**.

The authentication flow is:

```text
Register
   ↓
Login
   ↓
JWT Access Token
   ↓
Send token with protected requests
   ↓
FastAPI verifies token
   ↓
User accesses their own notes
```

Protected note endpoints require:

```text
Authorization: Bearer <access_token>
```

Users can only access notes belonging to their own account.

## Notes API Endpoints

### Notes

| Method | Endpoint      | Description         | Authentication |
| ------ | ------------- | ------------------- | -------------- |
| GET    | `/notes/`     | Get user's notes    | Required       |
| POST   | `/notes/`     | Create a note       | Required       |
| GET    | `/notes/{id}` | Get a specific note | Required       |
| PUT    | `/notes/{id}` | Update a note       | Required       |
| DELETE | `/notes/{id}` | Delete a note       | Required       |

### Pagination

The notes listing endpoint supports pagination:

```text
GET /notes/?limit=10&skip=0
```

* `limit` — number of notes to return
* `skip` — number of notes to skip

### Search

Notes can be searched by title or body:

```text
GET /notes/?search=python
```

## Redis Caching

Redis is used to cache the results of the notes listing endpoint.

The cache key includes:

* User ID
* Limit
* Skip
* Search query

Cached results expire after **60 seconds**.

When a user creates, updates, or deletes a note, the related user cache is cleared so that subsequent requests receive updated data.

## Database

The application uses **PostgreSQL** as its relational database.

SQLAlchemy is used to interact with the database through Python models and database sessions.

The application reads the database connection configuration from the environment rather than hard-coding credentials in the source code.

## Environment Variables

Create a `.env` file in the project root:

```env
SECRET_KEY=your_secret_key
DATABASE_URL=your_database_url
REDIS_HOST=localhost
REDIS_PORT=6379
```

Do not commit your `.env` file or real secrets to GitHub.

## Running the Project

### 1. Clone the repository

```bash
git clone https://github.com/Shagunkeshari25/notes-api-fastapi.git

cd notes-api-fastapi
```

### 2. Create and activate a virtual environment

Windows PowerShell:

```powershell
python -m venv fastapi-env
.\fastapi-env\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create the `.env` file using the variables shown above.

### 5. Start PostgreSQL and Redis

If using Docker Compose:

```bash
docker compose up -d
```

Check running containers:

```bash
docker ps
```

### 6. Start FastAPI

```bash
uvicorn Note.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Interactive API documentation:

```text
http://127.0.0.1:8000/docs
```

## Testing

The project uses **Pytest** for automated API testing.

Run:

```bash
pytest
```

The test suite covers functionality including:

* User registration
* User login
* JWT authentication
* Note creation
* Note retrieval
* Note updating
* Note deletion
* Unauthorized note creation
* User isolation between accounts

For example, the tests verify that one user cannot access another user's private notes.

## Docker

Docker is used to run the supporting services required by the application.

The project uses:

* PostgreSQL container
* Redis container

FastAPI can be run locally with Uvicorn while PostgreSQL and Redis run through Docker Compose.

## API Documentation

FastAPI automatically provides interactive API documentation through Swagger UI:

```text
/docs
```

This allows endpoints to be viewed and tested directly from the browser.

## Future Improvements

Possible future improvements include:

* Refresh token authentication
* More advanced Redis usage
* Rate limiting
* API versioning
* Production deployment
* Logging and monitoring
* CI/CD pipeline


