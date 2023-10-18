from flask import Flask, redirect, url_for, render_template, request, abort, session
from flask_hashing import Hashing
from flask_session import Session

# local imports
import db_client

# TODO implement logging

# global configuration
app = Flask(__name__)
hashing = Hashing(app)
sess = Session()

# import configuration from config.py
app.config.from_pyfile('config.py')

# create database client
meimei_db = db_client.DbClientMeme()


def is_valid_session():
    return session.get('user_name') is not None


def check_and_abort():
    if not session.get('user_name'):
        abort(403)


@app.route('/')
def root():
    # always redirect to '/login'
    return redirect(url_for('login'))


# standard login screen for logged-out users
@app.route('/login', methods=['POST', 'GET'])
def login():
    if not is_valid_session():
        # display if user doesn't have a valid session
        return render_template('login.html')
    # skip to session if user has valid session
    return redirect(url_for('create_meme'))


@app.post('/validate')
def validate_post():
    # get credentials from form
    user_name = request.form['user-name']
    password = request.form['password']

    # fail login attempt if one or more is empty
    if not any([user_name, password]):
        return redirect(url_for('login_failed'))

    # check for valid password
    hashed_password = hashing.hash_value(password)
    if hashing.check_value(hashed_password, app.config['PASSWORD']):
        # set persistent cookie with user credentials
        session['user_name'] = user_name
        return redirect(url_for('login_successful'))
    else:
        return redirect(url_for('login_failed'))


@app.get('/validate')
def validate_get():
    # return 403 forbidden if method is HTTP GET
    abort(403)


# TODO disallow access by HTTP GET
@app.route('/login-successful')
def login_successful():
    check_and_abort()
    # successful login redirects here
    return render_template('login-successful.html')


# TODO disallow access by HTTP GET
@app.route('/login-failed')
def login_failed():
    # failed login redirects here
    return render_template('login-failed.html')


@app.route('/logout')
def logout():
    # delete user session
    if is_valid_session():
        session['user_name'] = None
    return redirect('/')


@app.route('/create_meme')
def create_meme():
    # check login status
    check_and_abort()

    # get Meme from DB
    meimei = list(meimei_db.get_rand_image())[0]
    img_url = meimei['img_url']
    text_pos = meimei['text_pos']

    # check if meimei url is a Video
    is_video = any([img_url.endswith('.mp4'), img_url.endswith('.avi'), img_url.endswith('.mov')])

    return render_template('create_meme.html',
                           url=img_url,
                           is_video=is_video,
                           x=text_pos[0],
                           y=text_pos[1])


# submit a meme in a meme lab game
@app.route('/submit')
def submit():
    return render_template('meme_submit.html')


# view all memes in database
@app.route('/view')
def view_meme():
    return render_template("view_memes.html")


# view specific memes, enables sharing meme urls
@app.route('/view/<meme_url>')
def view(meme_url):
    print(meme_url)
    return meme_url


if __name__ == '__main__':
    # initialize flask session
    sess.init_app(app)
    app.run()
