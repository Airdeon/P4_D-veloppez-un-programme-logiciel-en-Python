from .utils import clean_screen, ask_for_choice


class MainView:
    def show_main_menu(self):
        clean_screen()
        print("## Menu Principale ##\n")
        print("1 : Tournois")
        print("2 : Gestion des joueurs")
        print("3 : Quitter le programme")
        print("\nEntré le nombre correspondant a votre choix.")
        return ask_for_choice(3)

    def show_tournament_menu(self):
        clean_screen()
        print("## Menu des tournois ##\n")
        print("1 : Crée un nouveau tournois")
        print("2 : Continuer un tournois")
        print("3 : Liste des tournois")
        print("4 : Retour au menu principale")
        return ask_for_choice(4)

    def show_player_management_menu(self):
        clean_screen()
        print("## Gestion des joueurs ##\n")
        print("1 : Liste des joueurs")
        print("2 : Ajouter un nouveau joueur")
        print("3 : Retour au menu principale")
        return ask_for_choice(3)

    def show_number_of_player_warning(self):
        clean_screen()
        print("Le nombre de joueur dans la base de donnée est inssufisante pour lancer un tournois (Minimum 8)")
        print("Ajouter plus de joueurs depuis le menu de gestion des joueurs")
        input("\nAppuyer sur ENTER pour continuer !\n")

    def show_number_of_tournament_warning(self):
        clean_screen()
        print("Il n'y a pas de tournois a terminer actuellement !")
        input("\nAppuyer sur ENTER pour continuer !\n")

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
                if ranking > 0:
                    good_value = True
            except ValueError:
                print("\nLa valeur entré n'est pas valide, entrer un nombre entier positif")
        player["ranking"] = ranking
        print("\nJoueur sauvegarder !")
        input("\nAppuyer sur ENTER pour continuer !\n")
        return player

    def choice_tournament(self, list_of_available_tounament):
        clean_screen()
        print("## Liste des tournois disponible ##\n")
        tournament_number = 1
        for tournament in list_of_available_tounament:
            print(str(tournament_number) + ' : ' + tournament['name'])
            tournament_number += 1
        return ask_for_choice(len(list_of_available_tounament))

    def ask_for_order_type(self):
        clean_screen()
        print("## choix du type de classement ##\n")
        print("1 : Par ordre alphabetique")
        print("2 : Par classement\n")
        return ask_for_choice(2)

    def show_player_list(self, player_list, order_type):
        ''' Show basic player info from the player list given

            attr:
                player_list : list of players to show
        '''
        if order_type == "1":
            sorted_list = sorted(player_list, key=lambda player: player.lastname)
        elif order_type == "2":
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

    def change_player_ranking(self, player):
        """ input for enter new player ranking

            attr :
                player : instance of Player
        """
        clean_screen()
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
            response = input("Classement : ")
            try:
                ranking = int(response)
                if ranking > 0:
                    good_value = True
            except ValueError:
                print("\nLa valeur entré n'est pas valide, entrer un nombre entier positif")
        print("nouveau classement enregistré\n\n")
        return ranking
