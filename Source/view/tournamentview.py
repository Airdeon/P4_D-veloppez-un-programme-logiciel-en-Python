from .utils import clean_screen, ask_for_choice


class TournamentView:
    def show_selected_tournament_menu(self, tournament_name, tournament_status):
        print("\n## Menu du tournois : " + tournament_name + " ##\n")
        if tournament_status == "enter_score":
            print("1 : Finir le tour")
        elif tournament_status == "not_started":
            print("1 : Commencer le premier tour")
        elif tournament_status == "start_new_round":
            print("1 : Commencer le prochain tour")
        elif tournament_status == "finish":
            print("1 : Voir les scores")
        if tournament_status != "finish":
            print("2 : Voir le classement actuelle du tournois")
            print("3 : Voir la liste des joueurs")
            print("4 : Voir la liste des matchs")
            print("5 : Quitter le tournois")
            numbers_of_choice = 5
        else:
            print("2 : Voir la liste des joueurs")
            print("3 : Voir la liste des matchs")
            print("4 : Quitter le tournois")
            numbers_of_choice = 4
        print("\nentré le nombre correspondant a votre choix.")
        return ask_for_choice(numbers_of_choice)

    def enter_tournament_info(self):
        clean_screen()
        print("## Entrer les information du nouveau tournois ##\n")
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
        tournament["time_controle"] = ask_for_choice(3)
        tournament["number_of_player"] = "8"
        return tournament

    def choice_player(self, player_list):
        clean_screen()
        print("Choisisez les joueurs participant à ce tournois\n")
        for player in player_list:
            player_string = (
                str(player.player_id)
                + " : " +
                player.firstname
                + " " +
                player.lastname
                + " | " +
                str(player.ranking)
                )
            print(player_string)
        print("\nEntrer le numero du joueur à ajouter")
        good_choice = False
        while not good_choice:
            choice = input("\nchoix : ")
            for player in player_list:
                if choice.isdigit() and int(choice) == player.player_id:
                    clean_screen()
                    return player
            print("le choix entré ne corespond pas à un choix valide. choisisser à nouveau")

    def show_match_info(self, match):
        """ show information of a match

            attr:
                match : instance of Match
        """
        match_string = (
            str(match.player1.ranking)
            + " "
            + match.player1.firstname
            + " "
            + match.player1.lastname
            )
        if match.player1_score != 0 or match.player2_score != 0:
            match_string += (
                " " + str(match.player1_score)
                + " -- VS -- "
                + str(match.player2_score)
                + " "
                )
        else:
            match_string += " -- VS -- "
        match_string += (
            match.player2.firstname
            + " "
            + match.player2.lastname
            + " "
            + str(match.player2.ranking)
            )
        print(match_string)

    def enter_score_choice(self, match):
        """ input for enter the result of a match

            attr:
                match : instance of a match
        """
        clean_screen()
        print("\nchoisisez le score pour le match entre :\n")
        self.show_match_info(match)
        print("\n1 : Victoire de " + match.player1.firstname + ' ' + match.player1.lastname)
        print("2 : Match Nul")
        print("3 : Victoire de " + match.player2.firstname + ' ' + match.player2.lastname)
        return ask_for_choice(3)

    def show_score(self, sorted_list_player_by_score):
        ''' Show the scoreboard of the tournament

            attr:
                sorted_list_player_by_score : sorted list of player order by score descendant
        '''
        clean_screen()
        tournament_ranking = 1
        print("Classement du tournois / Score / Prenom / Nom (id du joueur) / Classement général\n")
        for player in sorted_list_player_by_score:
            print(
                str(tournament_ranking)
                + ' : ' +
                str(player[1])
                + " : " +
                player[0].firstname
                + ' ' +
                player[0].lastname
                + ' (' +
                str(player[0].player_id)
                + ') : ' +
                str(player[0].ranking)
            )
            tournament_ranking += 1
        print("""\nPour modifier le classement général d'un joueur, entrer son numero id\n
        Si non, appuyer sur ENTER pour revenir au menu !\n""")
        choice = input("choix : ")
        for player in sorted_list_player_by_score:
            if str(player[0].player_id) == choice:
                return player[0]
        return ""

    def show_match_list(self, round_list):
        """ Show the list of all rounds and all matchs of the current tournament

            attr:
                round_list : list of round instance
        """
        for round in round_list:
            round_string = '\n ## ' + round.round_name + ' Commencer le ' + round.start_datetime[0:19]
            if round.end_datetime != "":
                round_string += ' et terminé le ' + round.end_datetime[0:19]
            print(round_string)
            for match in round.matchs:
                self.show_match_info(match)

        input("\nAppuyer sur ENTER pour continuer !\n")
        clean_screen()
