from flask import abort
import pymysql
from util.DB import DB

db_pool = DB.init_db_pool()


class User:
    @classmethod
    def create(cls, id, name, email, password):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "INSERT INTO users (id,name,email,password) VALUES (%s,%s,%s,%s);"
                cur.execute(
                    sql,
                    (
                        id,
                        name,
                        email,
                        password,
                    ),
                )
                conn.commit()
        except pymysql.Error as e:
            print(f"エラーが発生しています:{e}")
            abort(500)
        finally:
            db_pool.release(conn)

    @classmethod
    def find_by_email(cls, email):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "SELECT * FROM users WHERE email=%s"
                cur.execute(sql, (email,))
                user = cur.fetchone()
            return user
        except pymysql.Error as e:
            print(f"エラーが発生しています:{e}")
            abort(500)
        finally:
            db_pool.release(conn)

    @classmethod
    def find_by_name(cls, name):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "SELECT * FROM users WHERE name=%s"
                cur.execute(sql, (name,))
                user = cur.fetchone()
            return user
        except pymysql.Error as e:
            print(f"エラーが発生しています:{e}")
            abort(500)
        finally:
            db_pool.release(conn)


############################ブックルーム関係（ここから）############################
# ブックルームクラス
class Bookroom:
    @classmethod
    def find_by_bookroom_name(cls, bookroom_name, is_public=None):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "SELECT * FROM bookrooms WHERE name=%s AND is_public=%s"
                cur.execute(sql, (bookroom_name, is_public))
                bookroom = cur.fetchone()
                return bookroom
        except pymysql.Error as e:
            print(f"エラーが発生しています：{e}")
            abort(500)
        finally:
            db_pool.release(conn)

    @classmethod
    def find_by_bookroom_id(cls, bookroom_id):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "SELECT * FROM bookrooms WHERE id=%s;"
                cur.execute(sql, (bookroom_id,))
                bookroom = cur.fetchone()
                return bookroom
        except pymysql.Error as e:
            print(f"エラーが発生しています：{e}")
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
    
    @classmethod # <-- @classmethod を追加
    def get_private_bookrooms(cls, user_id):  #<-- user_idを引数に追加
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "SELECT * FROM bookrooms WHERE user_id=%s AND is_public=FALSE;" 
                cur.execute(sql, (user_id,))
                private_bookrooms = cur.fetchall() 
                return private_bookrooms
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
                cur.execute(
                    sql,
                    (
                        user_id,
                        name,
                        description,
                        is_public,
                    ),
                )
                conn.commit()
                bookroom_id = cur.lastrowid
                return bookroom_id
        except pymysql.Error as e:
            print(f"エラーが発生しています：{e}")
            abort(500)
        finally:
            db_pool.release(conn)

    @classmethod
    def update(cls, bookroom_id, name, description):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "UPDATE bookrooms SET name=%s, description=%s WHERE id=%s"
                cur.execute(sql, (name, description,))
                conn.commit()
        except pymysql.Error as e:
            print(f"エラーが発生しています：{e}")
            abort(500)
        finally:
            db_pool.release(conn)

    @classmethod
    def delete(cls, bookroom_id):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "DELETE FROM bookrooms WHERE id=%s"
                cur.execute(sql, (bookroom_id,))
                conn.commit()
        except pymysql.Error as e:
            print(f"エラーが発生しています：{e}")
            abort(500)
        finally:
            db_pool.release(conn)


############タグ############
class Tag:
    @classmethod
    def get_all_tags(cls):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "SELECT * FROM tags ORDER BY id;"
                cur.execute(sql)
                tags = cur.fetchall()
                return tags
        except pymysql.Eroor as e:
            print(f"エラーが発生しています：{e}")
            abort(500)
        finally:
            db_pool.release(conn)


############ブックルームタグ############
class BookroomTag:
    @classmethod
    def create(cls, bookroom_id, tag_ids):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                for tag_id in tag_ids:
                    sql = (
                        "INSERT INTO bookroom_tag(bookroom_id, tag_id) VALUES(%s, %s);"
                    )
                    cur.execute(
                        sql,
                        (
                            bookroom_id,
                            tag_id,
                        ),
                    )
                    conn.commit()
        except pymysql.Error as e:
            print(f"エラーが発生しています：{e}")
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
                cur.execute(
                    sql,
                    (
                        user_id,
                        bookroom_id,
                        message,
                    ),
                )
                conn.commit()
        except pymysql.Error as e:
            print(f"エラーが発生しています:) {e}")
            abort(500)
        finally:
            db_pool.release(conn)

    @classmethod
    def get_all(cls, bookroom_id):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = """
                    SELECT m.id, 
                    u.id AS user_id,
                    u.name AS user_name,
                    m.content AS message 
                    FROM messages AS m 
                    INNER JOIN users AS u ON m.user_id = u.id 
                    WHERE m.bookroom_id = %s 
                    ORDER BY m.id ASC;
                """
                cur.execute(sql, (bookroom_id,))
                messages = cur.fetchall()
                return messages
        except pymysql.Error as e:
            print(f"エラーが発生しています：{e}")
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
            print(f"エラーが発生しています：{e}")
            abort(500)
        finally:
            db_pool.release(conn)


############################メッセージ関係（ここまで）############################


############################プロフィール画面関係（ここから)############################
class Profile:
    # アイコンの表示
    @classmethod
    def icon_view(cls, iconid):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "SELECT iconid FROM users WHERE id=%s"
                cur.execute(sql, (iconid,))
                user_icon = cur.fetchone()
                return user_icon["iconid"]
        except pymysql.Error as e:
            print(f"エラーが発生しています：{e}")
            abort(500)
        finally:
            db_pool.release(conn)

    # アイコンの変更
    @classmethod
    def icon_update(cls,iconid,user_id):
        conn= db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "UPDATE users SET iconid=%s WHERE id=%s"
                cur.execute(sql,(iconid,user_id,))
                conn.commit()
        except pymysql.Error as e:
            print(f"エラーが発生しています：{e}")
            abort(500)
        finally:
            db_pool.release(conn)
    
    # nameの表示
    @classmethod
    def name_view(cls,user_id):
        conn =db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "SELECT name FROM users where id = %s"
                cur.execute(sql,(user_id,))
                user = cur.fetchone()
                return user["name"]
        except pymysql.Error as e:
            print(f"エラーが発生しています：{e}")
            abort(500)
        finally:
            db_pool.release(conn)

    # emailの表示
    @classmethod
    def email_view(cls,user_id):
        conn =db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "SELECT email FROM users where id = %s"
                cur.execute(sql,(user_id,))
                user = cur.fetchone()
                return user["email"]
        except pymysql.Error as e:
            print(f'エラーが発生しています：{e}')
            abort(500)
        finally:
            db_pool.release(conn)

    # nameとemailの変更
    @classmethod
    def name_email_update(cls,name,email,user_id):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "UPDATE users SET name=%s, email=%s WHERE id=%s;"
                cur.execute(sql,(name, email, user_id,))
                conn.commit()
        except pymysql.Error as e:
            print(f"エラーが発生しています：{e}")
            abort(500)
        finally:
            db_pool.release(conn)

    # TODO リアクションの実装が完了したら
    # リアクションの数を取得(T_reactuin_messagesのuser_idはリアクションをしたuser_id)
    @classmethod
    def get_reactions_count(cls, id):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "SELECT COUNT(SUB.id) FROM (SELECT r.id,r.messages_id,m.user_id FROM reaction_messages AS r LEFT JOIN messages AS m ON r.messages_id = m.id WHERE m.user_id=%s)AS SUB"
                cur.execute(sql, (id,))
                reactions_count = cur.fetchone()
                return reactions_count
        except pymysql.Error as e:
            print(f"エラーが発生しています：{e}")
            abort(500)
        finally:
            db_pool.release(conn)

    # 自分が投稿したメッセージの数を取得
    @classmethod
    def get_messages_count(cls, id):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "SELECT COUNT(id) FROM messages WHERE user_id=%s"
                cur.execute(sql, (id,))
                messages_count = cur.fetchone()
                return messages_count["COUNT(id)"]
        except pymysql.Error as e:
            print(f"エラーが発生しています:{e}")
            abort(500)
        finally:
            db_pool.release(conn)


############################プロフィール画面関係（ここまで）###########################
