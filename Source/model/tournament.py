from datetime import datetime
from tinydb import TinyDB, Query
from .player import Player


class TournamentDataBase:
    def __init__(self):
        db = TinyDB("./db.json")
        self.tournament_table = db.table("tournaments")

    def save_tournament(self, tournament_info, new=False):
        """Save tournament in database"""

        if new:
            tournament_info["start_date"] = str(datetime.now())
            tournament_info["end_date"] = ""
            tournament_info["round_id"] = []
            self.tournament_table.insert(tournament_info)
            return self.tournament_table.count(all)
        else:
            # a faire : tournament info serialisé
            self.tournament_table.update(set(self.id_tournament, tournament_info))

    def available_tournament_list(self):
        """get list of unfinished tournament from the database"""
        tournament = Query()
        tournament_line = self.tournament_table.search(tournament.end_date == "")
        tournament_list = []
        tournament_count = 0
        for tournament in tournament_line:
            tournament_count += 1
            tournament_list.append(str(tournament_count) + " : " + tournament["name"])
        return tournament_list

    def get_tounament(self, tournament_choice):
        tournament = Query()
        tournament_line = self.tournament_table.search(tournament.end_date == "")
        tournament_info = tournament_line[int(tournament_choice) - 1]
        tournament_info["tournament_id"] = tournament_line[int(tournament_choice) - 1].doc_id
        return tournament_info


class Tournament:
    def __init__(self, tournament_info):
        """Init tournament object with tournament info

        Args :
            tournament_info : all tournament data in list
        """
        # Creation of tournament database object
        self.tournament_database = TournamentDataBase()
        # Tournament initialisation
        self.tournament_id = tournament_info["tournament_id"]
        self.name = tournament_info["name"]
        self.place = tournament_info["place"]
        self.round_number = tournament_info["round_number"]
        self.description = tournament_info["description"]
        self.time_controle = tournament_info["time_controle"]
        self.number_of_player = tournament_info["number_of_player"]
        self.players = []
        for player_id in tournament_info["player_id"]:
            player = Player(player_id)
            self.players.append(player)
        self.round = []
        for round_id in tournament_info["round_id"]:
            round = Round(round_id)
            self.round.append(round)
        self.start_date = ["start_date"]
        self.end_date = ["end_date"]

    def save(self):
        self.tournament_database.save_tournament(self, False)

class RoundDataBase:
    def __init__(self, tournament):
        db = TinyDB("./db.json")
        self.round_table = db.table("round")
    
    def save_new_round(self):
        round_info = []
        round_info['match'] = self.match
        self.round_table.insert(round_info)
        return self.round_table.count(all)

class Round:
    def __init__(self, tournament):
        db = TinyDB("./db.json")
        self.round_table = db.table("round")
        self.match = []
        self.tournament = tournament
        self.half_of_player = int(int(self.tournament.number_of_player) / 2)

    def first_round(self)
        sorted_player = self.sorted_by_ranking()
        for player in range(self.half_of_player):
            self.match.append(Match(sorted_player[player], sorted_player[player + self.half_of_player]))

    def start_round(self):
        pass

    def save_round(self):
        round_info = []
        round_info['match'] = self.match
        self.round_table.insert(round_info)
        return self.round_table.count(all)

    def sorted_by_ranking(self):
        sorted_player = sorted(self.tournament.players, key=lambda player: player.ranking, reverse=True)
        return sorted_player


class Match:
    def __init__(self, player1, player2):
        # Database
        db = TinyDB("./db.json")
        self.match_table = db.table("match")
        # init player
        self.player1 = player1
        self.player2 = player2
        self.player1_score = 0
        self.player2_score = 0
        self.match_id = self.save_new_match()
    
    def save_new_match(self):
        match_info = []
        match_info['player1'] = self.player1.player_id
        match_info['player2'] = self.player2.player_id
        match_info['player1_score'] = 0
        match_info['player2_score'] = 0
        self.match_table.insert(match_info)
        return self.match_table.count(all)
    
    def update_score(self, match_id, score_player1, score_player2):
        self.match_table.update(set(self.match_id, match_info))

    def register_result():
        pass
