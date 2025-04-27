# Django DRF Demo of API implementation

This is a demo Django project to provide APIs for managing user rewards, with administration of models,
with periodic task handled by Celery Beat, with extensive unittests (> 95%), and online OpenAPI/Swagger documentation

## Features

- User authentication with JWT tokens
- User profile management with coins system
- Scheduled rewards processing
- Online API documentation with Swagger/ReDoc
- Celery task queue integration
- Docker containerization
- Unittests with coverage report
- Python 3.13+, Django 5.1+, Celery 5.5+

## Prerequisites

- Docker and Docker Compose
- Make (optional, for testing & development commands)

## Quick Start

1. Clone the repository from GitHub:
```bash
git clone https://github.com/sokolovdp/api_platform
cd api_platform
```
3. Start the services:
```bash
docker-compose up -d
```
4. Open a web browser and navigate to http://localhost:8000/api/docs/
5. To create superuser, run:
```bash
docker exec -it api_service bash -c "python manage.py createsuperuser"
```
Create a superuser with username `admin` and password `admin`, or any other username and password.

6. Using credentials of created superuser you can enter Django admin: http://localhost:8000/admin/

## Environment Variables

All variables have default values, but can be customized through `.env` file:

- `POSTGRES_DB`: Database name (default: postgres)
- `POSTGRES_USER`: Database user (default: postgres)
- `POSTGRES_PASSWORD`: Database password (default: postgres)
- `POSTGRES_HOST`: Database host (default: db)
- `POSTGRES_PORT`: Database port (default: 5432)
- `REDIS_HOST`: Redis host (default: redis)
- `REDIS_PORT`: Redis port (default: 6379)
- `REDIS_DB`: Redis database number (default: 0)

## API Endpoints

### Authentication

- `POST /api/token/` - Obtain JWT token pair
- `POST /api/token/refresh/` - Refresh JWT token
- `POST /api/token/verify/` - Verify JWT token

### Profile Management

- `GET /api/profile/` - Get user profile

### Rewards System

- `GET /api/rewards/` - List available rewards
- `POST /api/rewards/request/` - Request a reward

## API Documentation

Interactive API documentation is available at:

- Swagger UI: http://localhost:8000/api/docs/
- ReDoc: http://localhost:8000/api/redoc/

## Development

The project includes development tools (to run tests you install tests dependencies):

```bash
# Format code
make pretty

# Run linting
make lint
```

## Project Structure

```
.
├── api/                   # Main API application
│   ├── models.py          # Database models
│   ├── views.py           # API views
│   ├── serializers.py     # DRF serializers
│   └── tasks.py           # Celery tasks
├── api_case/              # Project configuration
├── tests/                 # Folder with unittests
├── docker-compose.yml     # Docker services configuration
├── Dockerfile             # API service build instructions
├── requirements.txt       # Django application dependencies
├── requirements_prod.txt  # Python dependencies, required in production
├── requirements_test.txt  # Python dependencies, required for testing
├── start-api.sh           # bash script to start API container
├── start-celery-worker.sh # bash script to start Celery worker container
├── start-celery-beat.sh   # bash script to start Celery beat container
└── Makefile               # Development commands
```

## Testing

The project uses Django's test framework with parameterized tests. Run tests with:

```bash
make test
```
