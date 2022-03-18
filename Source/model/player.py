from tinydb import TinyDB


class PlayerDataBase:
    """ Acces to player database """
    def __init__(self):
        """ Init database """
        db = TinyDB('./db.json')
        self.players_table = db.table('players')

    def get_number_of_player(self):
        """ return the number of player in database"""
        return self.players_table.count(all)

    def get_player_available_list(self, players_already_pick):
        player_list = []
        for player in self.players_table:
            player_pick = False
            for playerpick in players_already_pick:
                if player.doc_id == playerpick.player_id:
                    player_pick = True
            if not player_pick:
                player_list.append(Player(player_id=player.doc_id))
        return player_list

    def get_player_list(self):
        """ return object list of all players in database"""
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

    def update_ranking(self, new_ranking):
        """ Update ranking of the player in database

            attr:
                new_ranking : a new ranking integer number
        """
        self.ranking = new_ranking
        self.players_table.update({"ranking": self.ranking}, doc_ids=[self.player_id])
