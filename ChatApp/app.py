from flask import Flask, request, redirect, render_template, url_for

# 仮のuser_id作成のためランダムな文字列発生のため使用
import random, string

from models import Bookroom

# 仮のuser_id作成のためランダムな文字列発生のため使用
def randomname(n):
   randlst = [random.choice(string.ascii_letters + string.digits) for i in range(n)]
   return ''.join(randlst)

app = Flask(__name__)

# 開発の確認のために使用
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.jinja_env.auto_reload = True
app.jinja_env.cache = {} 

# ブックルームの一覧表示
@app.route("/public_bookrooms", methods=["GET"])
def public_channels_view():
    # publicなブックルームのみ取得
    bookrooms = Bookroom.get_public_bookrooms()
    return render_template("test/bookroom.html", bookrooms=bookrooms, is_public=True)

# ブックルームの作成
@app.route('/public_bookrooms', methods=['POST'])
def create_public_bookroom():
    # userデータを格納
    # ユーザデータが今はないのでスキップ
   bookroom_name = request.form.get('bookroom_name')
   bookroom = Bookroom.find_by_name(bookroom_name)
   if bookroom == None:
      bookroom_description = request.form.get('bookroom_description')
      Bookroom.create(user_id = randomname(32), name = bookroom_name, description = bookroom_description, is_public = True)
      return redirect(url_for('public_channels_view'))
   else:
       error = '既に同じ名前のブックルームが存在しています。'
       return render_template('test/error.html', error_message=error)
   

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
