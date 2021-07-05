# My Tech Test

In this repository I'm going to showcase my abilities and techniques in django by solving and coding a task that used in
an job interview.

# Task Description

A client has requested we create a Directory app containing all the Teachers in a given school. Each teacher should have
the following information

- First Name
- Last Name
- Profile picture
- Email Address
- Phone Number
- Room Number
- Subjects taught

Teachers can have the same first name and last name but their email address should be unique. A teacher can teach no
more than 5 subjects. The directory should allow Teachers to filtered by first letter of last name or by subject. You
should be able to click on a teach in the directory and open up the profile page. From there you can see all details for
the teacher. An Importer will be needed to allow Teachers details to be added to the system in bulk. This should be
secure so only logged in users can run the importer. The CSV attached contains a list of teacher who need to be uploaded
as well as the filename for the profile image. Profile images are in the attached Zip file. if an image is not present
for the profile then you should use a default placeholder image. You can use SQLite for the database backend for
simplicity Your code should be uploaded to either Github or Bitbucket. And have instructions on how to set up the
project and how to run it.

# Set up the project

1. Clone and change directory to project directory
2. Create a virtual environment: `python -m venv venv`
3. Install `requirements.txt`: `pip install -r requirements.txt`
4. Set environment variables as follows:

```dotenv
SECRET_KEY=some-secret-key
PYTHONUNBUFFERED=1
DJANGO_SETTINGS_MODULE=tech_test.settings.development
```

5. Migrate: `python manage.py migrate`
6. Create a superuser: `python manage.py createsuperuser`
7. Run server: `python manage.py runserver`

# Model Dependency Graph

I considered a m2m relationship between Teacher and Subject, Because it makes sense and makes it easy to filter by
subject!

# Procedure

1. Upload required files
2. Store files temporarily on disk
3. Read data from CSV and normalize them
4. Create `Teacher` object and assign its profile picture (None in case of no-profile)
5. Create related `Subject` objects
6. Make m2m relationship using `add()` function

# Notes

- For filtering I used the django-url-filter
- For profile's placeholder I used template language
- Used multi-setting modules
- Used class based views