# Task Collaboration Tool

A web-based task management application built using Python, Flask, and SQLite. It allows users to manage their tasks, track progress, set deadlines, and organize their work through a simple dashboard.

## Features

* **User Registration:** Create a new account.
* **User Login and Logout:** Securely access and leave your account.
* **Password Hashing:** Passwords are hashed before being stored in the database.
* **Add Tasks:** Create tasks with a title and description.
* **Task Search:** Search for tasks by title.
* **Status Filtering:** Filter tasks by Pending, In Progress, or Completed.
* **Task Deadlines:** Set deadlines for tasks.
* **Update Task Status:** Track task progress.
* **Delete Tasks:** Remove tasks when they are no longer needed.
* **Dashboard Statistics:** View total, pending, in-progress, and completed task counts.
* **SQLite Database:** Store user accounts and tasks locally.

## Technologies Used

* Python
* Flask
* SQLite
* HTML
* CSS
* Werkzeug

## Project Structure

```text
TaskCollaborationTool/
├── app.py
├── tasks.db
├── templates/
│   ├── base.html
│   ├── login.html
│   ├── register.html
│   └── dashboard.html
├── static/
│   └── style.css
├── .gitignore
└── README.md
```

The `tasks.db` database is created automatically when the application starts. It is excluded from GitHub using `.gitignore`.

## Requirements

* Python 3
* pip

## Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/sharanyaveeranki-creator/TaskCollaborationTool.git
```

### 2. Open the Project Folder

```bash
cd TaskCollaborationTool
```

### 3. Install Flask

```bash
py -m pip install flask
```

### 4. Run the Application

```bash
py app.py
```

### 5. Open in Your Browser

Visit:

http://127.0.0.1:5000

Register an account or log in to start managing tasks.

## How to Use

1. Register a new account.
2. Log in to the application.
3. Add tasks with titles and descriptions.
4. Optionally set a deadline for each task.
5. Search for tasks by title.
6. Filter tasks by their status.
7. Update tasks as you make progress.
8. Delete tasks when they are no longer required.
9. Monitor your progress using dashboard statistics.

## Database

The application uses SQLite to store user accounts and tasks. The database file is created locally and is not included in the repository.

## Future Improvements

* Assign tasks to team members.
* Add task priorities.
* Send deadline reminders.
* Improve dashboard analytics.
* Deploy the application online.

## Author

**Soppari Vamshi**

## License

This project is available for educational and learning purposes.
