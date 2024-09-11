# <a href="https://todo-list-7a5c.onrender.com">TODO-List Project</a>

This is a simple Todo List application built with Django with CRUD functionality and designed to allow users to create, update, and delete tasks. The app also features user authentication, allowing tasks to be managed individually for each user.

Features
User registration and login/logout functionality.
Create, update, and delete tasks.
Tasks are user-specific (each user has their own set of tasks).
Use of Django's built-in authentication system.
Responsive user interface with Bootstrap.
Simple, minimalistic design.


Setup and Installation :

1] First need to install the project from github repository.

2] Create a Virtual Environment
To keep your project dependencies isolated, it's recommended to create a virtual environment.
python -m venv venv

 On linux computer
source venv/bin/activate   

#On Windows use 
`venv\Scripts\activate`

3] Install Dependencies

Install all required packages from the requirements.txt file:
pip install -r requirements.txt

If requirements.txt is missing, create it by running:
pip freeze > requirements.txt

4] Go to the directory, where the manage.py file is located

Run the Development Server
To start the Django development server, use the following command:
python manage.py runserver

Create a Superuser (
To access the Django admin panel, create a superuser:

python manage.py createsuperuser
