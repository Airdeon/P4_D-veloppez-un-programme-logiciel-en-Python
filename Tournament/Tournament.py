from datetime import datetime
from tinydb import TinyDB, Query
from Player.Player import Player



class Tournament:
    db = TinyDB('./db.json')
    tournament_table = db.table('tournaments')


    def __init__(self, new_tournament=False):
        if new_tournament == True:
            self.new_tournaments()
        else:
            self.backup_tournament()
    

    def new_tournaments(self):
        self.nom = input("Nom du tournois : ")
        self.lieu = input("Lieu du tournois : ")
        self.date_de_debut = datetime.now()
        self.date_de_fin = ""
        self.nombre_de_tour = input("nombre de tour (par defaut : 4) : ") or "4"
        self.tour = []
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
        self.nombre_de_joueur = "8"
        self.joueurs = self.get_players_choice()
        self.save_tournament(True)
        
    
    def get_players_choice(self):
        players = []
        for player_number in range(int(self.nombre_de_joueur)):
            player = Player(False, players)
            players.append(player)
        return players
    
    def backup_tournament(self):
        tournament = Query()
        tournament_line_serialized = self.tournament_table.search(tournament.date_de_fin == "")
        backup_tournament_number = 0
        for tournament in tournament_line_serialized:
            backup_tournament_number += 1
            print(str(backup_tournament_number) + " : " + tournament['nom'])
            
        print("entrer le numero du tournois à continuer")
        good_choice = False
        while good_choice == False:
            choice = input("choix : ")
            if int(choice) > 0 and int(choice) <= backup_tournament_number:
                good_choice=True
                backup_tournament = tournament_line_serialized[int(choice)]
                self.nom = backup_tournament['nom']
                self.lieu = backup_tournament['lieu']
                self.date_de_debut = backup_tournament['date_de_debut']
                self.date_de_fin = backup_tournament['date_de_fin']
                self.nombre_de_tour = backup_tournament['nombre_de_tour']
                self.controle_du_temps = backup_tournament['controle_du_temps']
                self.description = backup_tournament['description']
                self.nombre_de_joueur = backup_tournament['nombre_de_joueur']
                tour_id = backup_tournament['tour'].split()
                player_id = backup_tournament['joueurs'].split()
                players = []
                for player in player_id:
                    players.append(Player(player_id=int(player)))


            else:
                print("ce choix n'est pas valide !")

    def save_tournament(self, new=False):
        player_id = ""
        for player in self.joueurs:
            player_id += str(player.id) + " "
        tour_id = ""
        for tour in self.tour:
            tour_id += str(tour.id) + " "
        serialized_tournament = {
            'nom': self.nom,
            'lieu': self.lieu,
            'date_de_debut': str(self.date_de_debut),
            'date_de_fin': str(self.date_de_fin),
            'nombre_de_tour': self.nombre_de_tour,
            'tour': tour_id,
            'controle_du_temps': self.controle_du_temps,
            'description': self.description,
            'nombre_de_joueur': self.nombre_de_joueur,
            'joueurs': player_id,
        }
        if new:
            self.tournament_table.insert(serialized_tournament)
        else:
            pass


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
