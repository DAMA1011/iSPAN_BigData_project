# Docker實作

## 內容：
### 1. Nginx-Django-Postgresql
Main project structure:
```
.
├── compose.yml
├── django
│   ├── Dockerfile
│   ├── entrypoint.sh
│   ├── final
│   │   ├── __init__.py
│   │   ├── asgi.py
│   │   ├── db.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── views.py
│   │   └── wsgi.py
│   ├── manage.py
│   ├── requirements.txt
│   ├── statics
│   └── templates
├── postgresql
│   ├── sql_data
│   │   ├── restaurant_0114_final.csv
│   │   └── spot_0114_final.csv
│   └── sql_init
└── nginx
    ├── Dockerfile
    └── nginx.conf
```
   
### 2. Nginx-Flask-Mysql
Main project structure:
```
.
├── compose.yml
├── flask
│   ├── Dockerfile
│   ├── app.ini
│   ├── main.py
│   ├── requirements.txt
│   ├── static
│   └── templates
├── mysql
│   ├── sql_conf
│   │   └── my.cnf
│   ├── sql_data
│   │   ├── restaurant_0114_final.csv
│   │   └── spot_0114_final.csv
│   └── sql_init
│       └── test.sql
└── nginx
    ├── Dockerfile
    └── nginx.conf
```   
