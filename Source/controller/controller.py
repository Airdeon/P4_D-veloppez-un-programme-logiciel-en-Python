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
                    if self.players_data_base.get_number_of_player() < 8:
                        self.view.show_number_of_player_warning()
                    else:
                        self.create_tournament()
                case "2":
                    if len(self.tournament_data_base.get_available_tournament_list()) == 0:
                        self.view.show_number_of_tournament_warning()
                    else:
                        self.backup_tournament()
                case "3":
                    tournament_choice = self.view.show_tournament_list(self.tournament_data_base.get_tournament_list())
                    if tournament_choice != "":
                        self.tournament = tournament_choice
                        self.run_tournament()
                case "4":
                    end_loop = True

    def player_management_menu(self):
        """selector for player management menu"""
        end_loop = False
        while not end_loop:
            choice = self.view.show_player_management_menu()
            match choice:
                case "1":
                    playerchoice = self.view.show_player_list(self.players_data_base.get_player_list())
                    if playerchoice != "":
                        playerchoice.update_ranking(self.view.change_player_ranking(playerchoice))
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
        tournament_choice = self.view.show_tournament_list(self.tournament_data_base.get_available_tournament_list())
        if tournament_choice != "":
            self.tournament = tournament_choice
            self.run_tournament()

    def launch_round(self):
        self.tournament.rounds.append(Round(self.tournament))
        self.tournament.update()
        for match in self.tournament.rounds[-1].matchs:
            self.view.show_match_info(match)

    def define_score(self):
        print(self.tournament.rounds)
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
            self.tournament.rounds[-1].round_status = ""

    def run_tournament(self):
        end_loop = False
        while not end_loop:

            # Find tournament status
            if len(self.tournament.rounds) == 0:
                tournament_status = "not_started"
            elif len(self.tournament.rounds) == int(self.tournament.number_of_round):
                if self.tournament.rounds[-1].end_datetime == "":
                    tournament_status = "enter_score"
                else:
                    tournament_status = "finish"
            else:
                if self.tournament.rounds[-1].end_datetime == "":
                    tournament_status = "enter_score"
                else:
                    tournament_status = "start_new_round"

            choice = self.view.show_selected_tournament_menu(self.tournament.name, tournament_status)
            match choice:
                case "1":
                    if tournament_status == "enter_score":
                        self.define_score()
                    elif tournament_status == "start_new_round" or tournament_status == "not_started":
                        self.launch_round()
                    elif tournament_status == "finish":
                        playerchoice = self.view.show_score(self.tournament.get_score())
                        if playerchoice != "":
                            playerchoice.update_ranking(self.view.change_player_ranking(playerchoice))
                case "2":
                    if tournament_status != "finish":
                        playerchoice = self.view.show_score(self.tournament.get_score())
                        if playerchoice != "":
                            playerchoice.update_ranking(self.view.change_player_ranking(playerchoice))
                    else:
                        end_loop = True
                case "3":
                    if tournament_status != "finish":
                        end_loop = True
