from flask import Flask, redirect, url_for, render_template, request, abort, session, jsonify, make_response
from flask_hashing import Hashing
from flask_session import Session
from game import Game, Player

# local imports
import db_client

# TODO implement logging

# global configuration
app = Flask(__name__)
hashing = Hashing(app)
current_session = Session()
game = Game()

# import configuration from config.py
app.config.from_pyfile('config.py')

# create database client
meimei_db = db_client.DbClientMeme()


def is_valid_session():
    return session.get('user_name') is not None
    # session.get('user_name') in [player.name for player in game.memes.keys()]


def check_and_abort():
    if not session.get('user_name'):
        abort(403)


@app.route('/')
def root():
    # always redirect to '/login'
    print(game.memes)
    return redirect(url_for('login'))


# standard login screen for logged-out users
@app.route('/login', methods=['POST', 'GET'])
def login():
    if not is_valid_session():
        # display if user doesn't have a valid session
        return render_template('login.html')

    # skip to session if user has valid session
    return redirect(url_for('lobby'))


@app.route('/validate', methods=['POST'])
def validate():
    # get credentials from form
    user_name = request.form['user-name']
    password = request.form['password']

    # fail login attempt if one or more is empty
    if not any([user_name, password]):
        return jsonify({'success': False})

    # check for valid password
    if hashing.hash_value(password) == app.config['PASSWORD']:
        # set persistent cookie with user credentials
        session['user_name'] = user_name

        # create a player Object and add it to the game
        player = Player(user_name)
        game.add_player(player)
        return jsonify({'success': True})
    else:
        data['success'] = False

    print(data)
    return jsonify(data)


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

    game.phase = GamePhase.Creating
    print(game.phase)
    # get Meme from DB
    meimei = list(meimei_db.get_rand_image())[0]
    img_url = meimei['img_url']
    text_pos = meimei['text_pos']
    print(f"{img_url = }  ||||  {text_pos = }")

    # check if meimei url is a Video
    is_video = any([img_url.endswith('.mp4'), img_url.endswith('.avi'), img_url.endswith('.mov')])

    return render_template('create_meme.html',
                           url=img_url,
                           is_video=is_video,
                           x=text_pos[0],
                           y=text_pos[1],
                           name=session.get("user_name"))


# submit a meme in a meme lab game
@app.route('/submit', methods=['POST'])
def submit():
    data = request.get_json()  # Extract data from the JSON POST request
    text = data.get('text')
    url = data.get('url')
    name = data.get("name")
    # Select player from memes by name
    player = [player for player in game.memes.keys() if player.name == name]
    game.submit(player, url, text)
    return render_template('meme_submit.html')


@app.route('/wait_for_game_start')
def wait_for_game_start():
    # return to /login if the user aren't in the game
    if not is_valid_session():
        print("12345")
        return redirect(url_for('login'))

    return render_template('lobby.html')


# view all memes in database
@app.route('/view')
def view_meme():
    return render_template("view_memes.html")


# view specific memes, enables sharing meme urls
@app.route('/view/<meme_url>')
def view(meme_url):
    print(meme_url)
    return meme_url


@app.route('/admin_panel')
def admin_panel():
    return render_template("admin_panel.html")


@app.route('/admin_panel/game_state')
def admin_state_game():
    match game.phase:
        case GamePhase.Waiting:
            game.phase = GamePhase.Creating
        case _:
            game.phase = GamePhase.Waiting

    return redirect(url_for("admin_panel"))


#@app.route('/admin_panel/start_game')
#def admin_start_game():
#    return redirect(url_for("admin_panel"))


if __name__ == '__main__':
    # initialize flask session
    current_session.init_app(app)
    app.run()
