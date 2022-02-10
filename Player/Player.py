from tinydb import TinyDB

class Player:
    db = TinyDB('./db.json')
    players_table = db.table('players')

    def __init__(self, new_player=False, players_already_pick=[]):
        self.players_already_pick = players_already_pick
        if new_player == True:
            self.new_player()
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

    def show_player_list(self):
        valid_players=[]
        total_number_of_player = self.players_table.count(all))
        for number_of_player in range(total_number_of_player):
            player_line_serialized = self.players_table.get(all, number_of_player+1)
            player_line = str(number_of_player+1) + " " + player_line_serialized['nom'] + " " + player_line_serialized['prenom']
            if number_of_player+1 not in self.players_already_pick:
                valid_players.append(number_of_player+1)
            if number_of_player+1 not in valid_players:
                print(player_line)
        print("entrer le numero du joueur à ajouter")
        good_choice = False
        while good_choice == False:
            choice = input("choix : ")
            if choice 



    def save_player(self):
        serialized_player = {
            'nom': self.nom, 
            'prenom': self.prenom,
            'date_de_naissance': self.date_de_naissance,
            'sexe': self.sexe,
            'classement': self.classement,
        }

        #players_table.truncate()	# clear the table first
        self.players_table.insert(serialized_player)
