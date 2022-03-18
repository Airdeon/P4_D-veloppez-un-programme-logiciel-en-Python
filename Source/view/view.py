import os


def clean_screen():
    os.system('cls')


class View:
    def show_main_menu(self):
        clean_screen()
        print("## Menu Principale ##\n")
        print("1 : Tournois")
        print("2 : Gestion des joueurs")
        print("3 : Quitter le programme")
        print("\nEntré le nombre correspondant a votre choix.")
        return self.ask_for_choice(3)

    def show_tournament_menu(self):
        clean_screen()
        print("## Menu des tournois ##\n")
        print("1 : Crée un nouveau tournois")
        print("2 : Continuer un tournois")
        print("3 : Liste des tournois")
        print("4 : Retour au menu principale")
        return self.ask_for_choice(4)

    def show_player_management_menu(self):
        clean_screen()
        print("## Gestion des joueurs ##\n")
        print("1 : Liste des joueurs")
        print("2 : Ajouter un nouveau joueur")
        print("3 : Retour au menu principale")
        return self.ask_for_choice(3)

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
        return self.ask_for_choice(numbers_of_choice)

    def show_number_of_player_warning(self):
        clean_screen()
        print("Le nombre de joueur dans la base de donnée est inssufisante pour lancer un tournois (Minimum 8)")
        print("Ajouter plus de joueurs depuis le menu de gestion des joueurs")
        input("\nAppuyer sur ENTER pour continuer !\n")

    def show_number_of_tournament_warning(self):
        clean_screen()
        print("Il n'y a pas de tournois a terminer actuellement !")
        input("\nAppuyer sur ENTER pour continuer !\n")

    def ask_for_choice(self, number_of_choices):
        good_choice = False
        while not good_choice:
            choice = input("choix : ")
            if choice.isdigit() and int(choice) > 0 and int(choice) <= number_of_choices:
                good_choice = True
            else:
                print("Le choix entré ne corespond pas à un choix valide. choisisser à nouveau")
        clean_screen()
        return choice

    def enter_player_info(self):
        clean_screen()
        print("Entrer les informations du nouveau joueurs")
        player = {}
        player["lastname"] = input("nom : ")
        player["firstname"] = input("prenom : ")
        player["birthday"] = input("date de naissance : ")
        player["sex"] = input("sexe : ")
        good_value = False
        while not good_value:
            response = input("Classement : ")
            try:
                ranking = int(response)
                good_value = True
            except ValueError:
                print("\nLa valeur entré n'est pas valide, entrer un nombre entier")
        player["ranking"] = ranking
        print("\nJoueur sauvegarder !")
        input("\nAppuyer sur ENTER pour continuer !\n")
        return player

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
        tournament["time_controle"] = self.ask_for_choice(3)
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

    def choice_player2(self, player_list):
        clean_screen()
        print("Choisisez les joueurs participant à ce tournois\n")
        print(player_list["valid_players_string"])
        print("entrer le numero du joueur à ajouter")
        good_choice = False
        while not good_choice:
            choice = input("\nchoix : ")
            print(choice.isdigit())
            if choice.isdigit() and int(choice) in player_list["valid_players_id"]:
                good_choice = True
            else:
                print("le choix entré ne corespond pas à un choix valide. choisisser à nouveau")
        clean_screen()
        return int(choice)

    def choice_tournament(self, list_of_available_tounament):
        clean_screen()
        print("## Liste des tournois disponible ##\n")
        tournament_number = 1
        for tournament in list_of_available_tounament:
            print(str(tournament_number) + ' : ' + tournament['name'])
            tournament_number += 1
        return self.ask_for_choice(len(list_of_available_tounament))

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
        return self.ask_for_choice(3)

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
        print("""\nPour modifier le classement général d'un joueur,
        entrer son numero id\nSi non, appuyer sur ENTER pour revenir au menu !\n""")
        choice = input("choix : ")
        for player in sorted_list_player_by_score:
            if str(player[0].player_id) == choice:
                return player[0]
        return ""

    def show_player_list(self, player_list):
        ''' Show basic player info from the player list given

            attr:
                player_list : list of players to show
        '''
        print("1 : Par ordre alphabetique")
        print("2 : Par classement")
        choice = self.ask_for_choice(2)
        if choice == "1":
            sorted_list = sorted(player_list, key=lambda player: player.lastname)
        elif choice == "2":
            sorted_list = sorted(player_list, key=lambda player: player.ranking)
        clean_screen()
        print("\n\n## Liste des Joueurs ##\n")
        print("ID / Classement / Prenom / Nom\n")
        for player in sorted_list:
            print(
                str(player.player_id)
                + ' : ' +
                str(player.ranking)
                + ' : ' +
                player.firstname
                + ' ' +
                player.lastname
            )
        print("\nPour modifier le classement d'un joueur, entrer son numero !")
        print("Si non, appuyer sur ENTER pour revenir au menu !\n")
        choice = input("choix :")
        clean_screen()
        for player in player_list:
            if str(player.player_id) == choice:
                return player
        return ""

    def change_player_ranking(self, player):
        """ input for enter new player ranking

            attr :
                player : instance of Player
        """
        player_string = (
            "\nle classement actuelle de "
            + player.firstname
            + " "
            + player.lastname
            + " est : "
            + str(player.ranking)
            )
        print(player_string)
        good_value = False
        while not good_value:
            response = input("enter son nouveau classement : ")
            try:
                ranking = int(response)
                good_value = True
            except ValueError:
                print("\nLa valeur entré n'est pas valide, entrer un nombre entier")

        print("nouveau classement enregistré")
        return ranking

    def show_tournament_list(self, tournament_list):
        """ Show list of tournament

            attr:
                tournament_list : list of Tournament instance
        """
        clean_screen()
        print("## Liste des Tournois ##\n")
        for tournament in tournament_list:
            tournament_line = (
                str(tournament.tournament_id)
                + ' : ' +
                tournament.name
                + ' à ' +
                tournament.place
                + ' | Démaré le ' +
                tournament.start_date[0:19]
                )
            if tournament.end_date != "":
                tournament_line.join(" et terminé le " + tournament.end_date[0:19])
            print(tournament_line)
        print("""\nPour entrer dans un tournois, entrer son numero id.
        Si non, appuyer sur ENTER pour revenir au menu !\n""")
        choice = input("choix : ")
        for tournament in tournament_list:
            if str(tournament.tournament_id) == choice:
                return tournament
        return ""

    def show_match_list(self, round_list):
        """ Show the list of all rounds and all matchs of the current tournament

            attr:
                round_list : list of round instance
        """
        for round in round_list:
            print("\n" + round.round_name)
            for match in round.matchs:
                print(self.show_match_info(match))
        input("\nAppuyer sur ENTER pour continuer !\n")
        clean_screen()
