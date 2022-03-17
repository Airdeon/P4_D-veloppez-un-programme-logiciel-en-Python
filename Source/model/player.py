from tinydb import TinyDB


class PlayerDataBase:
    def __init__(self):
        db = TinyDB('./db.json')
        self.players_table = db.table('players')

    def get_number_of_player(self):
        return self.players_table.count(all)

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

    def get_player_list(self):
        player_list = []
        for player in self.players_table:
            player_list.append(Player(player_id=player.doc_id))
        return player_list


class Player:
    def __init__(self, player_id=None, player_info=None):
        ''' Init player object with player information on database

            Args :
                player_id : id of an existing player in the database
        '''
        db = TinyDB('./db.json')
        self.players_table = db.table('players')
        if player_id is not None:
            player_info = self.players_table.get(all, int(player_id))
            self.player_id = player_id
        self.lastname = player_info['lastname']
        self.firstname = player_info['firstname']
        self.birthday = player_info['birthday']
        self.sex = player_info['sex']
        self.ranking = player_info['ranking']
        if player_id is None:
            self.player_id = self.save_new_player()

    def save_new_player(self):
        ''' Save player in tinydb database '''
        player_info = {
            'lastname': self.lastname,
            'firstname': self.firstname,
            'birthday': self.birthday,
            'sex': self.sex,
            'ranking': self.ranking,
        }
        return self.players_table.insert(player_info)

    def __str__(self):
        return self.player_id

    def update_ranking(self, new_ranking):
        self.ranking = new_ranking
        self.players_table.update({"ranking": self.ranking}, doc_ids=[self.player_id])