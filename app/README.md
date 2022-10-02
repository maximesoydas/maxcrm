# install the application
1. install postgresql
1. install pgadmin 4
1. setup the database name and password as follow :
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'epic_eventsDB',
        'USER': 'postgres',
        'PASSWORD': 'admin',
1. download the repository
1. open terminal and cd to: maxcrm/Scripts 
1. type in : activate 
1. pip install -r requirements.txt
1. cd app
1. python manage createsuperuser
1. create admin 
1. pyhon manage runserver

# use application
you will need to login with your superuser/admin to create support and sales Users.

once the app is running you can either use it through the localhost:8000/admin portal
or 
using the postman application to consume the APIs 

