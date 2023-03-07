import pymysql


def get_conn():
    return pymysql.connect(host='db',
                           user='root',
                           password='root',
                           port=3306,
                           database='test',
                           charset='utf8')


def query_data(sql):
    conn = get_conn()
    try:
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(sql)
        return cursor.fetchall()
    finally:
        conn.close()


def inser_or_update__data(sql):
    conn = get_conn()
    try:
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
    finally:
        conn.close()
