import numbers
from view.view import View
from model.player import Player, PlayerDataBase
from model.tournament import Tournament, TournamentDataBase, Round


class Controller:
    def __init__(self):
        self.players = []
        self.view = View()
        self.players_data_base = PlayerDataBase()
        self.tournament_data_base = TournamentDataBase()

    def run(self):
        """Run main programme"""
        end_loop = False
        while not end_loop:
            choice = self.view.show_main_menu()
            match choice:
                case "1":
                    self.players_data_base.save_new_player(self.view.enter_player_info())
                case "2":
                    self.create_tournament()
                case "3":
                    self.backup_tournament()
                case "4":
                    end_loop = True

    def create_tournament(self):
        """create new tournament in database"""
        tournament_info = self.view.enter_tournament_info()
        players = []
        for player in range(int(tournament_info["number_of_player"])):
            players.append(self.view.choice_player(self.players_data_base.get_player_available_list(players)))
        tournament_info["player_id"] = players
        tournament_info["tournament_id"] = self.tournament_data_base.save_tournament(tournament_info, True)
        self.tournament = Tournament(tournament_info)
        self.run_tournament()

    def backup_tournament(self):
        """get back an existing tournament from the database"""
        tournament_info = self.tournament_data_base.get_tounament(
            self.view.choice_tournament(self.tournament_data_base.available_tournament_list())
        )
        self.tournament = Tournament(tournament_info)
        self.run_tournament()

    def launch_round(self, tournament_status):
        self.round = Round(self.tournament)
        if not tournament_status:
            self.round.first_round()
            self.tournament.round.append(self.round.save_round())

        else:
            self.round.start_round()
            self.tournament.round.append(self.round.save_round())
        self.tournament.round.append(round)
        print(self.tournament.round)

    def run_tournament(self):
        end_loop = False
        while not end_loop:
            if len(self.tournament.round) == 0:
                tournament_status = False
            else:
                tournament_status = True
            choice = self.view.show_tournament_menu(tournament_status)
            match choice:
                case "1":
                    self.launch_round(tournament_status)
                case "2":
                    pass
                case "3":
                    end_loop = True
