from tinydb import TinyDB
from .player import Player


class Match:
    """ A Match object contain the 2 player object and score """
    def __init__(self, match_id=None, player1=None, player2=None):
        """ init database """
        db = TinyDB("./db.json")
        self.match_table = db.table("match")

        # init for existing match
        if match_id is not None:
            match_serialized = self.match_table.get(all, int(match_id))
            self.player1 = Player(match_serialized["player1"])
            self.player2 = Player(match_serialized["player2"])
            self.player1_score = match_serialized["player1_score"]
            self.player2_score = match_serialized["player2_score"]
            self.match_id = match_id

        # init for new match
        else:
            self.player1 = player1
            self.player2 = player2
            self.player1_score = 0
            self.player2_score = 0
            self.match_id = self.save_new_match()

    def save_new_match(self):
        """save new match in database"""
        match_info = {}
        match_info["player1"] = self.player1.player_id
        match_info["player2"] = self.player2.player_id
        match_info["player1_score"] = self.player1_score
        match_info["player2_score"] = self.player2_score
        return self.match_table.insert(match_info)

    def save_match_result(self):
        """Update player score in database"""
        self.match_table.update({
            "player1_score": self.player1_score,
            "player2_score": self.player2_score
            },
            doc_ids=[self.match_id])
