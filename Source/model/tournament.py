from datetime import datetime
from tinydb import TinyDB, Query
from .player import Player
from .round import Round


class TournamentDataBase:
    def __init__(self):
        db = TinyDB("./db.json")
        self.tournament_table = db.table("tournaments")

    def get_available_tournament_list(self):
        """get list of unfinished tournament from the database"""
        tournament = Query()
        tournament_line = self.tournament_table.search(tournament.end_date == "")
        tournament_list = []
        for tournament in tournament_line:
            tournament_list.append(Tournament(tournament_id=tournament.doc_id))
        return tournament_list

    def get_tournament_list(self):
        tournament_list = []
        for tournament in self.tournament_table:
            tournament_list.append(Tournament(tournament_id=tournament.doc_id))
        return tournament_list


class Tournament:
    def __init__(self, tournament_id=None, tournament_info=None):
        """Init tournament object with tournament info

        Args :
            tournament_info : all tournament data in list
        """
        db = TinyDB("./db.json")
        self.tournament_table = db.table("tournaments")
        if tournament_id is not None:
            tournament_info = self.tournament_table.get(all, int(tournament_id))
            self.tournament_id = tournament_id
            self.start_date = tournament_info["start_date"]
            self.end_date = tournament_info["end_date"]
        else:
            self.start_date = str(datetime.now())
            self.end_date = ""
        self.name = tournament_info["name"]
        self.place = tournament_info["place"]
        self.number_of_round = tournament_info["number_of_round"]
        self.description = tournament_info["description"]
        self.time_controle = tournament_info["time_controle"]
        self.number_of_player = tournament_info["number_of_player"]
        self.players = []
        for player_id in tournament_info["players"]:
            player = Player(player_id=player_id)
            self.players.append(player)
        self.rounds = []
        for round_id in tournament_info["rounds"]:
            round = Round(self, round_id)
            self.rounds.append(round)
        if tournament_id is None:
            self.tournament_id = self.save_new_tournament()

    def save_new_tournament(self):
        tournament_info = {
            "name": self.name,
            "place": self.place,
            "number_of_round": self.number_of_round,
            "description": self.description,
            "time_controle": self.time_controle,
            "number_of_player": self.number_of_player,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "players": [player.player_id for player in self.players],
            "rounds": [round.round_id for round in self.rounds],
        }
        return self.tournament_table.insert(tournament_info)

    def update(self):
        self.tournament_table.update({
            "rounds": [round.round_id for round in self.rounds],
            "end_date": self.end_date,
            },
            doc_ids=[self.tournament_id])

    def get_score(self):
        player_score = {}
        for round in self.rounds:
            for match in round.matchs:
                for player in self.players:
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

    def finish_tournament(self):
        self.end_date = str(datetime.now())
        self.update()