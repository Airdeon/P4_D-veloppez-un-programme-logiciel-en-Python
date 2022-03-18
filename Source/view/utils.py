import os


def clean_screen():
    os.system('cls')


def ask_for_choice(number_of_choices):
    good_choice = False
    while not good_choice:
        choice = input("choix : ")
        if choice.isdigit() and int(choice) > 0 and int(choice) <= number_of_choices:
            good_choice = True
        else:
            print("Le choix entré ne corespond pas à un choix valide. choisisser à nouveau")
    clean_screen()
    return choice
