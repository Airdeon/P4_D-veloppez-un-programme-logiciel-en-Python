from view.view import View
from model.player import Player, PlayerDataBase
from model.tournament import Tournament, TournamentDataBase
from model.round import Round


class Controller:
    def __init__(self):
        self.players = []
        self.view = View()
        self.round_status = ""
        self.players_data_base = PlayerDataBase()
        self.tournament_data_base = TournamentDataBase()

    def run(self):
        """Run main programme"""
        end_loop = False
        while not end_loop:
            choice = self.view.show_main_menu()
            match choice:
                case "1":
                    self.tournament_menu()
                case "2":
                    self.player_management_menu()
                case "3":
                    end_loop = True

    def tournament_menu(self):
        """Selector for tournament menu"""
        end_loop = False
        while not end_loop:
            choice = self.view.show_tournament_menu()
            match choice:
                case "1":
                    self.create_tournament()
                case "2":
                    self.backup_tournament()
                case "3":
                    pass
                case "4":
                    end_loop = True

    def player_management_menu(self):
        """selector for player management menu"""
        end_loop = False
        while not end_loop:
            choice = self.view.show_player_management_menu()
            match choice:
                case "1":
                    self.view.show_player_list(self.players_data_base.get_player_list())
                case "2":
                    Player(player_info=self.view.enter_player_info())
                case "3":
                    end_loop = True

    def create_tournament(self):
        """create new tournament and launch it"""
        tournament_info = self.view.enter_tournament_info()
        players = []
        for player in range(int(tournament_info["number_of_player"])):
            players.append(self.view.choice_player(self.players_data_base.get_player_available_list(players)))
        tournament_info["players"] = players
        tournament_info["rounds"] = []
        self.tournament = Tournament(tournament_info=tournament_info)
        self.run_tournament()

    def backup_tournament(self):
        """get back an existing tournament from the database"""
        tournament_available_list = self.tournament_data_base.available_tournament_list()
        tournament_choice = int(self.view.choice_tournament(tournament_available_list)) - 1
        self.tournament = Tournament(tournament_id=int(tournament_available_list[tournament_choice].doc_id))
        self.run_tournament()

    def launch_round(self):
        self.tournament.rounds.append(Round(self.tournament))
        self.round_status = "started"
        self.tournament.update()
        for match in self.tournament.rounds[-1].matchs:
            self.view.show_match_info(match)

    def define_score(self):
        for match in self.tournament.rounds[-1].matchs:
            choice = self.view.enter_score_choice(match)
            match choice:
                case "1":
                    match.player1_score = 1
                case "2":
                    match.player1_score = 0.5
                    match.player2_score = 0.5
                case "3":
                    match.player2_score = 1
            match.save_match_result()
            self.tournament.rounds[-1].update_end_datetime()
            if int(self.tournament.number_of_round) == len(self.tournament.rounds):
                self.tournament.finish_tournament()
            self.round_status = ""

    def run_tournament(self):
        end_loop = False
        while not end_loop:
            if len(self.tournament.rounds) < int(self.tournament.number_of_round):
                tournament_status = "round"
            else:
                tournament_status = "finish"

            choice = self.view.show_selected_tournament_menu(self.tournament.name, self.round_status, tournament_status)
            match choice:
                case "1":
                    if self.round_status == "starded":
                        self.define_score()
                    elif tournament_status == "round":
                        self.launch_round()
                    elif tournament_status == "finish" and self.round_status == "":
                        self.view.show_score(self.tournament.get_score())
                case "2":
                    pass
                case "3":
                    end_loop = True
