from flask import Flask,render_template,redirect,url_for,session,request
from datetime import timedelta
import hashlib
import uuid
import re
import os

from models import User

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', uuid.uuid4().hex)
#app.permanent_session_lifetime = timedelta(days=SESSION_DAYS)

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


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)