class Player:

    def __init__(self, id_, name):
        self.id = id_
        self.name = name
        self.upvote = 0
        self.downvote = 0


class Game:

    def __init__(self, max_player_count=-1, max_rounds=5):
        self.max_player_count = max_player_count
        self.max_rounds = max_rounds
        self.__memes = {}
        self.round = 0
        self.__round_activ = False

    def add_player(self, player: Player):
        if self.max_player_count == len(self.__memes) or self.__round_activ:
            return False

        self.__memes[player] = None

        return True

    def submit(self, player: Player, meme_id, text):
        self.__memes[player] = [meme_id, text]

        print(f"der Player{player.name} hat ein meme hochgeladen")
        if all([m for m in self.__memes.values()]):
            # create meme is finish
            return

