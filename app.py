# FlaskモジュールからFlaskクラスをインポート
from flask import Flask,render_template, request, redirect, session
#sqlite3をインポート
import sqlite3
#Flaskクラスをインスタンス化してapp変数に代入
app = Flask(__name__)

# secret_keyでセッション情報を暗号化
app.secret_key = "SUNABACO2023"

@app.route("/")
def index():
    if "user_id" in session:
        return redirect("/list")
    else:
        return render_template("top_page.html")

#@app.route("/<name>")
#def greet(name):
#    return name + "さん、こんばんは！"

@app.route("/add")
def add_get():
    if "user_id" in session:
        return render_template("add.html")
    else:
        return redirect("/")
    
@app.route("/add", methods=["POST"])
def add_post():
    if "user_id" in session:
        user_id = session["user_id"][0]
        # HTMLの入力フォームからデータをDBに保存する
        # 1.入力フォームからデータを取得する
        task = request.form.get("task")
        print(task)
        # 2.データベースに接続する
        conn = sqlite3.connect("myTask.db")
        # 3.データベースを操作するための準備@
        c = conn.cursor()
        # 4.SQLを実行してDBにデータを送る
        c.execute("insert into task values (null, ?, ?)",(task, user_id))
        # 5.データベースを更新（保存）する
        conn.commit()
        # 6.データベースの接続を終了する
        c.close()
        return redirect("/list") #"入力を受け付けました"
    else:
        return redirect("/")
    
@app.route("/list")
def list_get():
    # セッションが保持されていればリストページを返す
    if "user_id" in session:
        user_id = session["user_id"][0]
        conn = sqlite3.connect("myTask.db")
        c = conn.cursor()
        c.execute("select name from users where id = ?",(user_id,))
        user_name = c.fetchone()[0]
        # データを格納する配列を準備
        task_list = []
        # c.fetchall()で指定したDBのレコードを全件取得する
        for row in c.fetchall():
            # 取得したレコードを辞書型に変換して、task_listに追加する
            task_list.append({"id":row[0],"task":row[1]})
        c.close()
        print(task_list)
        return render_template("list.html", task_list = task_list, user_name = user_name)
    else:
        return redirect("/")
    
@app.route("/edit/<int:task_id>")
def edit_get(task_id):
    if "user_id" in session:
        conn = sqlite3.connect("myTask.db")
        c = conn.cursor()
        c.execute("select task from task where id = ?", (task_id,))
        #c.fetchone()でレコードの1行を取得（配列で取得される）
        task = c.fetchone()
        print(task)
        c.close
        # ここに記述
        task = task[0]
        return render_template("edit.html", task = task, task_id = task_id)
    else:
        return redirect("/")
    
@app.route("/edit", methods=["POST"])
def edit_post():
    if "user_id" in session:
        # フォームからtaskのidを取得
        task_id = request.form.get("task_id")
        # フォームから修正後の入力内容を取得
        task = request.form.get("task")
        # DBに接続
        conn = sqlite3.connect("myTask.db")
        # DBを操作できるようにする
        c = conn.cursor()
        # SQLを実行
        c.execute("update task set task = ? where id = ?", (task, task_id))
        # DBを更新(保存)する
        conn.commit()
        # DBの接続を終了する
        c.close()
        # リストページにリダイレクト
        return redirect("/list")
    else:
        return redirect("/")

@app.route("/delete/<int:task_id>")
def delete(task_id):
    if "user_id" in session:
        # DBに接続
        conn = sqlite3.connect("myTask.db")
        # DBを操作できるようにする
        c = conn.cursor()
        # SQLを実行する
        c.execute("delete from task where id = ?", (task_id,))
        # DBを更新(保存)する
        conn.commit()
        # DBの接続を終了する
        c.close()
        # リストページにリダイレクト
        return redirect("/list")
    else:
        return redirect("/")

@app.route("/regist")
def regist_get():
    if "user_id" in session:
        return redirect("/list")
    else:
        return render_template("regist.html")

@app.route("/regist", methods=["POST"])
def regist_post():
    #フォームからネームを取得
    name = request.form.get("name")
    #フォームからパスワードを取得
    password = request.form.get("password")
    #下のコードで、出力して内容を確認
    # DBに接続
    conn = sqlite3.connect("myTask.db")
    # DBを操作できるようにする
    c = conn.cursor()
    # SQLを実行する
    c.execute("insert into users values(null, ?, ?)",(name,password))
    conn.commit()
    c.close()
    return redirect("/login")

@app.route("/login")
def login_get():
    if "user_id" in session:
        return redirect("/list")
    else:
        return render_template("login.html")

@app.route("/login", methods=["POST"])
def login_post():
    #フォームからネームを取得
    name = request.form.get("name")
    #フォームからパスワードを取得
    password = request.form.get("password")
    #DBへ接続して、データを照合する
    conn = sqlite3.connect("myTask.db")
    # DBを操作できるようにする
    c = conn.cursor()
    c.execute("select id from users where name = ? and password = ?",(name, password))
    id = c.fetchone()
    c.close()
    if id is None:
    # idがなければログインページにリダイレクト
        return redirect("/login")
    else:
    # セッションを発行してidを格納
        session["user_id"] = id
    # idがあればリストページにリダイレクト
        return redirect("/list")

@app.route("/logout")
def logout():
    session.pop("user_id",None)
    return redirect("/")

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404


#スクリプトとして直接実行した場合
if __name__ == "__main__":
#　FlaskのWebアプリケーションを起動
    app.run(debug=True)