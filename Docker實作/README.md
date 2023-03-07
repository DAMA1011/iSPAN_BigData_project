# Docker實作

## 內容：
### 1. Nginx-Django-Postgresql
Main project structure:
```
.
├── compose.yml
├── django
│   ├── Dockerfile
│   ├── requirements.txt
│   └── server.py
├── nginx
│   └── nginx.conf
└── postgresql
    └── nginx.conf
```

.
├── compose.yml
├── flask
│   ├── Dockerfile
│   ├── __pycache__
│   │   └── db.cpython-310.pyc
│   ├── app.ini
│   ├── db.py
│   ├── icon.png
│   ├── icon2.png
│   ├── main.py
│   ├── requirements.txt
│   ├── static
│   ├── taipei-region.json
│   └── templates
│
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
### 2. Nginx-Flask-Mysql
