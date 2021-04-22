import pymysql

conn = pymysql.connect(
    host='bankdb.cing882ce6yu.us-west-1.rds.amazonaws.com',
    port=3306,
    user='admin',
    password='cmpe202bank',
    db='bank',

)


def data_ins(first_name, last_name, email, password):
    cur = conn.cursor()
    cur.execute("INSERT INTO user (first_name, last_name, email, password) VALUES (%s, %s, %s, %s)",
                (first_name, last_name, email, password))
    conn.commit()


def print_data():
    cur = conn.cursor()
    cur.execute("SELECT * FROM user")
    res = cur.fetchall()
    return res
