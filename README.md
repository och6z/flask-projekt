```
$ git clone https://github.com/jrajmundtest/flask-projekt.git
$ cd flask-projekt
$ python3 -m venv venv
$ source venv/bin/activate
(venv)$ pip install -U pip
(venv)$ pip install wheel eggs

(venv)$ pip install autopep8 flake8 jedi yapf
(venv)$ pip install -r requirements

(venv)$ mysql -uroot -p
mysql> CREATE USER 'flask_admin'@'localhost' IDENTIFIED BY 'flask_pass';
mysql> CREATE DATABASE flask_db;
mysql> GRANT ALL PRIVILEGES ON flask_db.* TO 'flask_admin'@'localhost';
mysql> EXIT

(venv)$ export FLASK_APP=run.py
(venv)$ export FLASK_ENV=development

(venv)$ flask db init
(venv)$ flask db migrate
(venv)$ flask db upgrade

(venv)$ mysql -uflask_admin -p
mysql> DROP TABLE flask_db.alembic_version;
mysql> EXIT

(venv)$ flask shell
>>> from app.models import User
>>> from app import db
>>> admin=User(email="admin@admin.com",username="superadmin",password="superpass",is_admin=True)
>>> db.session.add(admin)
>>> db.session.commit()
>>> exit()

(venv)$ flask run

```



