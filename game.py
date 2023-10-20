from typing import Dict


class Player:

    def __init__(self, name, id_=None):
        self.id = id_
        self.name = name
        self.upvote = 0
        self.downvote = 0


class Game:
    def __init__(self, max_player_count=-1, max_rounds=5):
        self.max_player_count = max_player_count
        self.max_rounds = max_rounds
        self.memes: Dict[Player, list] = {}
        self.round = 0
        self.round_activ = False

    def add_player(self, player: Player):
        if self.round_activ:
            return False

        # Activate the round when the maximum player count is reached
        self.round_activ = (self.max_player_count == len(self.memes) - 1)

        self.memes[player] = None

        return True

    def submit(self, player: Player, meme_id, text):
        self.memes[player] = [meme_id, text]

        print(f"der Player{player.name} hat ein meme hochgeladen")
        if all([m for m in self.memes.values()]):
            # create meme is finish
            return

