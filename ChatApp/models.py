from flask import abort
import pymysql
from flask_paginate import Pagination, get_page_parameter
from util.DB import DB

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
        conn = db_pool.get_conn()
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

############################メッセージ関係（ここから）############################
class Message:
    @classmethod
    def create(cls, user_id, bookroom_id, message):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "INSERT INTO messages(user_id, bookroom_id, content) VALUES(%s, %s, %s)"
                cur.execute(sql, (user_id, bookroom_id, message,))
                conn.commit()
        except pymysql.Error as e:
            print(f'エラーが発生しています:) {e}')
            abort(500)
        finally:
            db_pool.release(conn)

    @classmethod
    def get_all(cls, bookroom_id):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = """
                    SELECT m.id, u.id, u.name, m.content 
                    FROM messages AS m 
                    INNER JOIN users AS u ON m.user_id = u.id 
                    WHERE m.bookroom_id = %s 
                    ORDER BY m.id ASC;
                """
                cur.execute(sql, (bookroom_id,))
                messages = cur.fetchall()
                return messages
        except pymysql.Error as e:
            print(f'エラーが発生しています：{e}')
            abort(500)
        finally:
            db_pool.release(conn)

    
    @classmethod
    def delete(cls, message_id):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "DELETE FROM messages WHERE id=%s;"
                cur.execute(sql, (message_id,))
                conn.commit()
        except pymysql.Error as e:
            print(f'エラーが発生しています：{e}')
            abort(500)
        finally:
            db_pool.release(conn)

############################メッセージ関係（ここまで）############################
