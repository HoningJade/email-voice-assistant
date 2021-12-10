from flask import Flask, url_for, render_template, request, redirect, make_response
app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello, World!'

# URL Routing
# Converter


@app.route('/start/', defaults={'page': 0})
@app.route('/start/page/<int:page>/')
def show_users(page):
    return str(page)

# URL Building


@app.route('/user/<username>/')
def profile(username):
    # return f'{username}\'s profile'
    return render_template('hello.html', name=username)

# # Rendering HTML template
# @app.route('/template/')
# @app.route('/template/<name>')
# def hello(name=None):
#     return render_template('hello.html', name=name)

# Request


def valid_login(username, password):
    return username == 'admin' and password == 'foo'


def log_the_user_in(username):
    return redirect(url_for('profile', username=username))


@app.route('/login/', methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        if valid_login(request.form.get('uname'),
                       request.form.get('psw')):
            return log_the_user_in(request.form.get('uname'))
        else:
            error = 'Invalid username/password'
    return render_template('login.html', error=error)

# # Error Handler
# @app.errorhandler(404)
# def page_not_found(error):
#     # note that we set the 404 status explicitly
#     return render_template('404.html'), 404

# Response


@app.errorhandler(404)
def page_not_found(error):
    # print(1)
    # print(error)
    # print(request.url)
    # print(2)
    resp = make_response(render_template('404.html'), 404)
    return resp

# APIs with JSON


@app.route("/new-user/", methods=['POST', 'GET'])
def new_user():
    if request.method == 'POST':
        return {
            'username': request.form['uname'],
            'email': request.form['email'],
            'password': request.form['psw']
        }
    return render_template('new-user.html')


if __name__ == '__main__':
    # with app.test_request_context():
    #     print(url_for('hello_world'))
    #     print(url_for('show_users'))
    #     print(url_for('show_users', page=0))
    #     print(url_for('show_users', page=1))
    #     print(url_for('hello_world', next='foo'))
    #     print(url_for('profile', username='John Doe'))
    app.run(debug=True)
    # app.run(host='0.0.0.0', port=8080)
