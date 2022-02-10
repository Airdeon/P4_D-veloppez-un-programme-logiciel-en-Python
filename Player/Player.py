from tinydb import TinyDB

class Player:
    db = TinyDB('./db.json')
    players_table = db.table('players')


    def __init__(self, new_player=False, players_already_pick=[], player_id=0):
        self.players_already_pick = players_already_pick
        if new_player == True:
            self.new_player()
        elif player_id > 0:
            self.get_player_from_database(player_id)
        else:
            self.show_player_list()


    def new_player(self):
        self.nom = input("nom : ")
        self.prenom = input("prenom : ")
        self.date_de_naissance = input("date de naissance : ")
        self.sexe = input("sexe : ")
        self.classement = input("classement : ")
        self.save_player()
        print("\nJoueur sauvegarder !")


    def get_player_from_database(self, player_id):
        player_line_serialized = self.players_table.get(all, player_id)
        self.nom = player_line_serialized['nom']
        self.prenom = player_line_serialized['prenom']
        self.date_de_naissance = player_line_serialized['date_de_naissance']
        self.sexe = player_line_serialized['sexe']
        self.classement = player_line_serialized['classement']
        self.id = player_id


    def show_player_list(self):
        valid_players=[]
        total_number_of_player = self.players_table.count(all)
        for number_of_player in range(total_number_of_player):
            player_line_serialized = self.players_table.get(all, number_of_player+1)
            player_line = str(number_of_player+1) + " " + player_line_serialized['nom'] + " " + player_line_serialized['prenom']
            valid = True
            for player in self.players_already_pick:
                if player.id == (number_of_player + 1):
                    valid = False
                    break
            if valid == True:
                valid_players.append(number_of_player+1)
                print(player_line)
        print("entrer le numero du joueur à ajouter")
        good_choice = False
        while good_choice == False:
            choice = input("choix : ")
            if int(choice) in valid_players:
                good_choice=True
                player_select = self.players_table.get(all, int(choice))
                self.nom = player_select['nom']
                self.prenom = player_select['prenom']
                self.date_de_naissance = player_select['date_de_naissance']
                self.sexe = player_select['sexe']
                self.classement = player_select['classement']
                self.id = int(choice)
            else:
                print("ce choix n'est pas valide !")


    def save_player(self):
        serialized_player = {
            'nom': self.nom, 
            'prenom': self.prenom,
            'date_de_naissance': self.date_de_naissance,
            'sexe': self.sexe,
            'classement': self.classement,
        }
        self.players_table.insert(serialized_player)
