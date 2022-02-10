from tinydb import TinyDB

class Player:
    db = TinyDB('./db.json')
    players_table = db.table('players')

    def __init__(self, new_player=False):
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
        for number_of_player in range(self.players_table.count()):
            player_line_serialized = self.players_table.get(number_of_player)
            player_line = player_line_serialized['nom']
            print(player_line)


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
