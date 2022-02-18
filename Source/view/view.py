class View:
    def show_main_menu(self):
        print("\n\n## Menu Principale ##\n")
        print("1 : Ajouter un nouveau joueur")
        print("2 : Débuter un nouveau tournois")
        print("3 : Continuer un tournois en cour")
        print("4 : quiter le programme")
        print("\nentré le nombre correspondant a votre choix.")
        return self.ask_for_choice(4)

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
            "nom": input("Nom du tournois : "),
            "lieu": input("Lieu du tournois : "),
            "nombre_de_tour": input("Nombre de tour (par defaut : 4) : ") or "4",
            "description": input("Description : "),
        }
        print("type de controle du temps :")
        print("1 : Bullet")
        print("2 : Blitz")
        print("3 : Coup rapide")
        tournament["controle_du_temps"] = self.ask_for_choice(3)
        tournament["nombre_de_joueur"] = "8"
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
