from flask import Flask, redirect, url_for, render_template, request, abort, session, jsonify
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


@app.route('/validate', methods=['POST'])
def validate():
    # get credentials from form
    user_name = request.form['user-name']
    password = request.form['password']

    # fail login attempt if one or more is empty
    if not any([user_name, password]):
        return jsonify({'success': False})

    # check for valid password
    if hashing.check_value(hashing.hash_value(password), app.config['PASSWORD']):
        # set persistent cookie with user credentials
        session['user_name'] = user_name
        return jsonify({'success': True})
    else:
        return jsonify({'success': False})


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
