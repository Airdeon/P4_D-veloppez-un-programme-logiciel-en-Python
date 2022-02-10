from Player.Player import Player
from Tournament.Tournament import Tournament

def menu_principale():
    end_loop = False
    while end_loop == False:
        print("\n\n## Menu Principale ##\n")
        print("1 : Ajouter un nouveau joueur")
        print("2 : Débuter un nouveau tournois")
        print("3 : Continuer un tournois en cour")
        print("4 : quiter le programme")
        print("\nentré le nombre correspondant a votre choix.")
        good_choice = False
        while good_choice == False:
            choice = input("choix : ")
            match choice:
                case "1":
                    good_choice = True
                    Player(True)
                case "2":
                    good_choice = True
                    Tournament(True)
                case "3":
                    good_choice = True
                    Tournament()
                case "4":
                    good_choice = True
                    end_loop = True
                case _:
                    print("le choix entré ne corespond pas à un choix valide. choisisser à nouveau")