# Notes API

A backend REST API for creating, managing, and securely accessing personal notes. The project is built with **FastAPI** and uses **PostgreSQL** for persistent storage, **Redis** for caching, **JWT** for authentication, and **Docker** for containerized services.

**Live demo:** https://notes-api-qwgc.onrender.com/docs
*(Hosted on a free tier, so the first request may take about 50 seconds to wake up.)*

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
* Docker Compose setup for the full stack (app, PostgreSQL, Redis)
* Automated API tests using Pytest
* Validation and HTTP error handling
* Deployed on Render

## Tech Stack

| Technology | Purpose                                         |
| ---------- | ----------------------------------------------- |
| Python     | Backend programming                             |
| FastAPI    | REST API framework                              |
| PostgreSQL | Relational database                             |
| SQLAlchemy | ORM and database interaction                    |
| Redis      | Caching                                         |
| JWT        | Authentication                                  |
| Pydantic   | Request/response validation                     |
| Docker     | Containerized services                          |
| Pytest     | Automated testing                               |
| Render     | Cloud hosting for the app, PostgreSQL and Redis |

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
├── Dockerfile
├── docker-compose.yml
├── .dockerignore
├── pytest.ini
├── requirements.txt
└── requirements-dev.txt
```

## Authentication

The API uses **JWT Bearer authentication**.

```text
Register → Login → JWT access token → Send token with requests
→ FastAPI verifies token → User accesses their own notes
```

Protected note endpoints require:

```text
Authorization: Bearer <access_token>
```

Users can only access notes belonging to their own account.

## API Endpoints

### Authentication and Users

| Method | Endpoint | Description         |
| ------ | -------- | ------------------- |
| POST   | `/login` | Log in, get a JWT   |
| POST   | `/user/` | Register a new user |

### Notes

| Method | Endpoint      | Description         | Authentication |
| ------ | ------------- | ------------------- | -------------- |
| GET    | `/notes/`     | Get user's notes    | Required       |
| POST   | `/notes/`     | Create a note       | Required       |
| GET    | `/notes/{id}` | Get a specific note | Required       |
| PUT    | `/notes/{id}` | Update a note       | Required       |
| DELETE | `/notes/{id}` | Delete a note       | Required       |

**Pagination:** `GET /notes/?limit=10&skip=0`
`limit` is the number of notes to return, and `skip` is the number to skip.

**Search:** `GET /notes/?search=python`

Interactive Swagger documentation is available at `/docs`.

## Redis Caching

Redis caches the results of the notes listing endpoint. The cache key includes the user ID, limit, skip, and search query. Cached results expire after **60 seconds**. When a user creates, updates, or deletes a note, that user's cache is cleared so the next request returns fresh data.

## Database

The app uses **PostgreSQL** through **SQLAlchemy** models and sessions. The connection is read from the `DATABASE_URL` environment variable and is not hard-coded.

## Environment Variables

Create a `.env` file in the project root:

```env
SECRET_KEY=your_secret_key
```

`DATABASE_URL`, `REDIS_HOST`, and `REDIS_PORT` are set in `docker-compose.yml` (and as environment variables on Render). Do not commit your `.env` file or real secrets to GitHub.

## Running the Project

```bash
git clone https://github.com/Shagunkeshari25/Notes-API.git
cd Notes-API
```

Create a `.env` file containing `SECRET_KEY=your_secret_key`, then run:

```bash
docker compose up --build
```

The API will be available at `http://localhost:8000/docs`.

## Testing

Create a virtual environment and run `pip install -r requirements.txt` first.

The tests use SQLite and a fake in-memory Redis, but importing the app still connects to PostgreSQL, so start it first:

```bash
docker compose up -d postgres redis
pytest
```

The test suite covers:

* User registration and login
* JWT authentication
* Note creation, retrieval, updating, and deletion
* Unauthorized note creation
* User isolation between accounts

## Docker

Docker Compose defines three services:

| Service    | Purpose             |
| ---------- | ------------------- |
| `app`      | FastAPI application |
| `postgres` | PostgreSQL database |
| `redis`    | Redis cache         |

PostgreSQL data is stored in a named Docker volume, so it persists across restarts.

```bash
docker compose up --build   # build and start everything
docker compose down         # stop and remove containers (data is kept)
```

## Deployment

The app is deployed on **Render** from the project's `Dockerfile`, using a Render PostgreSQL database and a Render Key Value (Redis) instance. Configuration is provided through the environment variables `DATABASE_URL`, `REDIS_HOST`, `REDIS_PORT`, and `SECRET_KEY`.

## Future Improvements

* Refresh token authentication
* Rate limiting
* API versioning
* Database migrations (for example Alembic) instead of creating tables at startup
* Logging and monitoring
* CI/CD pipeline