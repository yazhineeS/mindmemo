# MindMemo: Daily Thoughts Journal

A small web app where each user signs up, logs in, and keeps a private journal of daily thoughts.

## Features
- Sign up and log in (passwords are stored as hashes, not plain text)
- Write and save entries with a date and time
- View your own previous entries, newest first
- Delete an entry (with a confirmation)
- Each user sees only their own entries

## Built with
- Python and Flask (backend)
- SQLite (database, created automatically as `mindmemo.db`)
- HTML, CSS and JavaScript (templates and static files)

## Project structure
app.py            Flask app: routes, login, database code
templates/        login.html, index.html
static/           style.css, script.js
requirements.txt  Python packages


## How to run
1. Install Python 3.
2. In a terminal, go to the project folder and install Flask:
   pip install -r requirements.txt
   
3. Start the app:
   python app.py

4. Open http://127.0.0.1:5000 in your browser and create an account.

The database file `mindmemo.db` is created automatically the first time the app runs.

### Optional settings
- `SECRET_KEY`: secret used to sign the login cookie. Set it for any real deployment.
- `FLASK_DEBUG=1`: turn on debug mode (local use only).

## Ideas for improvement
- Edit existing entries
- CSRF protection on the forms (for example with Flask-WTF)
- Search entries by date or word

## Author
Yazhini Senthilkumar