# Docker實作

## 內容：
### 1. Nginx-Django-Postgresql
Main project structure:

 
    
### 2. Nginx-Flask-Mysql
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
