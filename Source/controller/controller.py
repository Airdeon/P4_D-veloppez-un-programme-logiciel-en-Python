from view.view import View
from model.player import Player
from model.tournament import Tournament

class Controller:
    def __init__(self, view):
        self.players = []
        self.view = View

    def run(self):
        end_loop = False
        while not end_loop:
            choice = self.view.show_main_menu()
            match choice:
                case "1":
                    Player(True)
                case "2":
                    Tournament(True)
                case "3":
                    Tournament()
                case "4":
                    end_loop = True
