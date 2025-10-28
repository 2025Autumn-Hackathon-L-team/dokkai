from flask import Flask,render_template,redirect,url_for,session,request,flash
from datetime import timedelta
import hashlib
import uuid
import re
import os

from models import User #, Bookroom

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', uuid.uuid4().hex)
#app.permanent_session_lifetime = timedelta(days=SESSION_DAYS)

#ルートページのリダイレクト
@app.route('/')
def index():
    id = session.get('id')
    if id is None:
        return redirect(url_for('login_view'))
    return f'パブリックチャンネルの表示'
    # TODO: ページができたら追加 redirect(url_for('public_channels_view'))

#サインアップページの表示
@app.route('/signup')
def signup_view():
    return render_template('auth/signup.html')

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
    return f'{name}作るの成功'#redirect(url_for('public_channels_view'))

#ログインページの表示
@app.route('/login')
def login_view():
    return render_template('auth/login.html')

#ログイン処理
@app.route('/login', methods=['POST'])
def login_process():
    email = request.form.get('email')
    password = request.form.get('password')
    if email=='' and password=='':
        flash('ログインできませんでした')
        flash('メールアドレスとパスワードを入力してください')
    elif password=='':
        flash('ログインできませんでした')
        flash('パスワードを入力してください')
    elif email=='':
        flash('ログインできませんでした')
        flash('メールアドレスを入力してください')
    else:
        user = User.find_by_email(email)
        if user is None:
            flash('ログインできませんでした')
            flash('このユーザーは存在しません')
        else:
            # パスワードの一致チェック
            hashPassword = hashlib.sha256(password.encode('utf-8')).hexdigest()
            user = User.find_by_email(email)
            if user is None:  #ログイン失敗
                flash('ログインできませんでした')
                flash('メールアドレスかパスワードが間違っています')
            else:
                user['password'] == hashPassword #trueならログイン
                print(f'{user}でログインできました') #ログインできているかチェック、後ほど削除ß
                redirect(url_for('public_channels_view'))
    # TODO バリデーションエラーでauth/login.htmlnに戻る時、フォームに入力した値を残したい
    return redirect(url_for('login_view'))#render_template('auth/login.html',email=email,password=password)   

#ログアウト処理
@app.route('/logout',methods = ['POST'])
def logout():
    return redirect(url_for('login_view'))


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)