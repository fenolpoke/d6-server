# d6-server
d6-news Server code

## Build Setup

```bash
# install dependencies
$ pip install -r requirements.txt
$ python manage.py db init
$ python manage.py db migrate

# optional: seed the database
$ python manage.py seed

# serve at localhost:5000
$ python deploy.py

```