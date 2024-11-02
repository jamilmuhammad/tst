# Library Management System

A FastAPI-based REST API for managing books and authors.

## Prerequisites

- Python 3.8+
- PostgreSQL
- Redis
- Docker

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