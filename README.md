# Bad Electricity Usage Quiz

This is a Flask application that simulates a fun quiz to teach users how to be a "bad energy consumer" in Quebec. It is a joke application meant for educational purposes.

## Features:
- Unique usernames for users.
- Quiz available in French.
- Responses can be stored in memory, on disk, or in a PostgreSQL database.
- Scoreboard showing user scores and time taken to complete the quiz.

## How to Build and Run:

### Run with Docker:

```bash
docker-compose up
```

This will set up a PostgreSQL database and run the Flask application.

### Run Locally:

1.	Set up a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

2.	Install dependencies:
```bash
pip install -r requirements.txt
```

3.	Run the Flask application:
```bash
export FLASK_APP=app
export FLASK_ENV=development
flask run
```

### Adding Questions

To add more questions, modify the app/quiz.py file by adding more entries to the QUESTIONS dictionary.

## Environment Variables

The application uses the following environment variables:

- `DATABASE_URL`: The URL for the PostgreSQL database.

i.e.
```bash
export DATABASE_URL="postgresql://username:password@localhost:5432/dbname"
```

**Warning:** When using `DATABASE_URL`, ensure that the specified database exists before running the application. The application will not automatically create the database for you.
