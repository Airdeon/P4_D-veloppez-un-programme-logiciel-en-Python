from view.view import View
from model.player import Player, PlayerDataBase
from model.tournament import Tournament, TournamentDataBase


class Controller:
    def __init__(self):
        self.players = []
        self.view = View()
        self.players_data_base = PlayerDataBase()
        self.tournament_data_base = TournamentDataBase()

    def run(self):
        end_loop = False
        while not end_loop:
            choice = self.view.show_main_menu()
            match choice:
                case "1":
                    self.players_data_base.save_new_player(self.view.enter_player_info())
                case "2":
                    self.create_tournament()
                case "3":
                    Tournament()
                case "4":
                    end_loop = True

    def create_tournament(self):
        tournament_info = self.view.enter_tournament_info()
        players = []
        for player in range(int(tournament_info["nombre_de_joueur"])):
            players.append(self.view.choice_player(self.players_data_base.get_player_available_list(players)))
        tournament_info['player_id'] = players
        tournament_info['tournament_id'] = self.tournament_data_base.save_tournament(tournament_info, True)
        self.tournament = Tournament(tournament_info)

    def backup_tournament(self):
        tournament_info = self.tournament_data_base.get_tounament(self.view.choice_tournament(self.tournament_data_base.available_tournament_list()))
        self.tournament = Tournament(tournament_info)