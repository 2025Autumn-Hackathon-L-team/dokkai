from flask import Flask , request, render_template,flash
import uuid
import os

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', uuid.uuid4().hex)

@app.route('/')
def test():
    flash('フラッシュメッセージです')
    return render_template('auth/signup.html')

if __name__ == '__main__':
    # run()メソッドの引数に port=5001 を追加します
    app.run(host='0.0.0.0', port=5001, debug=True)