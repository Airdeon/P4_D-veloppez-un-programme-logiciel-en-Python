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
            player_line = str(index_player) + " " + player_line_serialized['lastname'] + " " + player_line_serialized['firstname']
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
        player_serialized = self.player_database.get_player_from_database(int(player_id))
        self.lastname = player_serialized['lastname']
        self.firstname = player_serialized['firstname']
        self.birthday = player_serialized['birthday']
        self.sex = player_serialized['sex']
        self.ranking = player_serialized['ranking']
        self.player_id = player_id

    def __str__(self):
        return "".join(self.lastname + " " + self.firstname + " : " + self.ranking)

    def save(self):
        self.player_database.save_player(self)
