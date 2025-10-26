import os
import pymysql
from pymysqlpool.pool import Pool


class DB:
    @classmethod
    def init_db_pool(cls):  
        pool = Pool(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            datebase=os.getenv('DB_DATABASE'),
            max_size=5,
            charaset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor
        )
        pool.init()
        return pool
