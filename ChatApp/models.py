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
    def find_by_public_bookroom_name(cls, bookroom_name):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "SELECT * FROM bookrooms WHERE name=%s AND is_public=TRUE"
                cur.execute(sql, (bookroom_name,))
                bookroom = cur.fetchone()
                return bookroom
        except pymysql.Error as e:
            print(f"エラーが発生しています：{e}")
            abort(500)
        finally:
            db_pool.release(conn)

    # private bookroomかつ同じユーザで同じチャンネル名がないかを確認
    @classmethod
    def find_by_private_bookroom_name(cls, bookroom_name, user_id):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "SELECT * FROM bookrooms WHERE name=%s AND is_public=FALSE AND user_id=%s"
                cur.execute(sql, (bookroom_name, user_id))
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
                sql = "SELECT * FROM bookrooms WHERE is_public=TRUE ORDER BY updated_at DESC;"
                cur.execute(sql)
                public_bookrooms = cur.fetchall()
                return public_bookrooms
        except pymysql.Error as e:
            print(f"エラーが発生しています:{e}")
            abort(500)
        finally:
            db_pool.release(conn)
    
    @classmethod  # <-- @classmethod を追加
    def get_private_bookrooms(cls, user_id):  # <-- user_idを引数に追加
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "SELECT * FROM bookrooms WHERE user_id=%s AND is_public=FALSE ORDER BY updated_at DESC;"
                cur.execute(sql, (user_id,))
                private_bookrooms = cur.fetchall()
                return private_bookrooms
        except pymysql.Error as e:
            print(f"エラーが発生しています:{e}")
            abort(500)
        finally:
            db_pool.release(conn)
    
    @classmethod
    def get_public_bookrooms_include_keyword(cls, keyword):
        keyword_wild = f"%{keyword}%"
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = ("SELECT id FROM bookrooms WHERE is_public=TRUE "
                      "AND (name LIKE %s OR description LIKE %s) ORDER BY updated_at DESC;")
                cur.execute(sql, (keyword_wild,keyword_wild,))
                private_bookrooms = cur.fetchall()
                return private_bookrooms
        except pymysql.Error as e:
            print(f"エラーが発生しています:{e}")
            abort(500)
        finally:
            db_pool.release(conn)
    
    @classmethod
    def get_private_bookrooms_include_keyword(cls, keyword, user_id):
        keyword_wild = f"%{keyword}%"
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = ("SELECT id FROM bookrooms WHERE is_public=FALSE AND user_id=%s "
                      "AND (name LIKE %s OR description LIKE %s) ORDER BY updated_at DESC;")
                cur.execute(sql, (user_id,keyword_wild,keyword_wild,))
                private_bookrooms = cur.fetchall()
                return private_bookrooms
        except pymysql.Error as e:
            print(f"エラーが発生しています:{e}")
            abort(500)
        finally:
            db_pool.release(conn)

    @classmethod
    def get_public_bookrooms_from_bookroomid(cls, bookroom_ids):
        if len(bookroom_ids) == 0:
                    return []
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "SELECT * FROM bookrooms WHERE is_public=TRUE AND id IN %s ORDER BY updated_at DESC;"
                cur.execute(sql, (tuple(bookroom_ids),))
                public_bookrooms = cur.fetchall()
                return public_bookrooms
        except pymysql.Error as e:
            print(f"エラーが発生しています:{e}")
            abort(500)
        finally:
            db_pool.release(conn)
    
    @classmethod
    def get_private_bookrooms_from_bookroomid(cls, bookroom_ids, user_id):
        if len(bookroom_ids) == 0:
                    return []
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "SELECT * FROM bookrooms WHERE is_public=FALSE AND user_id=%s AND id IN %s ORDER BY updated_at DESC;"
                cur.execute(sql, (user_id, tuple(bookroom_ids),))
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
                cur.execute(
                    sql,
                    (
                        name,
                        description,
                        bookroom_id,
                    ),
                )
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
        except pymysql.Error as e:
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
                    sql = "INSERT INTO bookroom_tag(bookroom_id, tag_id) VALUES(%s, %s);"
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

    @classmethod
    def get_bookroom_tag_tables(cls):
        conn = db_pool.get_conn()
        try:
            with conn.cursor(pymysql.cursors.DictCursor) as cur:
                sql = (
                    "SELECT bt.bookroom_id, t.name "
                    "FROM bookroom_tag AS bt "
                    "INNER JOIN tags AS t ON bt.tag_id = t.id "
                    "ORDER BY bt.bookroom_id, bt.id;"
                )
                cur.execute(sql)
                conn.commit()
        except pymysql.Error as e:
            print(f"エラーが発生しています：{e}")
            abort(500)
        finally:
            db_pool.release(conn)

        bookroom_tag_tables = cur.fetchall()
        return bookroom_tag_tables

    @classmethod
    def get_selected_tags_from_bookroomid(cls, bookroom_id):
        conn = db_pool.get_conn()
        try:
            with conn.cursor(pymysql.cursors.DictCursor) as cur:
                sql = (
                    "SELECT t.id, t.name "
                    "FROM bookroom_tag AS bt "
                    "INNER JOIN tags AS t ON bt.tag_id = t.id "
                    "WHERE bookroom_id=%s"
                    "ORDER BY bt.bookroom_id, bt.id;"
                )
                cur.execute(sql, (bookroom_id,))
                conn.commit()
                selected_tag_id = cur.fetchall()
                return selected_tag_id
        except pymysql.Error as e:
            print(f"エラーが発生しています：{e}")
            abort(500)
        finally:
            db_pool.release(conn)

    @classmethod
    def delete_bookroomtag_by_bookroomid(cls, bookroom_id):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = ("DELETE FROM bookroom_tag WHERE bookroom_id=%s;")
                cur.execute(sql, (bookroom_id,))
                conn.commit()
        except pymysql.Error as e:
            print(f"エラーが発生しています：{e}")
            abort(500)
        finally:
            db_pool.release(conn)

    # 検索機能の使用　tagidからbookroomidを探す
    @classmethod
    def get_public_bookroomids_from_tagids(cls, tag_ids):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = ("SELECT bookroom_id FROM bookroom_tag "
                "WHERE tag_id IN %s ORDER BY bookroom_id;")
                cur.execute(sql, (tuple(tag_ids),))
                bookroom_ids = cur.fetchall()
                if len(bookroom_ids) == 0:
                    return []
                return bookroom_ids
        except pymysql.Error as e:
            print(f"エラーが発生しています：{e}")
            abort(500)
        finally:
            db_pool.release(conn)

    @classmethod
    def get_private_bookroomids_from_tagids(cls, tag_ids, user_id):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = ("SELECT bt.bookroom_id "
                "FROM bookroom_tag AS bt INNER JOIN bookrooms AS b ON bt.bookroom_id = b.id "
                "WHERE tag_id IN %s AND b.is_public=FALSE AND b.user_id=%s "
                "ORDER BY bt.bookroom_id;")
                cur.execute(sql, (tuple(tag_ids),user_id,))
                bookroom_ids = cur.fetchall()
                if len(bookroom_ids) == 0:
                    return []
                return bookroom_ids
        except pymysql.Error as e:
            print(f"エラーが発生しています：{e}")
            abort(500)
        finally:
            db_pool.release(conn)

#############ヒストリー#############
# bookroom_idだけの集合を作る。チャンネル名は重複しない設定。
class History:
    @classmethod
    def history(cls, user_id):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                # sqlの構成：SELECT 取得したいカラム FROM bookrooms INNER JOIN bookroom_idが入ったmessageとreaction_messageの投稿時間がわかる表（WHEREで特定のユーザーが投稿したものを指定）ON bookroom_idで紐付け ORDER BY 更新順
                sql = """
                SELECT 
                    b.id,
                    b.name,
                    b.description,
                    b.is_public,
                    hist.last_updated_at -- ユーザーが最後にメッセージかリアクションを投稿した時間
                FROM bookrooms AS b
                -- ユーザーがこの bookroom で最後に行った操作の時間のsub_tableをINNER JOINする
                INNER JOIN (
                    SELECT 
                        bookroom_id,
                        MAX(updated_at) AS last_updated_at
                    FROM (
                        -- T_messagesから取得
                        SELECT m.bookroom_id,m.updated_at
                        FROM messages AS m
                        WHERE m.user_id = %s
                        UNION ALL
                        -- T_message_reactionsから取得
                        SELECT m2.bookroom_id,mr.created_at AS updated_at -- 別名を付けて、カラム名を合わせる
                        FROM message_reaction AS mr
                        JOIN messages AS m2 -- UNIONは同じカラム名だとエラーになるから、messageの別名はm2とする
                        ON mr.message_id = m2.id
                        WHERE mr.user_id = %s
                    ) AS sub_table -- 別名つけないとエラーになるのでつける
                    GROUP BY bookroom_id -- 複数回同じチャンネルに投稿していた場合、すべての場合が取得されているので、bookroom_idにグループ化する。
                ) AS hist
                ON b.id = hist.bookroom_id
                WHERE b.is_public=1 -- publicのみ表示
                ORDER BY hist.last_updated_at DESC; -- 最新投稿順に並び替え
                """
                cur.execute(sql, (user_id, user_id))
                history = cur.fetchall()
                return history
        except pymysql.Error as e:
            print(f"エラーが発生しています:) {e}")
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
                    m.content AS message,
                    m.created_at,
                    COALESCE(i.icon_image, '/static/img/icons/icon2_rabbit.png') AS icon_image
                    FROM messages AS m 
                    INNER JOIN users AS u ON m.user_id = u.id 
                    LEFT JOIN icons AS i ON u.iconid = i.id
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
    # TODO M_iconsテーブルができたら、iconidでなく画像のパスを返す形に変える
    @classmethod
    def icon_view(cls, user_id):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = """
                SELECT icons.icon_image 
                FROM users
                LEFT JOIN icons ON users.iconid = icons.id
                WHERE users.id = %s
                """
                cur.execute(sql, (user_id,))
                result = cur.fetchone()

                if result is None or result["icon_image"] is None:
                    return "/static/img/icons/icon2_rabbit.png"
                
                return result["icon_image"]

        except pymysql.Error as e:
            print(f"エラーが発生しています : {e}")
            abort(500)

        finally:
            db_pool.release(conn)

    # nameの表示
    @classmethod
    def name_view(cls, user_id):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "SELECT name FROM users where id = %s"
                cur.execute(sql, (user_id,))
                user = cur.fetchone()
                return user["name"]
        except pymysql.Error as e:
            print(f"エラーが発生しています：{e}")
            abort(500)
        finally:
            db_pool.release(conn)

    # emailの表示
    @classmethod
    def email_view(cls, user_id):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "SELECT email FROM users where id = %s"
                cur.execute(sql, (user_id,))
                user = cur.fetchone()
                return user["email"]
        except pymysql.Error as e:
            print(f"エラーが発生しています：{e}")
            abort(500)
        finally:
            db_pool.release(conn)

    # アイコンの変更
    @classmethod
    def icon_update(cls, iconid, user_id):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "UPDATE users SET iconid=%s WHERE id=%s"

                rows = cur.execute(
                    sql,
                    (
                        iconid,
                        user_id,
                    ),
                )
                # 更新結果チェック
                if rows == 0:
                    print("対象ユーザーが見つかりません")
            conn.commit()
        except pymysql.Error as e:
            print(f"エラーが発生しています：{e}")
            abort(500)
        finally:
            db_pool.release(conn)

    # nameの変更
    @classmethod
    def name_update(cls, name, user_id):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "UPDATE users SET name=%s WHERE id=%s;"
                cur.execute(
                    sql,
                    (
                        name,
                        user_id,
                    ),
                )
                conn.commit()
        except pymysql.Error as e:
            print(f"エラーが発生しています：{e}")
            abort(500)
        finally:
            db_pool.release(conn)

    # emailの変更
    @classmethod
    def email_update(cls, email, user_id):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "UPDATE users SET email=%s WHERE id=%s;"
                cur.execute(
                    sql,
                    (
                        email,
                        user_id,
                    ),
                )
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
############################アイコン画面関係（ここから）###########################
class Icon:
    @classmethod
    def get_all(cls):
        conn = db_pool.get_conn()
        try:
            with conn.cursor(pymysql.cursors.DictCursor) as cur:
                sql = "SELECT * FROM icons ORDER BY id;"
                cur.execute(sql)
                icons = cur.fetchall()
                return icons
        except pymysql.Error as e:
            print(f"エラーが発生しています:{e}")
            abort(500)
        finally:
            db_pool.release(conn)

    @classmethod
    def find_id(cls, icon_id):
        conn = db_pool.get_conn()
        try:
            with conn.cursor(pymysql.cursors.DictCursor) as cur:
                sql = "SELECT * FROM icons WHERE id=%s;"
                cur.execute(sql, (icon_id,))
                icon = cur.fetchone()
                return icon
        except pymysql.Error as e:
            print(f"エラーが発生しています:{e}")
            abort(500)
        finally:
            db_pool.release(conn)
