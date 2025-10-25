from flask import Flask, request, redirect, render_template, url_for

from models import Bookroom


app = Flask(__name__)

# 開発の確認のために使用
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.jinja_env.auto_reload = True
app.jinja_env.cache = {} 

# ブックルームの一覧表示
@app.route("/public_bookrooms", methods=["GET"])
def public_channels_view():
    # userデータを格納
    # ユーザデータが今はないのでスキップ

    # publicなブックルームのみ取得
    bookrooms = Bookroom.get_public_bookrooms()
    return render_template("test/bookroom.html", bookrooms=bookrooms, is_public=True)


# ブックルームの作成
# @app.route('/public_bookrooms', methods=['POST'])
# def create_bookroom():
#    bookroom_name = request.form['bookroomname']
#    db = get_db()
#    if not book


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
