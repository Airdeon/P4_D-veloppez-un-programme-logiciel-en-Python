from tinydb import TinyDB


class PlayerDataBase:
    def __init__(self):
        db = TinyDB('./db.json')
        self.players_table = db.table('players')

    def save_new_player(self, player_info):
        ''' save new player in the database '''
        self.lastname = player_info["lastname"]
        self.firstname = player_info["firstname"]
        self.birthday = player_info["birthday"]
        self.sex = player_info["sex"]
        self.ranking = player_info["ranking"]
        self.save_player()

    def save_player(self):
        ''' Save player in tinydb database '''
        serialized_player = {
            'nom': self.lastname,
            'prenom': self.firstname,
            'date_de_naissance': self.birthday,
            'sexe': self.sex,
            'classement': self.ranking,
        }
        self.players_table.insert(serialized_player)

    def get_player_available_list(self, players_already_pick):
        ''' get a list of every player available '''
        valid_players_id = []
        valid_players_string = ""
        total_number_of_player = self.players_table.count(all)
        for index_player in range(1, total_number_of_player+1):
            player_line_serialized = self.players_table.get(all, index_player)
            player_line = str(index_player) + " " + player_line_serialized['nom'] + " " + player_line_serialized['prenom']
            if index_player not in players_already_pick:
                valid_players_id.append(index_player)
                valid_players_string += player_line + "\n"
        player_list = {
            "valid_players_id": valid_players_id,
            "valid_players_string": valid_players_string
        }
        return player_list



class Player:

    def __init__(self, new_player=False, players_already_pick=[], player_id=0):
        ''' Init player object
            send to a good method depends of arguments

            Args :
                new_player : true for create a new player
                players_already_pick : list of player in tournament to make them unavailable to pick
                player_id : id of an existing player in the database
        '''
        self.players_already_pick = players_already_pick
        if new_player:
            self.new_player()
        elif player_id > 0:
            self.get_player_from_database(player_id)
        else:
            self.show_player_list()


    def get_player_from_database(self, player_id):
        ''' Get one player from database

        Args:
            player_id : id of the player in database
        '''
        player_line_serialized = self.players_table.get(all, player_id)
        self.nom = player_line_serialized['nom']
        self.prenom = player_line_serialized['prenom']
        self.date_de_naissance = player_line_serialized['date_de_naissance']
        self.sexe = player_line_serialized['sexe']
        self.classement = player_line_serialized['classement']
        self.id = player_id

    def show_player_list(self):
        ''' Show a list of every player available '''
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
