# Cinema API

Cinema API is a RESTful API service for managing movies, actors, genres, cinema halls, movie sessions, orders, and tickets.

The project is built with Django REST Framework and uses PostgreSQL, JWT authentication, Swagger/OpenAPI documentation, Docker, and Docker Compose.

## Features

* User registration
* JWT authentication
* User profile management
* Movie management
* Actor management
* Genre management
* Cinema hall management
* Movie session management
* Ticket ordering
* Movie image upload
* Movie filtering
* Movie session filtering
* Swagger/OpenAPI documentation
* PostgreSQL database
* Dockerized application
* Persistent Docker volumes for PostgreSQL, static files, and media files
* Automatic database migrations on container startup
* Automatic static file collection
* Database availability check with `wait_for_db`
* API throttling
* Automated tests

Additional business rules:

* Tickets cannot be purchased for movie sessions that have already started.
* Movie sessions cannot be scheduled in the past.
* Ticket row and seat values are validated against the selected cinema hall.
* The same seat cannot be booked twice for the same movie session.

## Technologies

* Python 3.12
* Django
* Django REST Framework
* PostgreSQL 17
* Simple JWT
* drf-spectacular
* Docker
* Docker Compose

## Project Structure

```text
cinema-api/
├── cinema/
├── cinema_service/
├── user/
├── Dockerfile
├── docker-compose.yml
├── .dockerignore
├── .env.sample
├── manage.py
├── requirements.txt
└── README.md
```

## Installation with Docker

Clone the repository:

```bash
git clone git@github.com:supremacy91/cinema-api.git
cd cinema-api
```

Create your local environment file:

```bash
cp .env.sample .env
```

Example `.env`:

```env
DJANGO_SECRET_KEY=change-me
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost

POSTGRES_HOST=db
POSTGRES_PORT=5432
POSTGRES_DB=cinema
POSTGRES_USER=cinema
POSTGRES_PASSWORD=cinema
```

Build and start the project:

```bash
docker compose up --build
```

Or run it in the background:

```bash
docker compose up -d --build
```

The application will be available at:

```text
http://127.0.0.1:8000/
```

## Docker Services

The project uses two main services:

```text
app
```

Django REST Framework application.

```text
db
```

PostgreSQL database.

Docker Compose also creates persistent volumes for:

```text
postgres_data
static_data
media_data
```

These volumes store database data, collected static files, and uploaded media files.

## Automatic Startup

When the `app` container starts, it executes:

```text
wait_for_db => migrate => collectstatic => runserver
```

This means the application waits until PostgreSQL becomes available before starting database operations.

## API Documentation

Swagger UI:

```text
http://127.0.0.1:8000/api/doc/
```

ReDoc:

```text
http://127.0.0.1:8000/api/redoc/
```

OpenAPI schema:

```text
http://127.0.0.1:8000/api/schema/
```

## Authentication

The API uses JWT authentication.

### Register a user

```http
POST /api/user/register/
```

### Obtain access and refresh tokens

```http
POST /api/user/token/
```

Example request:

```json
{
  "email": "user@example.com",
  "password": "your-password"
}
```

Example response:

```json
{
  "refresh": "...",
  "access": "..."
}
```

### Refresh access token

```http
POST /api/user/token/refresh/
```

Example:

```json
{
  "refresh": "your-refresh-token"
}
```

### Current user

```http
GET /api/user/me/
PUT /api/user/me/
PATCH /api/user/me/
```

For authenticated requests, send:

```http
Authorization: Bearer <access_token>
```

## Cinema API Endpoints

Base URL:

```text
/api/cinema/
```

### Genres

```http
GET    /api/cinema/genres/
POST   /api/cinema/genres/
GET    /api/cinema/genres/{id}/
PUT    /api/cinema/genres/{id}/
PATCH  /api/cinema/genres/{id}/
DELETE /api/cinema/genres/{id}/
```

### Actors

```http
GET    /api/cinema/actors/
POST   /api/cinema/actors/
GET    /api/cinema/actors/{id}/
PUT    /api/cinema/actors/{id}/
PATCH  /api/cinema/actors/{id}/
DELETE /api/cinema/actors/{id}/
```

### Cinema Halls

```http
GET    /api/cinema/cinema_halls/
POST   /api/cinema/cinema_halls/
GET    /api/cinema/cinema_halls/{id}/
PUT    /api/cinema/cinema_halls/{id}/
PATCH  /api/cinema/cinema_halls/{id}/
DELETE /api/cinema/cinema_halls/{id}/
```

### Movies

```http
GET    /api/cinema/movies/
POST   /api/cinema/movies/
GET    /api/cinema/movies/{id}/
PUT    /api/cinema/movies/{id}/
PATCH  /api/cinema/movies/{id}/
DELETE /api/cinema/movies/{id}/
```

Upload a movie image:

```http
POST /api/cinema/movies/{id}/upload-image/
```

### Movie Sessions

```http
GET    /api/cinema/movie_sessions/
POST   /api/cinema/movie_sessions/
GET    /api/cinema/movie_sessions/{id}/
PUT    /api/cinema/movie_sessions/{id}/
PATCH  /api/cinema/movie_sessions/{id}/
DELETE /api/cinema/movie_sessions/{id}/
```

### Orders

```http
GET  /api/cinema/orders/
POST /api/cinema/orders/
GET  /api/cinema/orders/{id}/
```

## Filtering

Movies can be filtered by title, genre, and actor.

Examples:

```text
/api/cinema/movies/?title=matrix
/api/cinema/movies/?genres=1,2
/api/cinema/movies/?actors=1,3
```

Movie sessions can be filtered by date and movie.

Examples:

```text
/api/cinema/movie_sessions/?date=2026-08-18
/api/cinema/movie_sessions/?movie=1
```

## Tests

Run all tests inside Docker:

```bash
docker compose exec app python manage.py test
```

Run Django system checks:

```bash
docker compose exec app python manage.py check
```

Check for missing migrations:

```bash
docker compose exec app python manage.py makemigrations --check --dry-run
```

Run code style checks:

```bash
docker compose exec app flake8
```

## Stop the Project

Stop and remove containers:

```bash
docker compose down
```

This keeps Docker volumes and PostgreSQL data.

To also delete all project volumes:

```bash
docker compose down -v
```

Warning: this deletes the PostgreSQL volume and therefore removes the stored database data.

## Development Branch

Development is performed in:

```text
develop
```

Completed changes are merged into:

```text
main
```

through a Pull Request.
