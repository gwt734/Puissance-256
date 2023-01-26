# Fichier où stocker toutes les fonctions nécessaires à l'affichage du jeu
import time

import pygame

import constants

import sys

import functions

import screeninfo

import types_and_inits


def window_init():
    "Fonction permettant de créer la window, les différentes fonts, et affiche un message de bienvenue"
    pygame.init()
    for monitor in screeninfo.get_monitors():
        monitor_size = monitor.width, monitor.height
        break
    window = pygame.display.set_mode(monitor_size)
    pygame.display.set_caption('Puissance 256')
    fonts = {"small": pygame.font.Font('freesansbold.ttf', constants.FONT_SIZE_SMALL),
               "medium": pygame.font.Font('freesansbold.ttf', constants.FONT_SIZE_MEDIUM),
               "large": pygame.font.Font('freesansbold.ttf', constants.FONT_SIZE_LARGE)}  # Créer les fonts et les places dans un dictionnaire
    window.fill(constants.BACKGROUND_COLOR)
    creer_boite_texte((window.get_size()[0] // 2, window.get_size()[1] // 3),
                      "Bienvenue dans cette partie de", window,
                      fonts["medium"])
    creer_boite_texte((window.get_size()[0] // 2, window.get_size()[1] // 2), "PUISSANCE 256", window,
                      fonts["large"], couleur_texte=constants.YELLOW)
    creer_boite_texte((window.get_size()[0] // 2, 4 * window.get_size()[1] // 5),
                      "* Appuyez sur ESPACE pour commencer *", window,
                      fonts["small"], couleur_texte=constants.GREY)
    update(window, fonts)
    pygame_bool_input()
    return window, fonts


def pygame_bool_input():
    """Fonction qui attends une touche de l'utilisateur et retourne vrai si ESPACE est touché et faux si TAB est touché."""
    while True:
        for evenement in pygame.event.get():  # Parcours tous les évenements recus depuis le dernier tick
            if evenement.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif evenement.type == pygame.KEYDOWN:  #
                if evenement.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif evenement.key == pygame.K_SPACE:
                    return True
                elif evenement.key == pygame.K_TAB:
                    return False


def update(window, fonts):
    standard_elements(window, fonts)
    pygame.display.update()


def creer_boite_texte(position, texte_a_afficher, window, font, couleur_texte=constants.WHITE, couleur_fond=None):
    """Simplifie l'ajout à l'affichage d'un texte en une seule ligne"""
    if len(texte_a_afficher)>0 :
        texte = font.render(texte_a_afficher, True, couleur_texte)
        boite_texte = texte.get_rect()
        boite_texte.center = (position[0], position[1])
        box_surf = pygame.Surface(
            texte.get_rect().inflate(30, 10).size)
        if couleur_fond is not None :
            box_surf.fill(couleur_fond)
            boite_boite = box_surf.get_rect()
            boite_boite.center = (position[0], position[1])
            window.blit(box_surf, boite_boite)
        window.blit(texte, boite_texte)


def str_input(window, fonts, question, valeur_par_default="", warning_message="", font_size="medium", is_show_grid=False, is_show_points=False, game=None, vertical_positions=types_and_inits.vertical_positions(0.40,0.50,0.60)):
    """Fonction input adaptés à l'affichage graphique"""
    saisie = str(valeur_par_default)
    valid = False
    last_tick = time.time()
    show_curseur = True
    window.fill(constants.BACKGROUND_COLOR)
    creer_boite_texte((window.get_size()[0] // 2, int(window.get_size()[1]*vertical_positions.input_position)),
                      saisie + "|" * int(show_curseur) + " " * (10 - len(saisie) - 1 * int(show_curseur)),
                      window, fonts["medium"], couleur_fond=constants.DARKER_BACKGROUND_COLOR)
    creer_boite_texte((window.get_size()[0] // 2, int(window.get_size()[1]*vertical_positions.question_position)), question, window,
                      fonts["large"])
    creer_boite_texte((window.get_size()[0] // 2, int(window.get_size()[
                      1]*vertical_positions.warning_position)), warning_message, window,
                      fonts["small"], couleur_texte=constants.WARNING_COLOR)
    window.fill(constants.BACKGROUND_COLOR)
    if is_show_grid:
        show_grid(window, fonts, game)
    if is_show_points:
        show_points(window, fonts, game)
    update(window, fonts)
    while not valid:  # Tant que l'utilisateur n'a pas validé sa reponse on cherche parmis les événeent et même parmis les touches de l'utilisateur
        for evenement in pygame.event.get():
            if evenement.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif evenement.type == pygame.KEYDOWN:
                if evenement.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif evenement.key == pygame.K_RETURN:
                    valid = True
                elif evenement.key == pygame.K_BACKSPACE:
                    saisie = saisie[:-1]
                else:
                    if len(saisie) < 10:
                        saisie += evenement.unicode
        window.fill(constants.BACKGROUND_COLOR)
        creer_boite_texte((window.get_size()[0] // 2, int(window.get_size()[1]*vertical_positions.input_position)),
                          saisie + "|" * int(show_curseur) + " " * (10 - len(saisie) - 1 * int(show_curseur)),
                          window, fonts["medium"], couleur_fond=constants.DARKER_BACKGROUND_COLOR)
        creer_boite_texte((window.get_size()[0] // 2, int(window.get_size()[1]*vertical_positions.question_position)), question, window,
                          fonts[font_size])
        creer_boite_texte((window.get_size()[0] // 2, int(window.get_size()[
            1]*vertical_positions.warning_position)), warning_message,
                          window,
                          fonts["small"],couleur_texte=constants.WHITE ,couleur_fond=constants.WARNING_COLOR)
        if is_show_grid:
            show_grid(window, fonts=fonts, game=game)
        if is_show_points:
            show_points(window, fonts, game)
        standard_elements(window, fonts)
        pygame.display.update()
        if time.time() - last_tick > 0.5:
            last_tick = time.time()
            show_curseur = not show_curseur  # Inverse la valeur
    return saisie

def move_selection(window, fonts, game, warning_message):
    question = str(game.players[game.current_player-1]
                   ) + ", où voulez vous jouer?"
    distance_between_cells = (
        (8/game.grid_size.y)*(constants.CELL_PADDING[0]+2*constants.CELL_RADIUS+constants.CELL_OFFSET[0]), (8/game.grid_size.y)*(constants.CELL_PADDING[1]+2*constants.CELL_RADIUS+constants.CELL_OFFSET[1]))

    cell_offset = (int(window.get_size()[0]*0.5)-distance_between_cells[0]*((len(game.grid[0])-1)/2), int(
        window.get_size()[1]*0.6)-distance_between_cells[1]*((len(game.grid)-1)/2))

    while True:
        window.fill(constants.BACKGROUND_COLOR)
        creer_boite_texte((window.get_size()[0] // 2, int(window.get_size()[1]*0.12)), question, window,
                        fonts["large"])
        creer_boite_texte((window.get_size()[0] // 2, int(window.get_size()[
                        1]*0.17)), warning_message, window,
                        fonts["small"], couleur_texte=constants.WARNING_COLOR)
        window.fill(constants.BACKGROUND_COLOR)
        show_grid(window, fonts, game)
        show_points(window, fonts, game)
        for evenement in pygame.event.get():
            if evenement.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif evenement.type == pygame.KEYDOWN:
                if evenement.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            elif evenement.type == pygame.MOUSEBUTTONDOWN:
                for i in range(len(game.grid)):
                    if (cell_offset[0]*i-distance_between_cells[0] < pygame.mouse.get_pos()[0] < cell_offset[0]*(i+1)+distance_between_cells[0] and cell_offset[1]*i-distance_between_cells[1] < pygame.mouse.get_pos()[1] < cell_offset[1]*(i+1)+distance_between_cells[1]):
                        print(i)
                        print((cell_offset[0]*i-distance_between_cells[0], cell_offset[1]*i-distance_between_cells[1]))
                        print((cell_offset[0]*(i+1)+distance_between_cells[0], cell_offset[1]*(i+1)+distance_between_cells[1]))
                        pygame.draw.circle(surface=window, color=constants.PLAYER_COLORS[i], center=(cell_offset[0]*i-distance_between_cells[0], cell_offset[1]*i-distance_between_cells[1]), radius=(8/game.grid_size.y)*(constants.CELL_RADIUS))
                        pygame.draw.circle(surface=window, color=constants.PLAYER_COLORS[i], center=(
                            cell_offset[0]*(i+1)+distance_between_cells[0], cell_offset[1]*(i+1)+distance_between_cells[1]), radius=(3/game.grid_size.y)*(constants.CELL_RADIUS))
                        return i+1
        update(window, fonts)




def show_grid(window, fonts, game) :
    distance_between_cells = (
        (8/game.grid_size.y)*(constants.CELL_PADDING[0]+2*constants.CELL_RADIUS+constants.CELL_OFFSET[0]), (8/game.grid_size.y)*(constants.CELL_PADDING[1]+2*constants.CELL_RADIUS+constants.CELL_OFFSET[1]))
    cell_offset = (int(window.get_size()[0]*0.5)-distance_between_cells[0]*((len(game.grid[0])-1)/2), int(window.get_size()[1]*0.6)-distance_between_cells[1]*((len(game.grid)-1)/2))
    for y_index in range(len(game.grid)) :
        for x_index in range(len(game.grid[y_index])) :
            cell_center = cell_offset[0]+x_index * \
                distance_between_cells[0], cell_offset[1] + \
                y_index*distance_between_cells[1]
            pygame.draw.circle(surface=window, color=constants.PLAYER_COLORS[game.grid[y_index][x_index]], center=(
                cell_center), radius=(8/game.grid_size.y)*(constants.CELL_RADIUS))
            if (cell_center) in game.cells_on_winning_horizontal :
                print(cell_center)
                creer_boite_texte((cell_offset[0]+x_index*distance_between_cells[0],
                              cell_offset[1] + y_index*distance_between_cells[1]), "-")


def show_points(window, fonts, game):
    points = functions.count_points(game)
    for i in range(len(points)):
        creer_boite_texte((window.get_size()[0]*0.85, window.get_size()[1]*(0.2+0.07*i)), game.players[i] + " a " + str(
            points[i]) + " points.", window=window, font=fonts["medium"])


def creer_boites_texte_scores(window, fonts, scores, encore, kopecs, j=-1, mises=None):
    """Créer les boites de texte qui permettent l"affichage des scores"""
    joueurs_restants = []
    for joueur in scores.keys():
        if kopecs[joueur] != 0 or mises[joueur] != 0:
            joueurs_restants.append(joueur)
    nombre_de_joueurs = len(joueurs_restants)
    for index_joueur in range(nombre_de_joueurs):
        nom_joueur = joueurs_restants[index_joueur]
        score = scores[nom_joueur]
        taille_font = "medium"
        if nom_joueur == j:
            taille_font = "large"
        if score > 21:
            couleur_texte = constants.RED
        elif nom_joueur == functions.gagnant(scores):
            couleur_texte = constants.OR
        elif not encore[nom_joueur]:
            couleur_texte = constants.GRIS
        else:
            couleur_texte = constants.BLANC
        creer_boite_texte(((window.get_size()[0] // (nombre_de_joueurs + 1)) * (index_joueur + 1),
                           window.get_size()[1] // 2),
                          "*" * (j == nom_joueur) + nom_joueur + " : " + str(scores[nom_joueur]) + "*" * (
                                      j == nom_joueur), window, fonts[taille_font], couleur_texte=couleur_texte)


def creer_boites_texte_kopecs(window, fonts, kopecs, mises, scores):
    """Créer les boites de texte qui permettent l"affichage des kopecs"""
    joueurs_restants = []
    for joueur in scores.keys():
        if kopecs[joueur] != 0 or mises[joueur] != 0:
            joueurs_restants.append(joueur)
    nombre_de_joueurs = len(joueurs_restants)
    for index_joueur in range(nombre_de_joueurs):
        nom_joueur = joueurs_restants[index_joueur]
        taille_font = "medium"
        creer_boite_texte(((window.get_size()[0] // (nombre_de_joueurs + 1)) * (index_joueur + 1),
                           2 * window.get_size()[1] // 3 - 50), nom_joueur + " : " + str(kopecs[nom_joueur]),
                          window, fonts[taille_font])


def creer_boites_texte_gains(window, fonts, kopecs, vainqueur, gain, mises, scores):
    """Créer les boites de texte qui permettent l"affichage des gains (ou pertes)"""
    joueurs_restants = []
    for joueur in scores.keys():
        if kopecs[joueur] != 0 or mises[joueur] != 0:
            joueurs_restants.append(joueur)
    nombre_de_joueurs = len(joueurs_restants)
    for index_joueur in range(nombre_de_joueurs):
        nom_joueur = joueurs_restants[index_joueur]
        taille_font = "medium"
        if nom_joueur == vainqueur:
            couleur_texte = constants.VERT
            creer_boite_texte(((window.get_size()[0] // (nombre_de_joueurs + 1)) * (index_joueur + 1),
                               2 * window.get_size()[1] // 3), "(+" + str(gain - mises[nom_joueur]) + ")",
                              window, fonts[taille_font], couleur_texte=couleur_texte)
        else:
            couleur_texte = constants.RED
            creer_boite_texte(((window.get_size()[0] // (nombre_de_joueurs + 1)) * (index_joueur + 1),
                               2 * window.get_size()[1] // 3), "(-" + str(mises[nom_joueur]) + ")", window,
                              fonts[taille_font], couleur_texte=couleur_texte)


def standard_elements(window, fonts):
    """Fonction qui permet d'afficher des choses tout le temps"""
    creer_boite_texte((window.get_size()[0] * 0.07, window.get_size()[1] * 0.02), "ECHAP pour fermer",
                      window,
                      fonts["small"])


def fin_partie():
    """Attends que l'utilisateur appuie sur la touche échap pour fermer le jeu"""
    while True:
        for evenement in pygame.event.get():
            if evenement.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif evenement.type == pygame.KEYDOWN:
                if evenement.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()