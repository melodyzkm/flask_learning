"""
http://www.bjhee.com/flask-4.html
"""
import time
from flask import Flask, request, render_template, session, redirect, url_for, make_response

app = Flask(__name__)



@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.html')


@app.route('/signin', methods=['GET'])
def signin_form():
    return render_template('form.html')


@app.route('/signin', methods=['POST'])
def signin():
    username = request.form['username']
    password = request.form['password']
    if username=='admin' and password=='admin':
        return render_template('signin_ok.html', username=username)
    else:
        title = request.args.get('title', 'Default')
        response = make_response(render_template('login.html', title=title), 200)
        response.header['key'] = 'value'
        return response


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form.get("user") == "admin":
            return "Admin login successfuly."
        else:
            return "No such user"
    title = request.args.get("title", "Default")
    return render_template("login.html", title=title)



app.secret_key = "123456"
@app.route('/loginwithsession', methods=['GET', 'POST'])
def login_with_session():
    if request.method == 'POST':
        if request.form['user'] == 'admin':
            # 使用session之前一定要设置app.secret_key
            session['user'] = request.form['user']
            return "Admin login successfully."
        else:
            return "No such user!"
    if "user" in session:
        return "Hello {}".format(session['user'])
    else:
        title = request.args.get('title', 'Default')
        # 构建response对象
        response = make_response(render_template('login.html', title=title), 200)
        # 在header中添加键值
        response.headers['key'] = 'value'
        return response


@app.route('/loginwithcookie', methods=['GET', 'POST'])
def login_with_cookie():
    if request.method == "POST":
        if request.form.get('user') == 'admin':
            session['user'] = request.form.get('user')
            response = make_response("Admin login successfully")
            response.set_cookie('login_time', time.strftime("%Y-%m-%d %H:%M:%S"))
            return response
    else:
        if "user" in session:
            login_time = request.cookies.get("login_time")
            response = make_response("Hello {}, you login on {}".format(session.get('user'), login_time))
            return response
        else:
            response = make_response(render_template("login.html"))
            return response


@app.route('/logout')
def logout():
    session.pop("user", None)
    return redirect(url_for('login'))


@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')


@app.route('/hello')
@app.route('/hello/<name>')
def hello(name=None):
    if name is None:
        name = 'World'
    return 'Hello %s' % name


if __name__ == '__main__':
    app.run(debug=True)