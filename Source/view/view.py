import os


def clean_screen():
    os.system('cls')


class View:
    def show_main_menu(self):
        clean_screen()
        print("## Menu Principale ##\n")
        print("1 : Tournois")
        print("2 : Gestion des joueurs")
        print("3 : Quiter le programme")
        print("\nentré le nombre correspondant a votre choix.")
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

    def show_selected_tournament_menu(self, tournament_name, round_status, etat):
        #clean_screen()
        print("## Menu du tournois : " + tournament_name + " ##\n")
        if round_status == "":
            print("1 : Finir le tour")
        elif etat == "round":
            print("1 : Commencer le prochain tour")
        elif etat == "finish" and round_status != "":
            print("1 : Voir les scores")
        print("2 : Voir la liste des joueurs du tournois")
        print("3 : Quitter le tournois")
        print("\nentré le nombre correspondant a votre choix.")
        return self.ask_for_choice(3)

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
                print("le choix entré ne corespond pas à un choix valide. choisisser à nouveau")
        return choice

    def enter_player_info(self):
        clean_screen()
        print("Entrer les informations du nouveau joueurs")
        player = {}
        player["lastname"] = input("nom : ")
        player["firstname"] = input("prenom : ")
        player["birthday"] = input("date de naissance : ")
        player["sex"] = input("sexe : ")
        player["ranking"] = input("classement : ")
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
        clean_screen()
        print("## Liste des tournois disponible ##\n")
        tournament_number = 1
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

    def enter_score_choice(self, match):
        clean_screen()
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
        clean_screen()
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
        clean_screen()
        print("\n\n## Liste des Joueurs ##\n")
        print("ID / Classement / Prenom / Nom\n")
        for player in player_list:
            print(
                str(player.player_id)
                + ' : ' +
                player.ranking
                + ' : ' +
                player.firstname
                + ' ' +
                player.lastname
            )
        input("\nAppuyer sur ENTER pour continuer !\n")
