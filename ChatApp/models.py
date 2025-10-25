from flask import abort
import pymysql
from util.DB import DB

db_pool = DB.init_db_pool()


# ブックルームクラス
class Bookroom:
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
