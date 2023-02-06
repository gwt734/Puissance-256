#!/usr/bin/env python3
import constants
import functions
import types_and_inits
import gui

def main():
    if (constants.IS_GUI_ENABLED) :
        window, fonts = gui.window_init()
    else :
        print("Bienvenue dans cette partie de Puissance 256 ! \n")
    
    veut_rejouer = True
    nb_parties = 0
    
    while veut_rejouer:
        is_base_param = functions.input_protege("Souhaitez-vous jouer avec les paramètres de base ?", range_or_list="list", valid_answers_list=["Oui","Non"],window=window,fonts=fonts, default_answer="Oui") in [
            "oui", "Oui", "OUI"]
        if is_base_param:
            joueurs = functions.init_joueurs(2, window, fonts) 
            game = types_and_inits.game(joueurs)
        else:
            nb_joueurs = functions.input_protege("Combien de joueurs jouerons ?", answer_type=int, range_or_list="range", valid_answers_interval=(2, 5), default_answer="2", window=window, fonts=fonts) # Demande le nombre de joueurs
            joueurs = functions.init_joueurs(nb_joueurs, window, fonts)
            taille_grille = functions.input_protege("Quelle est la dimension du plateau ?",answer_type=int, range_or_list="range", valid_answers_interval=(3, 15), default_answer=str(constants.DEFAULT_GRID_SIZE[0]), window=window, fonts=fonts)
            winning_size = functions.input_protege("Quelle est la taille minimum d'une ligne gagnante ?",answer_type=int, range_or_list="range", valid_answers_interval=(2, taille_grille),default_answer=constants.DEFALUT_WINNING_SIZE, window=window, fonts=fonts)
            game = types_and_inits.game(joueurs,player_count=nb_joueurs,grid_size=types_and_inits.position(taille_grille,taille_grille), winning_size=winning_size)
        nb_parties += 1

        functions.play_game(game,window=window,fonts=fonts)
        veut_rejouer = functions.is_replay_asked(window=window, fonts=fonts, game=game)

if __name__ == "__main__":
    main()