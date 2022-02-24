from tinydb import TinyDB


class PlayerDataBase:
    def __init__(self):
        db = TinyDB('./db.json')
        self.players_table = db.table('players')

    def save_new_player(self, player_info):
        ''' save new player in the database '''
        self.players_table.insert(player_info)

    def save_player(self, Player):
        ''' Save player in tinydb database '''
        serialized_player = {
            'lastname': Player.lastname,
            'firstname': Player.firstname,
            'birthday': Player.birthday,
            'sex': Player.sex,
            'ranking': Player.ranking,
        }
        self.players_table.update(set(Player.player_id, serialized_player))

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

    def get_player_from_database(self, player_id):
        ''' Get one player from database

            Args:
                player_id : id of the player in database
        '''
        player_information = self.players_table.get(all, player_id)
        return player_information


class Player:
    def __init__(self, player_id):
        ''' Init player object with player information on database

            Args :
                player_id : id of an existing player in the database
        '''
        # creation of database object
        self.player_database = PlayerDataBase()
        # player initialisation
        player_serialized = PlayerDataBase.get_player_from_database(player_id)
        self.lastname = player_serialized['lastname']
        self.firstname = player_serialized['firstname']
        self.birthday = player_serialized['birthday']
        self.sex = player_serialized['sex']
        self.ranking = player_serialized['ranking']
        self.player_id = player_id
    
    def save(self):
        self.player_database.save_player(self)

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
