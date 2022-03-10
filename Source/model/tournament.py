from datetime import datetime
from tabnanny import check
from tinydb import TinyDB, Query, where
from .player import Player


class TournamentDataBase:
    def __init__(self):
        db = TinyDB("./db.json")
        self.tournament_table = db.table("tournaments")

    def available_tournament_list(self):
        """get list of unfinished tournament from the database"""
        tournament = Query()
        tournament_line = self.tournament_table.search(tournament.end_date == "")
        return tournament_line

class Tournament:
    def __init__(self, tournament_id=None, tournament_info=None):
        """Init tournament object with tournament info

        Args :
            tournament_info : all tournament data in list
        """
        db = TinyDB("./db.json")
        self.tournament_table = db.table("tournaments")
        if tournament_id != None:
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
            player = Player(player_id)
            self.players.append(player)
        self.rounds = []
        for round_id in tournament_info["rounds"]:
            round = Round(self, round_id)
            self.rounds.append(round)
        if tournament_id is None:
            self.tournament_id = self.save_new_tournament()

    def save_new_tournament(self):
        tournament_info = {}
        tournament_info["name"] = self.name
        tournament_info["place"] = self.place
        tournament_info["number_of_round"] = self.number_of_round
        tournament_info["description"] = self.description
        tournament_info["time_controle"] = self.time_controle
        tournament_info["number_of_player"] = self.number_of_player
        tournament_info["start_date"] = self.start_date
        tournament_info["end_date"] = self.end_date
        tournament_info["players"] = [player.player_id for player in self.players]
        tournament_info["rounds"] = [round.round_id for round in self.rounds]
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


class Round:
    def __init__(self, tournament, round_id=None):
        db = TinyDB("./db.json")
        self.round_table = db.table("round")
        self.tournament = tournament
        self.half_of_player = int(len(self.tournament.players) / 2)
        if round_id != None:
            self.round_id = round_id
            round_serialized = self.round_table.get(all, int(round_id))
            match_id = round_serialized["matchs"]
            self.matchs = []
            for match in match_id:
                self.matchs.append(Match(match_id=match))
        else:
            self.matchs = []
            if len(self.tournament.rounds) == 0:
                self.first_round()
            else:
                self.start_round()
            self.round_id = self.save_round()
    
    def __str__(self):
        return self.round_id
        
    def save_round(self):
        round_info = {}
        round_info["matchs"] = [match.match_id for match in self.matchs]
        return self.round_table.insert(round_info)

    def first_round(self):
        sorted_players = self.sorted_by_ranking()
        for player in range(self.half_of_player):
            self.matchs.append(Match(player1=sorted_players[player], player2=sorted_players[player + self.half_of_player]))

    def start_round(self):
        sorted_player = self.sorted_by_score()
        sorted_player_left = []
        for player in sorted_player:
            sorted_player_left.append(player[0])
        for player in range(self.half_of_player):
            print("test player number : " + str(player))
            print(sorted_player_left)
            player1 = sorted_player_left[0]
            del sorted_player_left[0]
            not_meet_player = self.check_previous_match(player1, sorted_player_left)
            player2 = not_meet_player[0]
            del sorted_player_left[not_meet_player[1]]
            self.matchs.append(Match(player1=player1, player2=player2))

    def check_previous_match(self, player1, sorted_player_left):
        player_index = 0
        meet = False
        for playerleft in sorted_player_left:
            print(player1.firstname )
            print(playerleft.firstname)
            for round in self.tournament.rounds:
                for match in round.matchs:
                    if player1.player_id == match.player1.player_id and playerleft.player_id == match.player2.player_id:
                        print(player1.firstname + ' a deja rencontrer ' + playerleft.firstname)
                        meet = True
                    elif player1.player_id == match.player2.player_id and playerleft.player_id == match.player1.player_id:
                        print(player1.firstname + ' a deja rencontrer ' + playerleft.firstname)
                        meet = True
            if meet == False:
                return [playerleft, player_index]
            player_index +=1
        return [sorted_player_left[0], 0]

    def sorted_by_ranking(self):
        sorted_players = sorted(self.tournament.players, key=lambda player: player.ranking, reverse=True)
        return sorted_players
    
    def sorted_by_score(self):
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


class Match:
    def __init__(self, match_id=None, player1=None, player2=None):
        # Database
        db = TinyDB("./db.json")
        self.match_table = db.table("match")
        if match_id != None:
            # init match
            match_serialized = self.match_table.get(all, int(match_id))
            self.player1 = Player(match_serialized["player1"])
            self.player2 = Player(match_serialized["player2"])
            self.player1_score = match_serialized["player1_score"]
            self.player2_score = match_serialized["player2_score"]
            self.match_id = match_id
        else:
            self.player1 = player1
            self.player2 = player2
            self.player1_score = 0
            self.player2_score = 0
            self.match_id = self.save_new_match()

    def save_new_match(self):
        match_info = {}
        match_info["player1"] = self.player1.player_id
        match_info["player2"] = self.player2.player_id
        match_info["player1_score"] = self.player1_score
        match_info["player2_score"] = self.player2_score
        return self.match_table.insert(match_info)

    #def update_score(self, score_player1, score_player2):
     #   self.player1_score = score_player1
      #  self.player2_score = score_player2

    def save_match_result(self):
        self.match_table.update({"player1_score": self.player1_score, "player2_score": self.player2_score}, doc_ids=[self.match_id])
