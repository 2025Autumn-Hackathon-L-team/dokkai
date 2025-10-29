from flask import Flask,render_template,redirect,url_for,session,request
from datetime import timedelta
import hashlib
import uuid
import re
import os

from models import User, Bookroom

# user idを仮で作成するためにランダムを作成 ここから
TEST_USER_ID = "970af84c-dd40-47ff-af23-282b72b7cca8"
# user idを仮で作成するためにランダムを作成 ここまで


app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', uuid.uuid4().hex)
#app.permanent_session_lifetime = timedelta(days=SESSION_DAYS)

# 開発中の確認のために使用
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.jinja_env.auto_reload = True
app.jinja_env.cache = {}

#ルートページのリダイレクト
@app.route('/')
def index():
    #if uid is None:
    #    return redirect(url_for('login_view'))
    #return redirect(url_for('channels_view'))
    return 'Hello World'

#サインアップページの表示
@app.route('/signup')
def signup_view():
    return 'signupの表示'

#サインアップ処理
@app.route('/signup', methods=['POST'])
def signup_process():
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')
    passwordConfirmation = request.form.get('password-confirmation')
    id = uuid.uuid4()
    password = hashlib.sha256(password.encode('utf-8')).hexdigest()
    registered_user = User.find_by_email(email)
    User.create(id,name,email,password)
    UserId = str(id)
    session['id'] = UserId
    return f'{name}作るの成功'#redirect(url_for('channels_view'))

#ログインページの表示
@app.route('/login')
def login_view():
    return render_template('auth/login.html')

#ログイン処理
@app.route('/login', methods=['POST'])
def login_process():
    email = request.form.get('email')
    password = request.form.get('password')
    return f'{email}と{password}を表示'

#ログアウト処理
@app.route('/logout',methods = ['POST'])
def logout():
    return redirect(url_for('login_view'))


############################ブックルーム関係（ここから）############################

###########################
#  パブリックブックルーム   #
###########################

# パブリックブックルームの一覧表示

@app.route("/public_bookrooms", methods=["GET"])
def public_channels_view():
    # publicなブックルームのみ取得
    bookrooms = Bookroom.get_public_bookrooms()
    return render_template("test/bookroom.html", bookrooms=bookrooms, is_public=True)

# パブリックブックルームの作成
@app.route('/public_bookrooms', methods=['POST'])
def create_public_bookroom():
    # user_idは仮の値を使用（init.sqlでこのユーザーは作成済み）
    bookroom_name = request.form.get('bookroom_name')
    bookroom = Bookroom.find_by_bookroom_name(bookroom_name)
    if bookroom == None:
        bookroom_description = request.form.get('bookroom_description')      
        # セッション未実装なので仮値
        user_id=session.get('user_id',TEST_USER_ID)
        Bookroom.create(
            user_id=user_id,
            name=bookroom_name,
            description=bookroom_description,
            is_public=True
        )
        return redirect(url_for('public_channels_view'))
    else:
        error = '既に同じ名前のブックルームが存在しています。'
        return render_template('test/error.html', error_message=error)

# パブリックブックルームの更新
@app.route('/public_bookrooms/update/<bookroom_id>', methods=['POST'])
def update_public_bookroom(bookroom_id):
    # user_id = session.get('user_id')
    # セッションが未実装なため、仮値を入れる
    user_id = session.get('user_id', TEST_USER_ID)

    if user_id is None:
        return redirect(url_for('login_view'))
    
    bookroom = Bookroom.find_by_bookroom_id(bookroom_id)
    if bookroom['user_id'] != user_id:
        flash('ブックルーム作成者のみ編集可能です')
    
    bookroom_name = request.form.get('bookroom_name')
    bookroom_description = request.form.get('bookroom_description')
    Bookroom.update(
        bookroom_id=bookroom_id,
        name=bookroom_name,
        description=bookroom_description
    )
    return redirect(url_for("public_channels_view"))

# パブリックブックルームの削除
@app.route('/public_bookrooms/delete/<bookroom_id>', methods=['POST'])
def delete_public_bookroom(bookroom_id):
    # user_id = session.get('user_id')
    # セッションが未実装なため、仮値を入れる
    user_id = session.get('user_id', TEST_USER_ID)
    if user_id is None:
        return redirect(url_for('login_view'))
    
    bookroom = Bookroom.find_by_bookroom_id(bookroom_id)
    if bookroom['user_id'] != user_id:
        flash('ブックルーム作成者のみ削除可能です')
    else:
        Bookroom.delete(bookroom_id)
    return redirect(url_for('public_channels_view'))

###########################
# プライベートブックルーム  #
###########################



############################ブックルーム関係（ここまで）############################

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)

