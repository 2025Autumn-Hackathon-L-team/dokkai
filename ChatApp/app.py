from flask import Flask, render_template, redirect, url_for, session, request, flash
from flask_paginate import Pagination, get_page_parameter
from datetime import timedelta
from zoneinfo import ZoneInfo
import hashlib
import uuid
import re
import os

from models import User, Bookroom, Message, Profile, Tag, BookroomTag

############################認証関係(ここから)####################################
EMAIL_PATTERN = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
SESSION_DAYS = 30
MAX_LENGTH_BOOKROOM_NAME=100
MAX_LENGTH_BOOKROOM_DESCRIPTION=250

PER_PAGE = 5  # 1ページに表示するブックルームの数

# ユーザーIDを仮で作成
TEST_USER_ID = "970af84c-dd40-47ff-af23-282b72b7cca8"

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", uuid.uuid4().hex)
app.permanent_session_lifetime = timedelta(days=SESSION_DAYS)

# 開発中の確認のために使用
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.jinja_env.auto_reload = True
app.jinja_env.cache = {}


# ルートページのリダイレクト
@app.route("/")
def index():
    user_id = session.get("user_id")
    print(f"sessionは{user_id}です")
    if user_id is None:
        return redirect(url_for("login_view"))
    return redirect(url_for("public_bookrooms_view"))


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
        registered_email_user = User.find_by_email(email)
        registered_name_user = User.find_by_name(name)
        if registered_email_user != None:
            flash("入力されたメールアドレスは使用されています。")
            flash("違うメールアドレスを入力してください。")
        elif registered_name_user != None:
            flash("入力された名前は使用されています。")
            flash("違う名前を入力してください。")
        else:
            id = uuid.uuid4()
            password = hashlib.sha256(password.encode("utf-8")).hexdigest()
            User.create(id, name, email, password)
            UserId = str(id)
            UserName = str(name)
            UserEmail = str(email)
            print(f"{UserId}はUserIdです")  # 代入された値の確認用
            print(f"{UserName}はUserNameです")  # 値確認用
            print(f"{UserEmail}はUserEmailです")  # 値確認用
            session["user_id"] = UserId
            session["user_name"] = UserName
            session["user_email"] = UserEmail
            return redirect(url_for("public_bookrooms_view"))
    # バリデーションエラーでsignup_processに戻る時、フォームに入力した値をauth/signup.htmlに返す
    print(f"{password}がpassword")
    print(f"{passwordConfirmation}がpassword_confirmation")
    return render_template(
        "auth/signup.html",
        name=name,
        email=email,
        password=password,
        password_confirmation=passwordConfirmation,
    )


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
        flash("ログインできませんでした。")
        flash("メールアドレスとパスワードを入力してください。")
    elif password == "":
        flash("ログインできませんでした。")
        flash("パスワードを入力してください。")
    elif email == "":
        flash("ログインできませんでした。")
        flash("メールアドレスを入力してください。")
    else:
        user = User.find_by_email(email)
        # ログイン失敗、セキュリティのため、mailとpasswordのどちらかが間違っているようなメッセージを表示。
        if user is None:
            flash("ログインできませんでした。")
            flash("メールアドレスかパスワードが間違っています。")
        else:
            # パスワードの一致チェック
            hashPassword = hashlib.sha256(password.encode("utf-8")).hexdigest()
            user = User.find_by_email(email)
            # ログイン失敗、セキュリティのため、mailとpasswordのどちらかが間違っているようなメッセージを表示。
            if user["password"] != hashPassword:
                flash("ログインできませんでした。")
                flash("メールアドレスかパスワードが間違っています。")
            else:
                session["user_id"] = user["id"]
                session["user_name"] = user["name"]
                session["user_email"] = user["email"]
                print(
                    f"{user}でログインできました"
                )  # ログインできているかチェック、後ほど削除
                return redirect(url_for("public_bookrooms_view"))
    # バリデーションエラーでauth/login.htmlnに戻る時、フォームに入力した値をauth/login.htmlに返す
    return render_template("auth/login.html", email=email, password=password)


# ログアウト処理
@app.route("/logout", methods=["GET", "POST"])
def logout():
    session.clear()
    return redirect(url_for("login_view"))


############################認証関係(ここまで)####################################
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


# ログインしているuser_idを返す。テストの際は、TEST_USER_IDを格納する。
def get_login_user_id():
    if app.debug:
        session["user_id"] = TEST_USER_ID

    user_id = session.get("user_id")
    return user_id


def get_bookroom_group_tags(bookroom_tag_tables):
    # 空のdictを作成(これにどんどん追加していく)
    # 空のtagリストを作成（同じブックルームのタグは、1つのリストに入れる。）
    bookroom_group_tag = {}
    tags = []

    # 空の場合は空のまま返す
    if not bookroom_tag_tables:
        return bookroom_group_tag

    previous_bookroom_id = bookroom_tag_tables[0]["bookroom_id"]

    for bookroom_tag_data in bookroom_tag_tables:
        if bookroom_tag_data["bookroom_id"] == previous_bookroom_id:
            tags.append(bookroom_tag_data["name"])  # タグの名前を追加格納
        else:
            bookroom_group_tag[previous_bookroom_id] = tags
            tags = []
            tags.append(bookroom_tag_data["name"])  # タグの名前を格納
            previous_bookroom_id = bookroom_tag_data["bookroom_id"]
    bookroom_group_tag[previous_bookroom_id] = tags
    return bookroom_group_tag


# 日本時間に変更
def change_jst(utc_time):
    utc = ZoneInfo("UTC")
    jst = ZoneInfo("Asia/Tokyo")
    utc_time = utc_time.replace(tzinfo=utc)
    if utc_time is None:
        utc_time = utc_time.replace(tzinfo=utc)
    return utc_time.astimezone(jst)


# パブリックブックルームの一覧表示
@app.route("/public_bookrooms", methods=["GET"])
def public_bookrooms_view():
    user_id = get_login_user_id()
    if user_id is None:
        return redirect(url_for("login_view"))

    # publicなブックルームのみ取得
    bookrooms = Bookroom.get_public_bookrooms()

    # tagデータを取得
    # データベースからすべてのbookroom_idとタグデータをセットで取得
    bookroom_tag_tables = BookroomTag.get_bookroom_tag_tables()
    # 同じブックルームIDのタグデータをまとめる様にデータを変更
    bookroom_group_tag = get_bookroom_group_tags(bookroom_tag_tables)

    # ページネーション
    page = request.args.get(get_page_parameter(), type=int, default=1)
    paginated_bookrooms = bookrooms[(page - 1) * PER_PAGE : page * PER_PAGE]

    # ページネーション分のbookroom_idを取得
    pagenated_bookroom_id = []
    for bookroom in bookrooms:
        pagenated_bookroom_id.append(bookroom["id"])

    # ページネーション分のbookroom_idに該当するtagデータを格納。タグがない場合は空データを入れる
    pagenated_bookroom_tag = {}
    for bookroom_id in pagenated_bookroom_id:
        if bookroom_id in bookroom_group_tag:
            pagenated_bookroom_tag[bookroom_id] = bookroom_group_tag[bookroom_id]
        else:
            pagenated_bookroom_tag[bookroom_id] = []

    pagination = Pagination(
        page=page,
        total=len(bookrooms),
        per_page=PER_PAGE,
        display_pages=True,
        record_name="ブックルーム",
    )

    # タグテーブルに登録されているタグを取得
    tags = Tag.get_all_tags()
    print("pagenated_bookroom_tag =", pagenated_bookroom_tag)

    # 時間をJSTに変更
    for bookroom in paginated_bookrooms:
        bookroom["created_at"] = change_jst(bookroom["created_at"])
        bookroom["updated_at"] = change_jst(bookroom["updated_at"])

    if app.debug:
        return render_template(
            "test/public_bookroom.html",
            is_public=True,
            uid=user_id,
            paginated_bookrooms=paginated_bookrooms,
            pagenated_bookroom_tag=pagenated_bookroom_tag,
            pagination=pagination,
            tags=tags,
        )
    else:
        return render_template(
            "public_bookroom.html",
            is_public=True,
            uid=user_id,
            paginated_bookrooms=paginated_bookrooms,
            pagenated_bookroom_tag=pagenated_bookroom_tag,
            pagination=pagination,
            tags=tags,
        )


# パブリックブックルームの作成
@app.route("/public_bookrooms", methods=["POST"])
def create_public_bookroom():
    user_id = get_login_user_id()
    if user_id is None:
        return redirect(url_for("login_view"))

    bookroom_name = request.form.get("bookroom_name")
    # ブックルームの名前が入力されていない。またはスペースだけであれば、作成できないようにする
    if len(bookroom_name.strip()) == 0:
        flash("ブックルーム名を入力してください","createbookroom_flash")
        return redirect(url_for("create_public_bookroom"))
    
    # ブックルームの名前がMAX_LENGTH_BOOKROOM_NAMEの数（自由に設定可能）を超えていたらバリデーション
    if len(bookroom_name)>MAX_LENGTH_BOOKROOM_NAME:
            flash("入力可能文字数をオーバーしました","createbookroom_flash")
            flash("BOOKROOMのテーマは100文字以内で入力してください","createbookroom_flash")
            return redirect(url_for("public_bookrooms_view")) # TODO 遷移先これでいいか確認

    bookroom = Bookroom.find_by_public_bookroom_name(
        bookroom_name=bookroom_name
    )

    # 他のユーザーが同じ名前を登録していないかチェック。
    if bookroom != None:
        flash("入力されたBOOKROOMのテーマは使用されています。","createbookroom_flash")
        return redirect(url_for("public_bookrooms_view")) # TODO 遷移先これでいいか確認
    
    if bookroom is None:
        bookroom_description = request.form.get("bookroom_description")
        # ブックルームの説明欄がMAX_LENGTH_BOOKROOM_DESCRIPTIONの数（自由に設定可能）を超えていたらバリデーション
        if len(bookroom_description)>MAX_LENGTH_BOOKROOM_DESCRIPTION:
            flash("入力可能文字数をオーバーしました","createbookroom_flash")
            flash("BOOKROOMの紹介文は256文字以内で入力してください","createbookroom_flash")
            return redirect(url_for("public_bookrooms_view")) # TODO 遷移先これでいいか確認
        bookroom_id = Bookroom.create(
            user_id=user_id,
            name=bookroom_name,
            description=bookroom_description,
            is_public=True,
        )

        tag_ids = request.form.getlist("tag_ids")
        BookroomTag.create(bookroom_id, tag_ids)

        return redirect(url_for("public_bookrooms_view"))
    else:
        error = "既に同じ名前のブックルームが存在しています。"
        return render_template("error/404.html", error_message=error)


###########################未使用ここから####################################
# パブリックブックルーム編集ページ表示

if app.debug:

    @app.route("/public_bookrooms/update/<bookroom_id>", methods=["GET"])
    def edit_bookroom(bookroom_id):
        # ログイン確認
        user_id = get_login_user_id()
        if user_id is None:
            return redirect(url_for("login_view"))

        # 編集権限確認
        if not is_bookroom_owner(user_id, bookroom_id):
            return redirect(url_for("public_bookrooms_view"))

        bookroom = Bookroom.find_by_bookroom_id(bookroom_id)
        all_tags = Tag.get_all_tags()

        selected_tag_ids = BookroomTag.get_selected_tags_from_bookroomid(bookroom_id)
        selected_tag_ids_list = []
        for selected_tag_id in selected_tag_ids:
            selected_tag_ids_list.append(selected_tag_id["tag_id"])

        # 日本時間に変更(編集のページでは表示しないが念のため)
        bookroom["created_at"] = change_jst(bookroom["created_at"])
        bookroom["updated_at"] = change_jst(bookroom["updated_at"])

        return render_template(
            "test/update-bookroom.html",
            bookroom=bookroom,
            tags=all_tags,
            selected_tag_ids=selected_tag_ids_list,
        )


###########################未使用ここまで####################################


# パブリックブックルームの編集作業
@app.route("/public_bookrooms/update/<bookroom_id>", methods=["POST"])
def update_public_bookroom(bookroom_id):
    # ログインしているかのチェック
    user_id = get_login_user_id()
    if user_id is None:
        return redirect(url_for("login_view"))

    if not is_bookroom_owner(user_id, bookroom_id):
        return redirect(url_for("public_bookrooms_view"))

    bookroom_name = request.form.get("bookroom_name")
    description = request.form.get("bookroom_description")

    # 他のユーザーが同じ名前を登録していないかチェック。ただし自分が登録したブックルーム名を編集せずにそのまま更新する場合はそのまま通る。
    exiting_bookroom_name=Bookroom.find_by_public_bookroom_name(bookroom_name=bookroom_name)
    if exiting_bookroom_name is not None and str(exiting_bookroom_name["id"]) != str(bookroom_id):
        flash("入力されたBOOKROOMのテーマは使用されています。","updatebookroom_flash")
        return redirect(url_for("detail", bookroom_id=bookroom_id)) # TODO 遷移先これでいいか確認
    # ブックルームの名前がMAX_LENGTH_BOOKROOM_NAMEの数（自由に設定可能）を超えていたらバリデーション
    if len(bookroom_name)>MAX_LENGTH_BOOKROOM_NAME:
        flash("入力可能文字数をオーバーしました")
        flash("BOOKROOMのテーマは100文字以内で入力してください","updatebookroom_flash")
        return redirect(url_for("detail", bookroom_id=bookroom_id)) # TODO 遷移先これでいいか確認
    # ブックルームの説明欄がMAX_LENGTH_BOOKROOM_DESCRIPTIONの数（自由に設定可能）を超えていたらバリデーション
    if len(description)>MAX_LENGTH_BOOKROOM_DESCRIPTION:
        flash("入力可能文字数をオーバーしました")
        flash("BOOKROOMの紹介文は256文字以内で入力してください","updatebookroom_flash")
        return redirect(url_for("public_bookrooms_view")) # TODO 遷移先これでいいか確認

    
    Bookroom.update(bookroom_id=bookroom_id, name=bookroom_name, description=description)

    tag_ids = request.form.getlist("tag_ids")
    BookroomTag.delete_bookroomtag_by_bookroomid(bookroom_id)
    BookroomTag.create(bookroom_id, tag_ids)

    if app.debug:
        return redirect(url_for("public_bookrooms_view", bookroom_id=bookroom_id))
    else:
        return redirect(url_for("detail", bookroom_id=bookroom_id))


# パブリックブックルームの削除
@app.route("/public_bookrooms/delete/<bookroom_id>", methods=["POST"])
def delete_public_bookroom(bookroom_id):
    # ログインしているかのチェック
    user_id = get_login_user_id()
    if user_id is None:
        return redirect(url_for("login_view"))

    if is_bookroom_owner(user_id, bookroom_id):
        Bookroom.delete(bookroom_id)

    return redirect(url_for("public_bookrooms_view"))


###########################
# プライベートブックルーム  #
###########################
# プライベートブックルームの一覧表示
@app.route("/private_bookrooms", methods=["GET"])
def private_bookrooms_view():
    # ログインしているかのチェック
    user_id = get_login_user_id()
    if user_id is None:
        return redirect(url_for("login_view"))

    # privateなブックルームのみ取得
    bookrooms = Bookroom.get_private_bookrooms(user_id)

    # tagデータを取得
    # データベースからすべてのbookroom_idとタグデータをセットで取得
    bookroom_tag_tables = BookroomTag.get_bookroom_tag_tables()
    # 同じブックルームIDのタグデータをまとめる様にデータを変更
    bookroom_group_tag = get_bookroom_group_tags(bookroom_tag_tables)

    # ページネーション
    page = request.args.get(get_page_parameter(), type=int, default=1)
    paginated_bookrooms = bookrooms[(page - 1) * PER_PAGE : page * PER_PAGE]

    # ページネーション分のbookroom_idを取得
    pagenated_bookroom_id = []
    for bookroom in bookrooms:
        pagenated_bookroom_id.append(bookroom["id"])

    # ページネーション分のbookroom_idに該当するtagデータを格納。タグがない場合は空データを入れる
    pagenated_bookroom_tag = {}
    for bookroom_id in pagenated_bookroom_id:
        if bookroom_id in bookroom_group_tag:
            pagenated_bookroom_tag[bookroom_id] = bookroom_group_tag[bookroom_id]
        else:
            pagenated_bookroom_tag[bookroom_id] = []

    pagination = Pagination(
        page=page,
        total=len(bookrooms),
        per_page=PER_PAGE,
        display_pages=True,
        record_name="ブックルーム",
    )

    for bookroom in paginated_bookrooms:
        bookroom["created_at"] = change_jst(bookroom["created_at"])
        bookroom["updated_at"] = change_jst(bookroom["updated_at"])

    # タグテーブルに登録されているタグを取得
    tags = Tag.get_all_tags()

    if app.debug:
        return render_template(
            "test/private_bookroom.html",
            is_public=False,
            uid=user_id,
            paginated_bookrooms=paginated_bookrooms,
            pagenated_bookroom_tag=pagenated_bookroom_tag,
            pagination=pagination,
            tags=tags,
        )
    else:
        return render_template(
            "private_bookroom.html",
            is_public=False,
            uid=user_id,
            paginated_bookrooms=paginated_bookrooms,
            pagenated_bookroom_tag=pagenated_bookroom_tag,
            pagination=pagination,
            tags=tags,
        )


# プライベートブックルームの作成
@app.route("/private_bookrooms", methods=["POST"])
def create_private_bookroom():
    # ログインしているかのチェック
    user_id = get_login_user_id()
    if user_id is None:
        return redirect(url_for("login_view"))

    bookroom_name = request.form.get("bookroom_name")
    # ブックルームの名前が入力されていない。またはスペースだけであれば、作成できないようにする
    if len(bookroom_name.strip()) == 0:
        flash("ブックルーム名を入力してください","createbookroom_flash")
        return redirect(url_for("create_private_bookroom","createbookroom_flash"))
    
    # ブックルームの名前がMAX_LENGTH_BOOKROOM_NAMEの数（自由に設定可能）を超えていたらバリデーション
    if len(bookroom_name)>MAX_LENGTH_BOOKROOM_NAME:
            flash("入力可能文字数をオーバーしました","createbookroom_flash")
            flash("BOOKROOMのテーマは100文字以内で入力してください","createbookroom_flash")
            return redirect(url_for("private_bookrooms_view")) # TODO 遷移先これでいいか確認

    bookroom = Bookroom.find_by_private_bookroom_name(
        bookroom_name=bookroom_name, user_id=user_id
    )

    # プライベートブックルームの中で同じ名前を登録していないかチェック。
    if bookroom != None:
        flash("入力されたBOOKROOMのテーマは使用されています。","createbookroom_flash")
        return redirect(url_for("private_bookrooms_view")) # TODO 遷移先これでいいか確認

    if bookroom is None:
        bookroom_description = request.form.get("bookroom_description")
        # ブックルームの説明欄がMAX_LENGTH_BOOKROOM_DESCRIPTIONの数（自由に設定可能）を超えていたらバリデーション
        if len(bookroom_description)>MAX_LENGTH_BOOKROOM_DESCRIPTION:
            flash("入力可能文字数をオーバーしました","createbookroom_flash")
            flash("BOOKROOMの紹介文は256文字以内で入力してください","createbookroom_flash")
            return redirect(url_for("private_bookrooms_view")) # TODO 遷移先これでいいか確認
        bookroom_id = Bookroom.create(
            user_id=user_id,
            name=bookroom_name,
            description=bookroom_description,
            is_public=False,
        )

        # タグ取得
        tag_ids = request.form.getlist("tag_ids")
        # タグデータをデータベースに登録
        BookroomTag.create(bookroom_id, tag_ids)

        return redirect(url_for("private_bookrooms_view"))
    else:
        error = "既に同じ名前のブックルームが存在しています。"
        return render_template("error/404.html", error_message=error)


# プライベートブックルームの編集作業
@app.route("/private_bookrooms/update/<bookroom_id>", methods=["POST"])
def update_private_bookroom(bookroom_id):
    # ログインしているかのチェック
    user_id = get_login_user_id()
    if user_id is None:
        return redirect(url_for("login_view"))

    if not is_bookroom_owner(user_id, bookroom_id):
        return redirect(url_for("private_bookrooms_view"))

    name = request.form.get("bookroom_name")
    description = request.form.get("bookroom_description")

    # プライベートブックルームの中で同じ名前を登録していないかチェック。ただし自分が登録したブックルーム名を編集せずにそのまま更新する場合はそのまま通る。
    exiting_bookroom_name=Bookroom.find_by_private_bookroom_name(bookroom_name=name, user_id=user_id)
    if exiting_bookroom_name is not None and str(exiting_bookroom_name["id"]) != str(bookroom_id):
        flash("入力されたBOOKROOMのテーマは使用されています。","updatebookroom_flash")
        return redirect(url_for("private_detail", bookroom_id=bookroom_id)) # TODO 遷移先これでいいか確認
    
    # ブックルームの名前がMAX_LENGTH_BOOKROOM_NAMEの数（自由に設定可能）を超えていたらバリデーション
    if len(name)>MAX_LENGTH_BOOKROOM_NAME:
        flash("入力可能文字数をオーバーしました","updatebookroom_flash")
        flash("BOOKROOMのテーマは100文字以内で入力してください","updatebookroom_flash")
        return redirect(url_for("private_detail", bookroom_id=bookroom_id)) # TODO 遷移先これでいいか確認
    # ブックルームの説明欄がMAX_LENGTH_BOOKROOM_DESCRIPTIONの数（自由に設定可能）を超えていたらバリデーション
    if len(description)>MAX_LENGTH_BOOKROOM_DESCRIPTION:
        flash("入力可能文字数をオーバーしました","updatebookroom_flash")
        flash("BOOKROOMの紹介文は256文字以内で入力してください","updatebookroom_flash")
        return redirect(url_for("private_detail", bookroom_id=bookroom_id)) # TODO 遷移先これでいいか確認

    Bookroom.update(bookroom_id=bookroom_id, name=name, description=description)

    tag_ids = request.form.getlist("tag_ids")
    BookroomTag.delete_bookroomtag_by_bookroomid(bookroom_id)
    BookroomTag.create(bookroom_id, tag_ids)

    return redirect(url_for("private_bookrooms_view"))


# プライベートブックルームの削除
@app.route("/private_bookrooms/delete/<bookroom_id>", methods=["POST"])
def delete_private_bookroom(bookroom_id):
    # ログインしているかのチェック
    user_id = get_login_user_id()
    if user_id is None:
        return redirect(url_for("login_view"))

    if not is_bookroom_owner(user_id, bookroom_id):
        flash("ブックルーム作成者のみ削除可能です")
    else:
        Bookroom.delete(bookroom_id)
    return redirect(url_for("private_bookrooms_view"))


# ヒストリーブックルームの表示（仮設置）
@app.route("/history", methods=["GET"])
def history_view():
    # publicなブックルームのみ取得
    bookrooms = Bookroom.get_public_bookrooms()
    # 表示チェックのためデフォルト値を設定
    user_id = session.get("user_id")

    # ページネーション
    page = request.args.get(get_page_parameter(), type=int, default=1)
    paginated_bookrooms = bookrooms[(page - 1) * PER_PAGE : page * PER_PAGE]
    pagination = Pagination(
        page=page,
        total=len(bookrooms),
        per_page=PER_PAGE,
        css_framework="bootstrap5",
        display_pages=True,
        record_name="ブックルーム",
    )

    return render_template(
        "history_bookroom.html",
        is_public=True,
        uid=user_id,
        paginated_bookrooms=paginated_bookrooms,
        pagination=pagination,
    )


############################ブックルーム関係（ここまで）############################
############################メッセージ関係（ここから）############################

#####################################
#  パブリックブックルームのメッセージ   #
#####################################


# パブリックブックルーム詳細ページの表示
@app.route("/public_bookrooms/<bookroom_id>/messages", methods=["GET"])
def detail(bookroom_id):
    # 表示チェックのためデフォルトユーザを設定
    user_id = session.get("user_id")

    if user_id is None:
        return redirect(url_for("login_view"))

    bookroom = Bookroom.find_by_bookroom_id(bookroom_id)
    messages = Message.get_all(bookroom_id)

    # 現在登録されているブックルーム名表示のため追記ここから
    all_tags = Tag.get_all_tags()

    selected_tag_ids = BookroomTag.get_selected_tags_from_bookroomid(bookroom_id)
    selected_tag_ids_list = []
    for selected_tag_id in selected_tag_ids:
        selected_tag_ids_list.append(selected_tag_id["tag_id"])

    # ブックルーム名編集のため追記ここまで

    return render_template(
        "public_messages.html",
        messages=messages,
        bookroom=bookroom,
        uid=user_id,
        tags=all_tags,
        selected_tag_ids=selected_tag_ids_list,
    )


# パブリックブックルームメッセージの投稿
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


# パブリックブックルームメッセージの削除
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


#####################################
#  プライベートブックルームのメッセージ   #
#####################################
# プライベートブックルーム詳細ページの表示
@app.route("/private_bookrooms/<bookroom_id>/messages", methods=["GET"])
def private_detail(bookroom_id):
    # 表示チェックのためデフォルトユーザを設定
    user_id = session.get("user_id")

    if user_id is None:
        return redirect(url_for("login_view"))

    bookroom = Bookroom.find_by_bookroom_id(bookroom_id)
    messages = Message.get_all(bookroom_id)

    # ブックルーム名編集のため追記ここから
    all_tags = Tag.get_all_tags()

    selected_tag_ids = BookroomTag.get_selected_tags_from_bookroomid(bookroom_id)
    selected_tag_ids_list = []
    for selected_tag_id in selected_tag_ids:
        selected_tag_ids_list.append(selected_tag_id["tag_id"])

    # ブックルーム名編集のため追記ここまで

    return render_template(
        "private_messages.html",
        messages=messages,
        bookroom=bookroom,
        uid=user_id,
        tags=all_tags,
        selected_tag_ids=selected_tag_ids_list,
    )


# プライベートブックルームへのメッセージの投稿
@app.route("/private_bookrooms/<bookroom_id>/messages", methods=["POST"])
def private_create_message(bookroom_id):
    user_id = session.get("user_id")
    if user_id is None:
        return redirect(url_for("login_view"))

    message = request.form.get("message")

    if message:
        Message.create(user_id, bookroom_id, message)

    return redirect(
        "/private_bookrooms/{bookroom_id}/messages".format(bookroom_id=bookroom_id)
    )


# プライベートブックルームのメッセージの削除
@app.route("/private_bookrooms/<bookroom_id>/messages/<message_id>", methods=["POST"])
def private_delete_message(bookroom_id, message_id):
    user_id = session.get("user_id")
    if user_id is None:
        return redirect(url_for("login_view"))

    if message_id:
        Message.delete(message_id)
    return redirect(
        "/private_bookrooms/{bookroom_id}/messages".format(bookroom_id=bookroom_id)
    )


############################メッセージ関係（ここまで）############################
############################プロフィール画面（ここから）##########################


# プロフィール画面の表示
@app.route("/profile")
def profile_view():
    user_id = session.get("user_id")
    if user_id is None:
        return redirect(url_for("login_view"))
    current_name = Profile.name_view(user_id)
    current_email = Profile.email_view(user_id)
    icon_view = Profile.icon_view(user_id)
    messages_count = Profile.get_messages_count(user_id)
    # TODO リアクション機能実装後、リアクションの数を取得する。
    # printはサーバーで出る値を確認。後日削除する。
    print(f"{icon_view}はiconidです")
    print(f"{user_id}はprofile.htmlで現在セッションを持っているユーザーです")
    print(
        f"{current_name}はprofile.htmlで現在セッションを持っているユーザーのnameを表示しています"
    )
    print(
        f"{current_email}はprofile.htmlで現在セッションを持っているユーザーのemailを表示しています"
    )
    print(f"{messages_count}は{current_name}が投稿したメッセージの数を表しています")
    return render_template(
        "profile.html",
        icon=icon_view,
        uid=user_id,
        name=current_name,
        email=current_email,
        messages_count=messages_count,
    )


# プロフィール画面の編集(name)
@app.route("/name/update",methods=["POST"])
def update_name():
    user_id=session.get("user_id")

    if user_id is None:
        return redirect(url_for("login_view"))
    
    name=request.form.get("profile_name")
    # 値確認用
    print(f'{name}は入力されたname')
    # 空欄チェック
    if name == "":
            flash("すべての項目を入力してください。", "name_flash")
            return redirect(url_for("profile_view"))
    # 他のユーザーが同じ名前を登録していないかチェック。ただし自分が登録した名前と一致している場合はそのまま通る。
    registered_name_user=User.find_by_name(name)
    if registered_name_user is not None and registered_name_user["id"] != user_id:
        flash("入力された名前は使用されています。", "name_flash")
        flash("違う名前を入力してください。", "name_flash")
        return redirect(url_for("profile_view"))
    # 更新処理
    else:
        Profile.name_update(name,user_id)
        flash("プロフィールを更新しました。", "success_flash")
    return redirect(url_for("profile_view"))

# プロフィール画面の編集(email)
@app.route("/email/update",methods=["POST"])
def update_email():
    user_id=session.get("user_id")
    current_email=Profile.email_view(user_id)

    if user_id is None:
        return redirect(url_for("login_view"))
    
    email=request.form.get("profile_email")
    password = request.form.get("password")
    # 値確認用
    print(f'{email}は入力されたemail')
    # 空欄チェック
    if email == "" or password == "" :
            flash("すべての項目を入力してください。", "email_flash")
            return redirect(url_for("profile_view"))
    # メールアドレス形式チェック
    if re.fullmatch(EMAIL_PATTERN, email) is None:
        flash("有効なメールアドレスを入力してください。", "email_flash")
        return redirect(url_for("profile_view"))
    # 他のユーザーが同じメールアドレスを登録していないかチェック。ただし自分が登録したメールアドレスと一致している場合はそのまま通る。
    registered_email_user= User.find_by_email(email) 
    if registered_email_user is not None and registered_email_user["id"] != user_id:
        flash("入力されたメールアドレスは使用されています。", "email_flash")
        flash("違うメールアドレスを入力してください。", "email_flash")
        return redirect(url_for("profile_view"))
    hashPassword = hashlib.sha256(password.encode("utf-8")).hexdigest()
    user = User.find_by_email(current_email)
    # ログインチェック
    if user["password"] != hashPassword:
        flash("パスワードが正しくありません。", "email_flash")
        return redirect(url_for("profile_view"))
    # 更新処理
    else:
        Profile.email_update(email,user_id)
        flash("プロフィールを更新しました。", "success_flash")
    return redirect(url_for("profile_view"))


# アイコン画面の変更
@app.route("/icons/update", methods=["POST"])
def update_icon():
    user_id = session.get("user_id")
    print("セッション内容:", dict(session))
    print("取得したuser_id:", session.get("user_id"))

    if user_id is None:
        return redirect(url_for("login_view"))
    else:
        iconid = request.form.get("icon_name")
        print(f"{iconid}は選択されたicon")
        Profile.icon_update(iconid, user_id)
    # TODO M_iconsができたらreturn render_template("profile_view",filename=画像のパス)を渡す。
    return redirect(url_for("profile_view"))


########プロフィール画面（ここまで）##########


@app.errorhandler(404)
def page_not_found(error):
    return render_template("error/404.html"), 404


@app.errorhandler(500)
def internal_server_error(error):
    return render_template("error/500.html"), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=False)
