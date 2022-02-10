from datetime import datetime

from Player.Player import Player

class Tournament:
    def __init__(self, new_tournament=False):
        if new_tournament == True:
            self.new_tournaments()
        else:
            pass
    
    def new_tournaments(self):
        self.nom = input("Nom du tournois : ")
        self.lieu = input("Lieu du tournois : ")
        self.date_de_debut = datetime.now()
        self.nombre_de_joueur = "8"
        self.joueurs = self.get_players_choice()
        self.nombre_de_tour = input("nombre de tour (par defaut : 4) : ") or "4"
        self.tournees = ()
        print("type de controle du temps :")
        print("1 : Bullet")
        print("2 : Blitz")
        print("3 : Coup rapide")
        good_choice = False
        while good_choice == False:
            choice = input("choix : ")
            match choice:
                case "1":
                    good_choice = True
                    self.controle_du_temps = "1"
                case "2":
                    good_choice = True
                    self.controle_du_temps = "2"
                case "3":
                    good_choice = True
                    self.controle_du_temps = "3"
                case _:
                    print("le choix entré ne corespond pas à un choix valide. choisisser à nouveau")

        self.description = input("Description : ")
        
    
    def get_players_choice(self):
        players = []
        for player_number in range(int(self.nombre_de_joueur)):
            player = Player()


class Tours:
    def __init__(self, nombre_de_match):
        self.nombre_de_match = nombre_de_match
        self.datetime_debut = datetime.now()


class Match:
    def __init__(self, id_joueur1, id_joueur2):
        self.id_joueur1 = id_joueur1
        self.id_joueur2 = id_joueur2

    def register_result():
        pass