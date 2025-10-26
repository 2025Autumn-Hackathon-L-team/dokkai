from flask import Flask,render_template,redirect,url_for,session,request

app = Flask(__name__)
#app.secret_key = 'your_secret_key'

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
    email =request.form.get('email')
    return f'{name}と{email}を表示'

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