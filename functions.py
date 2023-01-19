import types_and_inits
import gui
from constants import *


def show_grid(game: types_and_inits.game):
    output = "\n"
    output += " "
    for i in range(game.grid_size.x):
        output += " " + str(i)
    output += "\n"
    output += "~" * (2 * game.grid_size.x + 3) + "\n"
    for line in game.grid:
        output += "| "
        for cell in line:
            output += SYMBOLES[cell] + " "
        output += "|\n"
    output += "~" * (2 * game.grid_size.x + 3) + "\n"
    output += " "
    for i in range(game.grid_size.x):
        output += " " + str(i)
    print(output)


def ask_move(game: types_and_inits.game, message: str = "", warning_message: str = "", window=None, fonts=None):
    print()
    print(message)
    if IS_GUI_ENABLED:
        raw_player_input = gui.str_input(
            window=window, fonts=fonts, question=str(game.players[game.current_player-1]) + ", où voulez vous jouer?", warning_message=warning_message, font_size="medium", is_show_grid=True, game=game, vertical_positions=types_and_inits.vertical_positions(0.12, 0.17, 0.22))
    else:
        raw_player_input = input(
            "Joueur : " + game.players[game.current_player-1] + "\n\tOù voulez vous jouer?\n\033[0;34m"+warning_message+"\033[0m\n    -> ")
    try:
        player_input = int(raw_player_input) - 1
        if (player_input < 0 or player_input > game.grid_size.x-1):
            player_input = ask_move(
                window=window, fonts=fonts, game=game, message="", warning_message="Colonne inexistante")
        if game.grid[0][player_input] != 0:
            player_input = ask_move(
                window=window, fonts=fonts, game=game, message="", warning_message="Colonne pleine")
    except:
        player_input = ask_move(window = window, fonts=fonts ,game = game, message = "", warning_message="mauvais type")

    return player_input


def add_piece(game: types_and_inits.game, column: int):
    row = 0
    while game.grid[row][column] == 0 and row < game.grid_size.y-1:
        row += 1
    if game.grid[row][column] == 0:
        game.grid[row][column] = game.current_player
    else:
        game.grid[row-1][column] = game.current_player


def set_current_player(game: types_and_inits.game, new_current_player: int):
    game.current_player = new_current_player


def switch_to_next_player(game: types_and_inits.game):
    new_current_player = game.current_player + 1
    if new_current_player > game.player_count:
        new_current_player = 1
    set_current_player(game, new_current_player)


def round(game: types_and_inits.game, window=None, fonts=None):
    move = ask_move(game, "", warning_message="", window=window, fonts=fonts)
    add_piece(game, move)
    switch_to_next_player(game)
    show_grid(game)


def is_end_of_game(game: types_and_inits.game):
    for row in range(game.grid_size.y):
        for column in range(game.grid_size.x):
            if game.grid[row][column] == 0:
                return False
    return True


def play_game(game, window=None, fonts=None):
    show_grid(game)
    while not (is_end_of_game(game)):
        round(game, window=window, fonts=fonts)
        points = count_points(game)
        show_points(points)
    points = count_points(game)
    show_points(points)


def is_block_complete(game: types_and_inits.game, start_position: types_and_inits.position, end_position: types_and_inits.position, player: int):
    positions = []
    is_complete = True
    try:
        for cell_index in range(game.winning_size):
            column_index = int(start_position.x + cell_index *
                               ((end_position.x-start_position.x))/game.winning_size)
            row_index = int(start_position.y + cell_index *
                            ((end_position.y-start_position.y))/game.winning_size)
            positions.append((row_index, column_index))
            #print("(", row_index, ",", column_index, ")", " : ", game.grid[row_index][column_index])
            if game.grid[row_index][column_index] != player:
                is_complete = False
    except:
        pass

    #show_currently_checked(game, positions)
    return is_complete


def count_player_points(game: types_and_inits.game, player: int):
    player_points = 0
    grid = game.grid
    # lignes
    for row_index in range(game.grid_size.y):
        for block_index in range(game.grid_size.x - game.winning_size + 1):
            if is_block_complete(game, types_and_inits.position(block_index, row_index), types_and_inits.position(block_index + game.winning_size, row_index), player):
                player_points += 1

    # colonne
    for column_index in range(game.grid_size.y):
        for block_index in range(game.grid_size.y - game.winning_size + 1):
            if is_block_complete(game, types_and_inits.position(column_index, block_index), types_and_inits.position(column_index, block_index + game.winning_size), player):
                player_points += 1

    # diagonales haut bas
    for diagonal_index in range(game.grid_size.y - game.winning_size + 1, -1, -1):
        for index in range(game.grid_size.y-game.winning_size + 1 - diagonal_index):
            row_index = index + diagonal_index
            column_index = index
            #prin|t("\t: ", index)
            if is_block_complete(game, types_and_inits.position(column_index, row_index), types_and_inits.position(column_index + game.winning_size, row_index + game.winning_size), player):
                player_points += 1
                # print("+1")
            # print("\n")

    for diagonal_index in range(1, game.grid_size.x - game.winning_size + 1, 1):
        for index in range(game.grid_size.y-game.winning_size + 1 - diagonal_index):
            row_index = index
            column_index = index + diagonal_index
            #print("\t: ", index)
            if is_block_complete(game, types_and_inits.position(column_index, row_index), types_and_inits.position(column_index + game.winning_size, row_index + game.winning_size), player):
                player_points += 1
                # print("+1")
            # print("\n")

    # diagonales bas haut
    for diagonal_index in range(game.winning_size-1, game.grid_size.x):
        for index in range(diagonal_index - game.winning_size + 1 + 1):
            row_index = index
            column_index = diagonal_index - index
            if is_block_complete(game, types_and_inits.position(column_index, row_index), types_and_inits.position(column_index - game.winning_size, row_index + game.winning_size), player):
                player_points += 1

    for diagonal_index in range(1, game.grid_size.y - game.winning_size + 1):
        for index in range(game.winning_size - 2 - diagonal_index):
            row_index = diagonal_index
            column_index = game.grid_size.x - index - 1
            if is_block_complete(game, types_and_inits.position(column_index, row_index), types_and_inits.position(column_index - game.winning_size, row_index + game.winning_size), player):
                player_points += 1

    return player_points


def count_points(game: types_and_inits.game):
    points = [0] * game.player_count
    for player in range(1, game.player_count+1):
        points[player-1] = count_player_points(game, player)
    return points


def show_points(points: list[int]):
    print("Scores :\n")
    for i in range(len(points)):
        print("\tLe joueur ", i+1, " a ", points[i], " points\n")


def show_currently_checked(game: types_and_inits.game, positions: list[types_and_inits.position]):
    print(positions)
    print("~~~~~~~~~~~~~")
    for i in range(game.grid_size.x):
        print("|", end=" ")
        for j in range(game.grid_size.y):
            if (i, j) in positions:
                print(game.grid[j][i], end=" ")
            else:
                print(".", end=" ")
        print("|")
    print("~~~~~~~~~~~~~\n")


def input_protege(question, answer_type=str, range_or_list="none", valid_answers_interval=(), valid_answers_list=[], default_answer="", warning_message="", window=None, fonts=None, is_show_grid=False):
    """
    Fonction qui permet d'effectuer des inputs sans risques d'erreur fatales au programme. (utilisée pour toutes les demandes à l'utilisateur)
    elle permet aussi de spécifier un type et un intervalle ou une liste de réponses possibles comme c'est souvent nécessaire.
    question = question à poser (str)
    type_attendu = type de variable attendu (str par defaut)
    range_or_list = "range" pour un intervalle, "list" pour une liste de valeur, rien pour ignorer la condition
    intervalle_reponses_possibles = à completer pour un test d'intervalle
    liste_reponses_possibles = à completer pour un test de liste
    """
    if IS_GUI_ENABLED:
        saisie = gui.str_input(
            window, fonts, question, default_answer, warning_message, "medium", is_show_grid)
    else:
        saisie = input(question+"\n"+DEFAULT_QUESTION_TOKEN)
    type_verifie = False
    valeur_verifie = False

    while not (type_verifie and valeur_verifie):
        try:
            saisie_modifie = answer_type(saisie)

        except:
            if IS_GUI_ENABLED:
                saisie = gui.str_input(window, fonts, question,
                                       saisie, warning_message="Votre saisie n'est pas du type" + answer_type.__name__ + ".\nMerci de saisir un"+answer_type.__name__, font_size="medium", is_show_grid=is_show_grid)
            else:
                print("Votre saisie n'est pas du type", str(answer_type.__name__), ". Merci de saisir un",
                      answer_type.__name__)
                saisie = input(DEFAULT_QUESTION_TOKEN)

        else:
            type_verifie = True
            if range_or_list == "range":
                if saisie_modifie in range(valid_answers_interval[0], valid_answers_interval[1]):
                    valeur_verifie = True
                else:
                    if IS_GUI_ENABLED:
                        saisie = gui.str_input(window, fonts, question,
                                               saisie, warning_message="Votre saisie n'est pas comprise entre" + str(valid_answers_interval[0]) + "et" +
                                               str(
                                                   valid_answers_interval[1]-1) + ".\nMerci de saisir une valeur comprise dans cet intervalle", font_size="medium", is_show_grid=is_show_grid)
                    else:
                        print("Votre saisie n'est pas comprise entre", valid_answers_interval[0], "et",
                              str(valid_answers_interval[1]-1), ". Merci de saisir une valeur comprise dans cet intervalle")
                        saisie = input(DEFAULT_QUESTION_TOKEN)
            elif range_or_list == "list":
                if saisie_modifie in valid_answers_list:
                    valeur_verifie = True
                else:

                    if IS_GUI_ENABLED:
                        saisie = gui.str_input(
                            window, fonts, question, saisie, warning_message="Votre saisie n'est pas comprise dans la liste : " + str(valid_answers_list) +
                            ".\nMerci de saisir une valeur comprise dans : " + str(valid_answers_list), font_size="medium", is_show_grid=is_show_grid)
                    else:
                        print("Votre saisie n'est pas comprise dans la liste : ", valid_answers_list,
                              ". Merci de saisir une valeur comprise dans : ", valid_answers_list)
                        saisie = input(DEFAULT_QUESTION_TOKEN)
            else:
                valeur_verifie = True
            # print(valeur_verifie)
    return saisie_modifie


def init_joueurs(n, window, fonts):
    """Crée la liste des joueurs de taille n, chaque joueur ayant un nom différent"""
    joueurs = []
    for i in range(n):  # Pour chaque joueur on demande à l'utilisateur le nom
        nom_raw = input_protege(
            "Quel est le nom du joueur " + str(i+1)+" ?", window=window, fonts=fonts, default_answer="joueur_" + str(i+1))
        nom = nom_raw.upper()
        while nom in joueurs:  # contrôle pour ne pas avoir 2 fois le même nom
            nom = input_protege(
                "Quel est le nom du joueur " + str(i+1)+" ?", window=window, fonts=fonts, default_answer=nom_raw, warning_message="Ce nom est déjà utilisé, merci d'en entrer un autre!").upper()
        joueurs.append(nom)
    return joueurs


def is_replay_asked(window, fonts, game):
    window.fill(BACKGROUND_COLOR)
    points = count_points(game)
    for i in range(len(points)):
        gui.creer_boite_texte((window.get_size()[0] // 2, int(window.get_size()[1]*(0.2+0.075*(i+1)))),
                              "Le joueur "+ str(i+1) +
                              " a " + str(points[i]) + " points", window,
                      fonts["medium"])
    gui.creer_boite_texte((window.get_size()[0] // 2, int(window.get_size()[1]*0.2)), "SCORES :", window,
                      fonts["large"], couleur_texte=YELLOW)
    gui.creer_boite_texte((window.get_size()[0] // 2, 4 * window.get_size()[1] // 5),
                      "* Appuyez sur ESPACE pour rejouer ou TAB pour arreter *", window,
                      fonts["small"], couleur_texte=GREY)
    gui.update(window, fonts)
    return gui.pygame_bool_input()
