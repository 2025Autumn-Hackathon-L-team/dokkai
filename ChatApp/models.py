from flask import abort
import pymysql
from util.DB import DB

db_pool = DB.init_db_pool()

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
                sql = "SELECT email FROM users WHERE email=%s"
                cur.execute(sql,(email,))
                user = cur.fetchone()
            return user
        except pymysql.Error as e:
            print(f'エラーが発生しています:{e}')
            abort(500)
        finally:
            db_pool.release(conn)

############################ブックルーム関係（ここから）############################
# ブックルームクラス
class Bookroom:
    @classmethod
    def find_by_bookroom_name(cls, bookroom_name):
       conn = db_pool.get_conn()
       try:
           with conn.cursor() as cur:
               sql = "SELECT * FROM bookrooms WHERE name=%s;"
               cur.execute(sql, (bookroom_name))
               bookroom = cur.fetchone()
               return bookroom
       except pymysql.Error as e:
           print(f'エラーが発生しています：{e}')
           abort(500)
       finally:
           db_pool.release(conn)
    
    @classmethod
    def find_by_bookroom_id(cls, bookroom_id):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "SELECT * FROM bookrooms WHERE id=%s;"
                cur.execute(sql, (bookroom_id))
                bookroom = cur.fetchone()
                return bookroom
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
    
        def get_private_bookrooms(cls):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "SELECT * FROM bookrooms WHERE is_public=FALSE;"
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
    
    @classmethod
    def update(cls, bookroom_id, name, description):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "UPDATE bookrooms SET name=%s, description=%s WHERE id=%s;"
                cur.execute(sql, (name, description, bookroom_id))
                conn.commit()
        except pymysql.Error as e:
            print(f'エラーが発生しています：{e}')
            abort(500)
        finally:
            db_pool.release(conn)
    
    @classmethod
    def delete(cls, bookroom_id):
        conn = db.pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "DELETE FROM bookrooms WHERE id=%s;"
                cur.execute(sql, (bookroom_id))
                conn.commit()
        except pymysql.Error as e:
            print(f'エラーが発生しています：{e}')
            abort(500)
        finally:
            db_pool.release(conn)
    




############################ブックルーム関係（ここまで）############################

