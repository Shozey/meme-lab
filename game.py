from typing import Dict
from enum import IntEnum, auto


class GamePhase(IntEnum):
    Waiting = auto()
    Creating = auto()
    Viewing = auto()
    Results = auto()


class Player:

    def __init__(self, name, id_=None):
        self.id = id_
        self.name = name
        self.upvote = 0
        self.downvote = 0


# phase 0 in lobby warten bis alle spieler online sind
# phase 1 meme erstellen
# phase 2 meme anschauen


class Game:
    def __init__(self, max_rounds=1):
        self.max_rounds = max_rounds
        self.memes: Dict[Player, list] = {}
        self.round = 0
        self.phase = GamePhase.Waiting

    def add_player(self, player: Player):
        if self.phase:
            return False

        self.memes[player] = None

        return True

    def start_game(self):
        self.phase = True

    def submit(self, player: Player, meme_id, text):
        self.memes[player] = [meme_id, text]

        print(f"der Player {player.name} hat ein meme hochgeladen")
        if all([m for m in self.memes.values()]):
            # creating memes is finish
            return True
        return False

