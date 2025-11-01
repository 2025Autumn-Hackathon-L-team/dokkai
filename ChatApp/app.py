from flask import Flask, render_template, redirect, url_for, session, request, flash
from datetime import timedelta
import hashlib
import uuid
import re
import os

from models import User, Bookroom, Message

# user idを仮で作成するためにランダムを作成 ここから
TEST_USER_ID = "970af84c-dd40-47ff-af23-282b72b7cca8"
# user idを仮で作成するためにランダムを作成 ここまで

EMAIL_PATTERN = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
SESSION_DAYS = 30

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', uuid.uuid4().hex)
app.permanent_session_lifetime = timedelta(days=SESSION_DAYS)

# 開発中の確認のために使用
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.jinja_env.auto_reload = True
app.jinja_env.cache = {}


# ルートページのリダイレクト
@app.route("/")
def index():
    id = session.get("id")
    print (f'sessionは{id}です')
    if id is None:
        return redirect(url_for('login_view'))
    return redirect(url_for('public_channels_view'))


# サインアップページの表示
@app.route("/signup")
def signup_view():
    return render_template("auth/signup.html")


# サインアップ処理
@app.route("/signup", methods=["POST"])
def signup_process():
    name = request.form.get("name")
    email = request.form.get("email")
    password = request.form.get("password")
    passwordConfirmation = request.form.get("password_confirmation")
    if name == "" or email == "" or password == "" or passwordConfirmation == "":
        flash("入力されていないフォームがあります")
    elif password != passwordConfirmation:
        flash("パスワードが一致していません")
    elif re.fullmatch(EMAIL_PATTERN, email) is None:
        flash("有効なメールアドレスの形式ではありません")
    else:
        id = uuid.uuid4()
        password = hashlib.sha256(password.encode("utf-8")).hexdigest()
        registered_user = User.find_by_email(email) 
        if registered_user != None:
            flash("すでに登録済みです")
        else:
            User.create(id,name,email,password)
            UserId = str(id)
            session['id'] = UserId
            return redirect(url_for("public_channels_view"))
    # バリデーションエラーでsignup_processに戻る時、フォームに入力した値をauth/signup.htmlに返す
    return render_template("auth/signup.html",name=name,email=email,password=password)


# ログインページの表示
@app.route("/login")
def login_view():
    return render_template("auth/login.html")


# ログイン処理
@app.route("/login", methods=["POST"])
def login_process():
    email = request.form.get("email")
    password = request.form.get("password")
    if email == "" and password == "":
        flash("ログインできませんでした")
        flash("メールアドレスとパスワードを入力してください")
    elif password == "":
        flash("ログインできませんでした")
        flash("パスワードを入力してください")
    elif email == "":
        flash("ログインできませんでした")
        flash("メールアドレスを入力してください")
    else:
        user = User.find_by_email(email)
        if user is None:
            flash("ログインできませんでした")
            flash("このユーザーは存在しません")
        else:
            # パスワードの一致チェック
            hashPassword = hashlib.sha256(password.encode("utf-8")).hexdigest()
            user = User.find_by_email(email)
            # ログイン失敗、セキュリティのため、mailとpasswordのどちらかが間違っているようなメッセージを表示。
            if user["password"] != hashPassword:  
                flash("ログインできませんでした")
                flash("メールアドレスかパスワードが間違っています")
            else:
                print(f"{user}でログインできました") #ログインできているかチェック、後ほど削除
                return redirect(url_for("public_channels_view"))
    # バリデーションエラーでauth/login.htmlnに戻る時、フォームに入力した値をauth/login.htmlに返す
    return render_template("auth/login.html",email=email,password=password)


# ログアウト処理
@app.route("/logout", methods=["GET","POST"])
def logout():
    session.clear()
    return redirect(url_for("login_view"))


############################ブックルーム関係（ここから）############################

###########################
#  パブリックブックルーム   #
###########################

####################################################
#  ブックルームの作成者をチェックする関数
# 　作成者でなければFALSEを返す
# 　作成者であればTRUEを返す
####################################################


def is_bookroom_owner(user_id, bookroom_id):
    bookroom = Bookroom.find_by_bookroom_id(bookroom_id)
    if not bookroom:
        flash("ブックルームが存在しません")
        return False
    if bookroom["user_id"] != user_id:
        flash("ブックルーム作成者のみ操作可能です")
        return False
    return True


# パブリックブックルームの一覧表示
@app.route("/public_bookrooms", methods=["GET"])
def public_bookrooms_view():
    # 仮のユーザを設定
    session["user_id"] = TEST_USER_ID

    # publicなブックルームのみ取得
    bookrooms = Bookroom.get_public_bookrooms()
    #u_idをブックルームに渡す
    current_uid = session.get("user_id", TEST_USER_ID)
    return render_template("bookroom.html", bookrooms=bookrooms, is_public=True, uid=current_uid)

# パブリックブックルームの作成
@app.route("/public_bookrooms", methods=["POST"])
def create_public_bookroom():
    # user_idは仮の値を使用（init.sqlでこのユーザーは作成済み）
    bookroom_name = request.form.get("bookroom_name")
    bookroom = Bookroom.find_by_bookroom_name(bookroom_name)
    if bookroom == None:
        bookroom_description = request.form.get("bookroom_description")
        # セッション未実装なので仮値
        user_id = session.get("user_id", TEST_USER_ID)
        Bookroom.create(
            user_id=user_id,
            name=bookroom_name,
            description=bookroom_description,
            is_public=True,
        )

        return redirect(url_for("public_bookrooms_view"))
    else:
        error = "既に同じ名前のブックルームが存在しています。"
        return render_template("test/error.html", error_message=error)


# ブックルーム編集ページ表示
@app.route("/public_bookrooms/update/<bookroom_id>", methods=["GET"])
def show_public_bookroom(bookroom_id):
    user_id = session.get("user_id", TEST_USER_ID)
    if user_id is None:
        return redirect(url_for("login_view"))

    if not is_bookroom_owner(user_id, bookroom_id):
        return redirect(url_for("public_bookrooms_view"))

    bookroom = Bookroom.find_by_bookroom_id(bookroom_id)
    return render_template("test/update-bookroom.html", bookroom=bookroom)


# ブックルームの編集作業
@app.route("/public_bookrooms/update/<bookroom_id>", methods=["POST"])
def update_public_bookroom(bookroom_id):
    user_id = session.get("user_id", TEST_USER_ID)
    if user_id is None:
        return redirect(url_for("login_view"))

    if not is_bookroom_owner(user_id, bookroom_id):
        return redirect(url_for("public_bookrooms_view"))

    name = request.form.get("bookroom_name")
    description = request.form.get("bookroom_description")
    Bookroom.update(
        bookroom_id=bookroom_id,name=name, description=description
    )
    return redirect(url_for("public_bookrooms_view"))


# パブリックブックルームの削除
@app.route("/public_bookrooms/delete/<bookroom_id>", methods=["POST"])
def delete_public_bookroom(bookroom_id):
    # user_id = session.get('user_id')
    # セッションが未実装なため、仮値を入れる
    user_id = session.get("user_id", TEST_USER_ID)
    if user_id is None:
        return redirect(url_for("login_view"))

    if not is_bookroom_owner(user_id, bookroom_id):
        flash("ブックルーム作成者のみ削除可能です")
    else:
        Bookroom.delete(bookroom_id)
    return redirect(url_for("public_bookrooms_view"))


###########################
# プライベートブックルーム  #
###########################


############################ブックルーム関係（ここまで）############################


# ブックルーム詳細ページの表示
@app.route("/public_bookrooms/<bookroom_id>/messages", methods=["GET"])
def detail(bookroom_id):
    user_id = session.get("user_id")

    if user_id is None:
        return redirect(url_for("login_view"))

    bookroom = Bookroom.find_by_bookroom_id(bookroom_id)
    messages = Message.get_all(bookroom_id)

    return render_template(
        "messages.html", messages=messages, bookroom=bookroom, user_id=user_id
    )


# メッセージの投稿
@app.route("/public_bookrooms/<bookroom_id>/messages", methods=["POST"])
def create_message(bookroom_id):
    user_id = session.get("user_id")
    if user_id is None:
        return redirect(url_for("login_view"))

    message = request.form.get("message")

    if message:
        Message.create(user_id, bookroom_id, message)

    return redirect(
        "/public_bookrooms/{bookroom_id}/messages".format(bookroom_id=bookroom_id)
    )


# メッセージの削除
@app.route("/public_bookrooms/<bookroom_id>/messages/<message_id>", methods=["POST"])
def delete_message(bookroom_id, message_id):
    user_id = session.get("user_id")
    if user_id is None:
        return redirect(url_for("login_view"))

    if message_id:
        Message.delete(message_id)
    return redirect(
        "/public_bookrooms/{bookroom_id}/messages".format(bookroom_id=bookroom_id)
    )


@app.errorhandler(404)
def page_not_found(error):
    return render_template("error/404.html"), 404


@app.errorhandler(500)
def internal_server_error(error):
    return render_template("error/500.html"), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
