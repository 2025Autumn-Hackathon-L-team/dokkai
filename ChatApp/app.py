from flask import Flask, request, redirect, render_template, url_for

from models import Bookroom

app = Flask(__name__)


# ブックルームの一覧表示
@app.route("/public_bookrooms", methods=["GET"])
def public_channels_view():
    # uid = session.get('uid')
    # if uid is None:
    #    return redirect(ufl_for('login_view'))
    # else:
    bookrooms = Bookroom.get_public_bookrooms()
    return render_template("bookroom.html", bookrooms=bookrooms, is_public=True)


# @app.route('/public_bookrooms', methods=['POST'])
# def create_bookroom():
#    bookroom_name = request.form['bookroomname']

#    db = get_db()

#    if not book


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
