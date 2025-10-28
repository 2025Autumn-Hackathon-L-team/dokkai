from flask import abort
import pymysql
from util.DB import DB


#初期起動時にコネクションプール作成して接続を確立
db_pool = DB.init_db_pool()

class User:
    @classmethod
    def create(cls,id,name,email,password):  
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "INSERT INTO users (id,name,email,password) VALUES (%s,%s,%s,%s);"
                cur.execute(sql,(id,name,email,password,))
                conn.commit()
        except pymysql.Error as e:
            print(f'エラーが発生しています:{e}')
            abort(500)
        finally:
            db_pool.release(conn)

    @classmethod
    def find_by_email(cls,email):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "SELECT * FROM users WHERE email=%s"
                cur.execute(sql,(email,))
                user = cur.fetchone()
            return user
        except pymysql.Error as e:
            print(f'エラーが発生しています:{e}')
            abort(500)
        finally:
            db_pool.release(conn)