from flask import abort
import pymysql
from util.DB import DB

db_pool = DB.init_db_pool()


# ブックルームクラス
class Bookroom:
    @classmethod
    def find_by_name(cls, bookroom_name):
       conn = db_pool.get_conn()
       try:
           with conn.cursor() as cur:
               sql = "SELECT * FROM bookrooms WHERE name=%s;"
               cur.execute(sql, (bookroom_name,))
               channel = cur.fetchone()
               return channel
       except pymysql.Error as e:
           print(f'エラーが発生しています：{e}')
           abort(500)
       finally:
           db_pool.release(conn)


    @classmethod
    def get_public_bookrooms(cls):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "SELECT * FROM bookrooms WHERE is_public=TRUE;"
                cur.execute(sql)
                public_bookrooms = cur.fetchall()
                return public_bookrooms
        except pymysql.Error as e:
            print(f"エラーが発生しています:{e}")
            abort(500)
        finally:
            db_pool.release(conn)
    
    @classmethod
    def create(cls, user_id, name, description, is_public):
        conn = db_pool.get_conn()
        try:
           with conn.cursor() as cur:
            sql = "INSERT INTO bookrooms (user_id, name, description, is_public) VALUES(%s, %s, %s, %s)"
            cur.execute(sql,(user_id, name, description, is_public,))
            conn.commit()
        except pymysql.Error as e:
           print(f'エラーが発生しています：{e}')
           abort(500)
        finally:
           db_pool.release(conn)


