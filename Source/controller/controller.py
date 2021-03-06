from view.utils import clean_screen
from view.mainview import MainView
from view.tournamentview import TournamentView
from model.player import Player, PlayerDataBase
from model.tournament import Tournament, TournamentDataBase
from model.round import Round


class Controller:
    def __init__(self):
        self.players = []
        self.mainview = MainView()
        self.tournamentview = TournamentView()
        self.round_status = ""
        self.players_data_base = PlayerDataBase()
        self.tournament_data_base = TournamentDataBase()

    def run(self):
        """Run main programme"""
        end_loop = False
        while not end_loop:
            choice = self.mainview.show_main_menu()
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
            choice = self.mainview.show_tournament_menu()
            match choice:
                case "1":
                    if self.players_data_base.get_number_of_player() < 8:
                        self.mainview.show_number_of_player_warning()
                    else:
                        self.create_tournament()
                case "2":
                    if len(self.tournament_data_base.get_available_tournament_list()) == 0:
                        self.mainview.show_number_of_tournament_warning()
                    else:
                        self.backup_tournament()
                case "3":
                    tournament_choice = (
                        self.mainview.show_tournament_list(self.tournament_data_base.get_tournament_list())
                        )
                    if tournament_choice != "":
                        self.tournament = tournament_choice
                        self.run_tournament()
                case "4":
                    end_loop = True

    def player_management_menu(self):
        """selector for player management menu"""
        end_loop = False
        while not end_loop:
            choice = self.mainview.show_player_management_menu()
            match choice:
                case "1":
                    order_type = self.mainview.ask_for_order_type()
                    loop = True
                    while loop:
                        playerchoice = self.mainview.show_player_list(
                            self.players_data_base.get_player_list(), order_type
                            )
                        if playerchoice != "":
                            playerchoice.update_ranking(self.mainview.change_player_ranking(playerchoice))
                        else:
                            loop = False
                            clean_screen()
                case "2":
                    Player(player_info=self.mainview.enter_player_info())
                case "3":
                    end_loop = True

    def create_tournament(self):
        """create new tournament and launch it"""
        tournament_info = self.tournamentview.enter_tournament_info()
        players = []
        for player in range(int(tournament_info["number_of_player"])):
            players.append(
                self.tournamentview.choice_player(self.players_data_base.get_player_available_list(players))
                )
        tournament_info["players"] = players
        tournament_info["rounds"] = []
        self.tournament = Tournament(tournament_info=tournament_info)
        self.run_tournament()

    def backup_tournament(self):
        """get back an existing tournament from the database"""
        tournament_choice = (
            self.mainview.show_tournament_list(self.tournament_data_base.get_available_tournament_list())
            )
        if tournament_choice != "":
            self.tournament = tournament_choice
            self.run_tournament()

    def launch_round(self):
        """ create new round in rounds list """
        self.tournament.rounds.append(Round(self.tournament))
        self.tournament.update()
        for match in self.tournament.rounds[-1].matchs:
            self.tournamentview.show_match_info(match)

    def define_score(self):
        """ Change player score depend of who win"""
        for match in self.tournament.rounds[-1].matchs:
            choice = self.tournamentview.enter_score_choice(match)
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
        """ Main tournament choice menu """
        end_loop = False
        while not end_loop:

            # looking for tournament status
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
            # launch function depend of player choice and tournament status
            choice = self.tournamentview.show_selected_tournament_menu(self.tournament.name, tournament_status)
            match choice:
                case "1":
                    if tournament_status == "enter_score":
                        self.define_score()
                    elif tournament_status == "start_new_round" or tournament_status == "not_started":
                        self.launch_round()
                    elif tournament_status == "finish":
                        loop = True
                        while loop:
                            playerchoice = self.tournamentview.show_score(self.tournament.get_score())
                            if playerchoice != "":
                                playerchoice.update_ranking(self.mainview.change_player_ranking(playerchoice))
                            else:
                                loop = False
                                clean_screen()
                case "2":
                    if tournament_status != "finish":
                        loop = True
                        while loop:
                            playerchoice = self.tournamentview.show_score(self.tournament.get_score())
                            if playerchoice != "":
                                playerchoice.update_ranking(self.mainview.change_player_ranking(playerchoice))
                            else:
                                loop = False
                                clean_screen()
                    else:
                        order_type = self.mainview.ask_for_order_type()
                        loop = True
                        while loop:
                            playerchoice = self.mainview.show_player_list(self.tournament.players, order_type)
                            if playerchoice != "":
                                playerchoice.update_ranking(self.mainview.change_player_ranking(playerchoice))
                            else:
                                loop = False
                                clean_screen()
                case "3":
                    if tournament_status != "finish":
                        order_type = self.mainview.ask_for_order_type()
                        loop = True
                        while loop:
                            playerchoice = self.mainview.show_player_list(self.tournament.players, order_type)
                            if playerchoice != "":
                                playerchoice.update_ranking(self.mainview.change_player_ranking(playerchoice))
                            else:
                                loop = False
                                clean_screen()
                    else:
                        self.tournamentview.show_match_list(self.tournament.rounds)
                case "4":
                    if tournament_status != "finish":
                        self.tournamentview.show_match_list(self.tournament.rounds)
                    else:
                        end_loop = True
                case "5":
                    if tournament_status != "finish":
                        end_loop = True
