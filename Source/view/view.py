class View:
    def show_main_menu(self):
        print("\n\n## Menu Principale ##\n")
        print("1 : Ajouter un nouveau joueur")
        print("2 : Débuter un nouveau tournois")
        print("3 : Continuer un tournois en cour")
        print("4 : quiter le programme")
        print("\nentré le nombre correspondant a votre choix.")
        return self.ask_for_choice(4)

    def show_tournament_menu(self, round_status, etat):
        print("\n\n## Menu du tournois ##\n")
        if round_status == "started":
            print("1 : Finir le tour")
        elif etat == "first_round":
            print("1 : Commencer le tournois")
        elif etat == "new_round":
            print("1 : Commencer le prochain tour")
        elif etat == "finish" and round_status == "":
            print("1 : Voir les scores")
        print("2 : voir la liste des joueurs du tournois")
        print("3 : quitter le tournois")
        print("\nentré le nombre correspondant a votre choix.")
        return self.ask_for_choice(3)

    def ask_for_choice(self, number_of_choices):
        good_choice = False
        while not good_choice:
            choice = input("choix : ")
            if choice.isdigit() and int(choice) > 0 and int(choice) <= number_of_choices:
                good_choice = True
            else:
                print("le choix entré ne corespond pas à un choix valide. choisisser à nouveau")
        return choice

    def enter_player_info(self):
        player = {}
        player["lastname"] = input("nom : ")
        player["firstname"] = input("prenom : ")
        player["birthday"] = input("date de naissance : ")
        player["sex"] = input("sexe : ")
        player["ranking"] = input("classement : ")
        print("\nJoueur sauvegarder !")
        return player

    def enter_tournament_info(self):
        tournament = {
            "name": input("Nom du tournois : "),
            "place": input("Lieu du tournois : "),
            "number_of_round": input("Nombre de tour (par defaut : 4) : ") or "4",
            "description": input("Description : "),
        }
        print("type de controle du temps :")
        print("1 : Bullet")
        print("2 : Blitz")
        print("3 : Coup rapide")
        tournament["time_controle"] = self.ask_for_choice(3)
        tournament["number_of_player"] = "8"
        return tournament

    def choice_player(self, player_list):
        print(player_list["valid_players_string"])
        print("entrer le numero du joueur à ajouter")
        print(player_list["valid_players_id"])
        good_choice = False
        while not good_choice:
            choice = input("choix : ")
            print(choice.isdigit())
            if choice.isdigit() and int(choice) in player_list["valid_players_id"]:
                good_choice = True
            else:
                print("le choix entré ne corespond pas à un choix valide. choisisser à nouveau")
        return int(choice)

    def choice_tournament(self, list_of_available_tounament):
        tournament_number = 1
        print(list_of_available_tounament)
        for tournament in list_of_available_tounament:
            print(str(tournament_number) + ' : ' + tournament['name'])
            tournament_number +=1
        return self.ask_for_choice(len(list_of_available_tounament))

    def show_match_info(self, match):
        print(
            match.player1.ranking
            + " "
            + match.player1.firstname
            + " "
            + match.player1.lastname
            + " -- VS -- "
            + match.player2.firstname
            + " "
            + match.player2.lastname
            + " "
            + match.player2.ranking
        )
        input("\nAppuyer sur ENTER pour continuer !\n")
    
    def enter_score_choice(self, match):
        print("\nchoisisez le score pour le match entre :\n")
        self.show_match_info(match)
        print("1 : Victoire de " + match.player1.firstname + ' ' + match.player1.lastname)
        print("2 : Match Nul")
        print("3 : Victoire de " + match.player2.firstname + ' ' + match.player2.lastname)
        return self.ask_for_choice(3)
    
    def show_score(self, sorted_list_player_by_score):
        ''' Show the scoreboard of the tournament
        
            attr:
                sorted_list_player_by_score : sorted list of player order by score descendant
        '''
        tournament_ranking = 1
        for player in sorted_list_player_by_score:
            print(
                str(tournament_ranking)
                + ' : ' +
                player[0].firstname
                + ' ' +
                player[0].lastname
                + ' : ' +
                str(player[1])
            )
            tournament_ranking += 1
        input("\nAppuyer sur ENTER pour continuer !\n")
    
    def show_player_list(self, player_list):
        ''' Show basic player info from the player list given
        
            attr:
                player_list : list of players to show
        '''
        for player in player_list:
            print(
                player.ranking
                + ' : ' +
                player.firstname
                + ' ' +
                player.lastname
            )
        input("\nAppuyer sur ENTER pour continuer !\n")

