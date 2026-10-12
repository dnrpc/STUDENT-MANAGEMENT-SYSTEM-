# Student Management System

A desktop application built with Python, Tkinter, and SQLite for managing student records.

## Features

- Add student records
- View all saved students
- Search by roll number, name, course, email, or phone
- Update selected student records
- Delete records with confirmation
- Store records locally in an SQLite database
- Validate required fields and prevent duplicate roll numbers

## Technology

- Python 3
- Tkinter (usually included with standard Python installations)
- SQLite (included with Python)

## Run the application

1. Install Python 3 from https://www.python.org/downloads/.
2. Download or clone this repository.
3. Open a terminal in the project folder.
4. Run:

   ```bash
   python main.py
   ```

   On some Windows installations, use `py main.py`.

The application creates `students.db` in the current working directory the first time it runs. Keep this file to retain your records.

## Important note about GitHub Pages

GitHub Pages hosts the project's documentation only. It cannot run this Python desktop application or its SQLite database in a visitor's browser. To use the program, download the repository and run it locally with Python.

## Project files

- `main.py` — application source code
- `requirements.txt` — external Python dependencies (none required)
- `index.md` — GitHub Pages homepage
- `setup.md` — setup guide
- `features.md` — feature overview
- `screenshots.md` — screenshot page
- `documentation.md` — technical overview

## Data and privacy

Student records are stored locally in `students.db`. Use sample data for demonstrations and do not commit real student personal information to a public repository.
