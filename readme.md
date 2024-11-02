"""
# Library Management System API

A FastAPI-based REST API for managing books and authors.

## Prerequisites

- Python 3.8+
- PostgreSQL
- Redis

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a PostgreSQL database:
```sql
CREATE DATABASE library_db;
```

4. Create `.env` file with your database configuration:
```
DATABASE_URL=postgresql://username:password@localhost:5432/library_db
REDIS_URL=redis://localhost:6379/0
```

5. Run database migrations:
```bash
alembic upgrade head
```

6. Start the application:
```bash
uvicorn app.main:app --reload
```

## Testing

1. Create a test database:
```sql
CREATE DATABASE library_test_db;
```

2. Run tests:
```bash
pytest
```

## Performance Optimization for Large Scale

1. Database Indexing:
   - Indexes are created on frequently queried fields
   - Consider adding composite indexes based on query patterns

2. Connection Pooling:
   - SQLAlchemy connection pool is configured for optimal performance
   - Pool size and timeout settings can be adjusted based on load

3. Caching Strategy:
   - Redis caching implemented for frequently accessed data
   - Cache invalidation on data updates
   - Configurable cache expiration times

4. Query Optimization:
   - Eager loading relationships when needed
   - Pagination implemented for large result sets
   - Selective column loading

5. Future Scalability:
   - Consider implementing read replicas for heavy read workloads
   - Implement database partitioning for large tables
   - Add connection pooling at the application level
"""

# Project Structure
library-management-system/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── crud.py
│   └── cache.py
├── tests/
│   ├── __init__.py
│   └── test_api.py
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── .dockerignore
└── README.md

# app/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    REDIS_URL: str
    
    class Config:
        env_file = ".env"

settings = Settings()

# requirements.txt
fastapi==0.109.0
uvicorn==0.27.0
sqlalchemy==2.0.25
psycopg2-binary==2.9.9
pydantic==2.5.3
python-dotenv==1.0.0
pytest==7.4.4
httpx==0.26.0
redis==5.0.1
alembic==1.13.1

# Library Management System

## Setup and Installation

1. Clone the repository
2. Make sure Docker and Docker Compose are installed on your system
3. Run the following commands:

```bash
# Build and start the services
docker-compose up --build

# To run in detached mode
docker-compose up -d --build

# To view logs
docker-compose logs -f

# To stop the services
docker-compose down
```

## API Documentation

Once the services are running, you can access:
- API documentation: http://localhost:8000/docs
- Alternative API documentation: http://localhost:8000/redoc

## Database Migrations

Initial database migration and subsequent updates can be managed using Alembic:

```bash
# Create a new migration
docker-compose exec api alembic revision --autogenerate -m "description"

# Apply migrations
docker-compose exec api alembic upgrade head
```

## Testing

To run the tests:

```bash
docker-compose exec api pytest
```

## Services

The application runs three services:
1. API (FastAPI application) - Port 8000
2. PostgreSQL Database - Port 5432
3. Redis Cache - Port 6379

## Environment Variables

The following environment variables are set in docker-compose.yml:
- DATABASE_URL
- REDIS_URL