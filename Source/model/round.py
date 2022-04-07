from tinydb import TinyDB
from datetime import datetime
from .match import Match


class Round:
    def __init__(self, tournament, round_id=None):
        """ Init Round Object """
        db = TinyDB("./db.json")
        self.round_table = db.table("round")
        self.tournament = tournament
        self.half_of_player = int(len(self.tournament.players) / 2)
        # if round already exist
        if round_id is not None:
            self.round_id = round_id
            round_serialized = self.round_table.get(all, int(round_id))
            self.round_name = round_serialized["round_name"]
            match_id = round_serialized["matchs"]
            self.start_datetime = round_serialized["start_datetime"]
            self.end_datetime = round_serialized["end_datetime"]
            self.matchs = []
            for match in match_id:
                self.matchs.append(Match(match_id=match))
        else:
            self.round_name = "round " + str(len(self.tournament.rounds) + 1)
            self.matchs = []
            if len(self.tournament.rounds) == 0:
                self.first_round()
            else:
                self.start_round()
            self.start_datetime = str(datetime.now())
            self.end_datetime = ""
            self.round_id = self.save_round()

    def save_round(self):
        """ save round in database and return id of the entry"""
        round_info = {}
        round_info["round_name"] = self.round_name
        round_info["matchs"] = [match.match_id for match in self.matchs]
        round_info["start_datetime"] = self.start_datetime
        round_info["end_datetime"] = self.end_datetime
        return self.round_table.insert(round_info)

    def update_end_datetime(self):
        """ set end date in database when round is finish """
        self.end_datetime = str(datetime.now())
        self.round_table.update({"end_datetime": self.end_datetime}, doc_ids=[self.round_id])

    def first_round(self):
        """ first round of tournament """
        sorted_players = self.sorted_by_ranking()
        for player in range(self.half_of_player):
            self.matchs.append(
                Match(player1=sorted_players[player], player2=sorted_players[player + self.half_of_player])
                )

    def start_round(self):
        """ start round of tournament exept first one """
        sorted_player = self.sorted_by_score()
        sorted_player_left = []
        for player in sorted_player:
            sorted_player_left.append(player[0])
        for player in range(self.half_of_player):
            player1 = sorted_player_left[0]
            del sorted_player_left[0]
            not_meet_player = self.check_previous_match(player1, sorted_player_left)
            player2 = not_meet_player[0]
            del sorted_player_left[not_meet_player[1]]
            self.matchs.append(Match(player1=player1, player2=player2))

    def check_previous_match(self, player1, sorted_player_left):
        """ check if 2 player already meet in previous round """
        player_index = 0
        meet = False
        for playerleft in sorted_player_left:
            for round in self.tournament.rounds:
                for match in round.matchs:
                    if (player1.player_id == match.player1.player_id
                            and playerleft.player_id == match.player2.player_id):
                        meet = True
                    elif (player1.player_id == match.player2.player_id
                            and playerleft.player_id == match.player1.player_id):
                        meet = True
            if not meet:
                return [playerleft, player_index]
            player_index += 1
        return [sorted_player_left[0], 0]

    def sorted_by_ranking(self):
        """ sorted player by their ranking"""
        sorted_players = sorted(self.tournament.players, key=lambda player: player.ranking, reverse=True)
        return sorted_players

    def sorted_by_score(self):
        """ sorted player by their score (and ranking if score is same) """
        player_score = {}
        for round in self.tournament.rounds:
            for match in round.matchs:
                for player in self.tournament.players:
                    if player.player_id == match.player1.player_id:
                        if player in player_score:
                            player_score[player] += match.player1_score
                        else:
                            player_score[player] = match.player1_score
                    elif player.player_id == match.player2.player_id:
                        if player in player_score:
                            player_score[player] += match.player2_score
                        else:
                            player_score[player] = match.player2_score

        return sorted(player_score.items(), key=lambda x: (x[1], x[0].ranking), reverse=True)
