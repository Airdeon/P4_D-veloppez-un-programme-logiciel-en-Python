from Player.Player import Player
from Tournament.Tournament import Tournament, Tours, Match
from Menu.MenuPrincipale import menu_principale
from controller.controller import Controller
from view.view import View


def main():
    chess = Controller()
    chess.run()


if __name__ == "__main__":
    main()
