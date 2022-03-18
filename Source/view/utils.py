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


def check_name(input_string):
    good_value = False
    while not good_value:
        user_input = input(input_string)
        if len(user_input) < 3:
            print("\nle nom est trop court (minimum 3 caractere)\n")
        else:
            return user_input


def check_number(input_string, default=None):
    """check if input is positive integer"""
    good_value = False
    while not good_value:
        user_input = input(input_string)
        if user_input == "":
            if default is not None:
                user_input = default
        try:
            responce = int(user_input)
            if responce > 0:
                good_value = True
            else:
                print("\nEntrer un nombre entier positif")
        except ValueError:
            print("\nLa valeur entré n'est pas valide, entrer un nombre entier positif")
    return responce
