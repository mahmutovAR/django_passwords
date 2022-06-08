# Web Password Manager

The application "Avast Passwords" exports data with passwords in the file with JSON format.
'Web Password Manager' is website for uploading JSON files and operating with password databases.

## To run website:
`python manage.py runserver` and open `http://127.0.0.1:8000/`


### 'Web Password Manager' has the following features:
* uploading JSON file with passwords
* loading passwords from uploaded files
* displaying passwords by category (Cards, Logins, Notes)
* password searching and result by category

## Script runs on Python 3.9 with next modules:
* `datetime`, `json`, `os`, `pathlib` (standard libraries)
* `django` (3rd party libraries)