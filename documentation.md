# Technical Documentation

## Architecture

The application is a local Python desktop program. The user interface is built with Tkinter and the data is stored in SQLite.

## Source file

- `main.py`: creates the interface, validates input, runs CRUD operations, and refreshes the student table.

## Database

The `students` table contains:

| Field | Purpose |
|---|---|
| `id` | Automatically generated primary key |
| `roll_no` | Unique student roll number |
| `name` | Student name |
| `course` | Course or programme |
| `email` | Optional email address |
| `phone` | Optional phone number |

## CRUD operations

- **Create:** Add Student
- **Read:** table view and search
- **Update:** Update Selected
- **Delete:** Delete Selected, with confirmation

## Limitations

- This is a local desktop application, not a multi-user web application.
- The database is stored on the computer where the application runs.
- GitHub Pages hosts documentation only and does not execute Python code.
