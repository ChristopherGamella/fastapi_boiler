# FastAPI Boilerplate

A production-ready FastAPI boilerplate with the best developer experience.

## Features

- **FastAPI** - Modern, fast web framework for building APIs
- **SQLAlchemy** - SQL toolkit and ORM with async support
- **Alembic** - Database migrations
- **Pydantic** - Data validation and settings management
- **JWT Authentication** - With OAuth2 and bearer tokens
- **SQLite** - For development (easily switch to PostgreSQL or other databases)
- **Async Support** - Full async/await support throughout the application
- **API Versioning** - Support for multiple API versions
- **Testing** - Pytest with async support
- **Production-ready** - Includes best practices for production deployment
- **Developer Tools** - Black, isort, flake8, mypy, pre-commit

## Requirements

- Python 3.9+

## Setup

1. Clone the repository:

   ```
   git clone <repository-url>
   cd fastapi-boilerplate
   ```

2. Create a virtual environment:

   ```
   python -m venv venv
   ```

3. Activate the virtual environment:

   - **Windows**: `venv\Scripts\activate`
   - **Unix/MacOS**: `source venv/bin/activate`

4. Install dependencies:

   ```
   pip install -r requirements.txt
   ```

5. Create a `.env` file based on `.env.example`:

   ```
   cp .env.example .env
   ```

6. Initialize the database:

   ```
   alembic upgrade head
   ```

7. Run the development server:

   ```
   python run.py
   # or
   uvicorn main:app --reload
   ```

8. Open your browser at [http://localhost:48001](http://localhost:48001)
   - API Docs: [http://localhost:48001/docs](http://localhost:48001/docs)
   - ReDoc: [http://localhost:48001/redoc](http://localhost:48001/redoc)

## Docker

You can also run the application using Docker:

### Using Docker Compose

1. Create a `.env` file based on `.env.example`:

   ```
   cp .env.example .env
   ```

2. Update the `.env` file to use PostgreSQL:

   ```
   DATABASE_URL=postgresql://postgres:postgres@db:5432/fastapi_db
   ```

3. Start the Docker containers:

   ```
   docker-compose up -d
   ```

4. The API will be available at [http://localhost:48001](http://localhost:48001)

### Using Docker only

1. Build the Docker image:

   ```
   docker build -t fastapi-boilerplate .
   ```

2. Run the container:

   ```
   docker run -d --name fastapi-app -p 48001:48001 fastapi-boilerplate
   ```

## Development

### Database Migrations

Create a new migration:

```
alembic revision --autogenerate -m "Description of changes"
```

Apply migrations:

```
alembic upgrade head
```

### Testing

Run the tests:

```
pytest
```

With coverage:

```
pytest --cov=app
```

### Code Quality

Install pre-commit hooks:

```
pre-commit install
```

Run code quality checks manually:

```
pre-commit run --all-files
```

## Contribution Guidelines

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit your changes: `git commit -m 'Add some feature'`
4. Push to the branch: `git push origin feature-name`
5. Submit a pull request

### Coding Standards

- Follow PEP 8 style guide
- Write tests for new features
- Update documentation as needed

## API Structure

The API follows a layered architecture:

- **Endpoints**: API routes handled by FastAPI controllers
- **Schemas**: Pydantic models for request/response validation
- **Services**: Business logic and operations
- **Models**: SQLAlchemy ORM models
- **Database**: Database connection and session management

```
pre-commit run --all-files
```

## Project Structure

```
.
├── alembic/                # Database migrations
├── app/
│   ├── api/                # API endpoints
│   │   └── v1/             # API v1
│   ├── core/               # Core application config
│   ├── db/                 # Database setup
│   ├── models/             # SQLAlchemy models
│   ├── schemas/            # Pydantic schemas
│   ├── services/           # Business logic
│   └── tests/              # Tests
├── .env                    # Environment variables
├── .env.example            # Example environment variables
├── .pre-commit-config.yaml # Pre-commit hooks
├── alembic.ini             # Alembic config
├── main.py                 # Application entry point
├── pyproject.toml          # Python project config
├── pytest.ini              # Pytest config
└── requirements.txt        # Dependencies
```

## API Documentation

- Swagger UI: [http://localhost:48001/docs](http://localhost:48001/docs)
- ReDoc: [http://localhost:48001/redoc](http://localhost:48001/redoc)

## License

This project is licensed under the MIT License.
