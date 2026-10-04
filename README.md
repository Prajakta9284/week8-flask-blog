

1. Project Overview and Objectives

Project Overview

The **Flask Blog / Forum Application** is a web-based application developed using **Python Flask**. The application allows users to register, log in, create and manage blog posts, upload images, add comments, search posts, and view an RSS feed.

The project uses **SQLite** as the database and **SQLAlchemy** for database operations. **Flask-Login** is used to manage user authentication and sessions. The application also includes Bootstrap-based pages, static files, image uploads, categories/tags, and other features.

The application was developed locally using Python and VS Code and was later deployed on **PythonAnywhere**.

Project Objectives

The main objectives of the project are:

1. To develop a functional blog/forum web application using Flask.
2. To implement user registration, login, logout, and authentication.
3. To allow authenticated users to create, edit, and delete posts.
4. To provide a commenting system.
5. To implement image uploading for posts.
6. To provide search and pagination functionality.
7. To implement RSS feed support.
8. To store application data using SQLite and SQLAlchemy.
9. To protect passwords using password hashing.
10. To test the application and deploy it online.
11. To implement a database backup system.

---

2. Setup and Installation Instructions

System Requirements

The project requires:

- Python 3.x
- Flask
- Flask-SQLAlchemy
- Flask-Login
- Werkzeug
- Git
- Web browser
- VS Code or another Python IDE

Project Installation

Step 1: Download the Project

The project is available in the GitHub repository:

**Repository:** `week8-flask-blog`

The project can be cloned using:

git clone https://github.com/Prajakta9284/week8-flask-blog.git


Then move into the project directory:


cd week8-flask-blog


Step 2: Create a Virtual Environment

Create a virtual environment:


python -m venv venv


Activate it on Windows PowerShell:


.\venv\Scripts\Activate.ps1

After activation, the terminal displays:


(venv)

Step 3: Install Required Packages

Install the dependencies using:


pip install -r requirements.txt


The main packages used in the project include:

```text
Flask
Flask-SQLAlchemy
Flask-Login
Werkzeug
```

Step 4: Run the Application

Start the Flask application using:


python app.py


The application runs locally at:


http://127.0.0.1:5000


Open this address in a web browser to access the application.

Step 5: Database

The application uses SQLite with SQLAlchemy.

The database tables are created using:


with app.app_context():
    db.create_all()

Step 6: Deployment

The project was pushed to GitHub and deployed on PythonAnywhere.

The deployment process included:


Local Flask Project
       ↓
Git Repository
       ↓
GitHub
       ↓
PythonAnywhere
       ↓
Virtual Environment
       ↓
WSGI Configuration
       ↓
Live Flask Website


---

3. Code Structure Explanation

The project is organized into different folders and files to keep the application manageable.


week8-flask-blog/
│
├── app.py
├── requirements.txt
├── .gitignore
│
├── backups/
│   └── backup.py
│
├── static/
│   ├── css/
│   ├── js/
│   └── uploads/
│
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── profile.html
│   ├── create_post.html
│   ├── edit_post.html
│   └── ...
│
└── tests/
    └── test_app.py


 `app.py`

`app.py` is the main Flask application file.

It contains:

- Flask application configuration
- Database configuration
- SQLAlchemy setup
- Flask-Login configuration
- User model
- Post model
- Comment model
- Authentication routes
- Post routes
- Comment routes
- Search functionality
- Pagination
- Image upload functionality
- RSS feed
- Logout functionality

The Flask application is initialized using:

python
app = Flask(__name__)


`templates/`

The `templates` folder contains HTML files used to create the application's user interface.

Examples include:

- `base.html` — common layout/navigation
- `index.html` — home page
- `login.html` — login page
- `register.html` — registration page
- `profile.html` — user profile
- `create_post.html` — create post page
- `edit_post.html` — edit post page

Flask's `render_template()` function is used to display these pages.

`static/`

The `static` folder contains files that do not change dynamically.

It contains:

- CSS files
- JavaScript files
- Uploaded images

These files are used to control the appearance and behavior of the website.

`backups/`

The `backups` folder contains the database backup script.

`backup.py` creates a copy of the SQLite database with a timestamp so that data can be restored if required.

`tests/`

The `tests` folder contains automated tests for the Flask application.

The tests verify that important routes and application functions work correctly.

`requirements.txt`

This file contains the Python packages required to run the application.

It allows the same dependencies to be installed easily on another computer or hosting platform.

`.gitignore`

The `.gitignore` file prevents unnecessary or sensitive files from being uploaded to GitHub.

Examples include:


venv/
__pycache__/
*.pyc
.env


---

4. How the Technical Requirements Were Met

4.1 Flask Framework

The application was developed using the Flask framework.

Flask handles:

- URL routing
- HTTP requests
- HTML rendering
- Form processing
- Application configuration

Example:

python
@app.route("/")
def home():
    return render_template("index.html")

4.2 Database

SQLite was used as the database.

SQLAlchemy provides interaction between Python objects and database tables.

The application contains models for:

- Users
- Posts
- Comments

4.3 User Authentication

The application implements:

- User registration
- Login
- Logout
- Protected routes
- Password hashing

`Flask-Login` is used for session and authentication management.

Passwords are not stored as plain text. Werkzeug password hashing functions are used to securely store passwords.

4.4 CRUD Operations

CRUD functionality was implemented for posts.

CRUD stands for:

| Operation | Function |
|---|---|
| Create | Create a new post |
| Read | View posts |
| Update | Edit an existing post |
| Delete | Delete a post |

Authenticated users can manage their posts according to the application's authorization rules.

4.5 Comments

Users can add comments to posts.

The comment functionality allows users to interact with the content and provides a basic discussion/forum feature.

4.6 Search and Pagination

The application provides post searching so users can find relevant content.

Pagination is used to divide large numbers of posts into smaller pages, improving usability.

4.7 Image Upload

The application supports image uploads.

Uploaded images are stored in:


static/uploads/


Allowed image extensions are controlled by the application to prevent unsupported files from being uploaded.

4.8 RSS Feed

An RSS feed was implemented so that users can access the latest blog posts through an RSS reader.

The RSS route provides XML-formatted content.

Example:


/rss


4.9 Front-End Design

HTML templates are used for the user interface.

Bootstrap styling was used to create a responsive and user-friendly design.

Common elements such as navigation, forms, buttons, cards, and layouts are shared using the base template.

4.10 Testing

The application was tested using both automated and manual testing.

Automated testing was implemented using Python testing tools.

Important user flows were manually tested, including:

- Registration
- Login
- Logout
- Post creation
- Post editing
- Post deletion
- Comments
- Image upload
- Search
- RSS
- Protected pages

4.11 Version Control

Git was used for version control.

The project was initialized as a Git repository and pushed to GitHub.

The main branch used for the project is:


main


Git helps maintain project history and makes it easier to deploy the application.

4.12 Deployment

The application was deployed using PythonAnywhere.

The deployment process included:

1. Uploading the project to GitHub.
2. Cloning the GitHub repository on PythonAnywhere.
3. Creating a Python virtual environment.
4. Installing packages from `requirements.txt`.
5. Configuring the Flask application.
6. Configuring the WSGI file.
7. Configuring static files.
8. Creating the database.
9. Reloading the web application.
10. Testing the live website.

4.13 Backup System

A backup system was implemented using `backup.py`.

The script creates timestamped copies of the SQLite database.

Example backup filename:


forum_backup_20261004_192500.db


This provides a way to recover database information if the original database is lost or damaged.

---

Conclusion

The Flask Blog / Forum Application successfully meets the required technical objectives. It provides user authentication, database management, CRUD operations, comments, image uploads, search, pagination, RSS functionality, testing, version control, deployment, and database backup.

The project was developed locally, managed using Git and GitHub, and successfully deployed on PythonAnywhere. The application demonstrates the practical use of Python Flask for developing and deploying a complete web application.