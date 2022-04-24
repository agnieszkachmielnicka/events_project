# Events project

# Description
The events project is an app created for recruitment purposes. It is a simple django app. 
The users can sign up, log in, create events and join the events already created. 

# How to install and run the project

git clone https://github.com/agnieszkachmielnicka/events_project.git

cd events_project

pip install -r requirements.txt

python manage.py migrate

python manage.py runserver

go to http://localhost:8000/

Enjoy :)

# Note
For development purposes the app is using django.core.mail.backends.console.EmailBackend it means that every email will appear in the console (Confirmation email with activation link).
