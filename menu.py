import pygame
import sys 
import tetris_ia
import tetris_j
from tools import Button

pygame.init() # Initialisation de Pygame


# ================================
# INITIALISATION DE BASE
# ================================

# Couleurs
NOIR = (0, 0, 0)
BLANC = (255, 255, 255)
ORANGE = (255,140,0)
ROUGE = (255, 0, 0)

# Initialisation de la fenêtre
ecran = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Tetris")
font = pygame.font.Font("assets/font/Drawliner.ttf",130)
img = pygame.image.load('image/tetris.jfif')
pygame.display.set_icon(img)
clock = pygame.time.Clock()

# Images illustratives
img_ia = pygame.image.load ('image/tetris_ia.png')
position_img_ia = (470, 260)
new_sise = (160, 160)
new_img_ia = pygame.transform.scale(img_ia, new_sise)
img_j = pygame.image.load ('image/tetris_j.jpg')
position_img_j = (170, 260)
new_img_j = pygame.transform.scale(img_j, new_sise)

# Position du texte
player_pos = pygame.Vector2(ecran.get_width() / 2, ecran.get_height() / 4)


# Fonction pour afficher le menu principal
def show_menu(): 

    # ================================
    # AFFICHAGE
    # ================================

    button_color = (ROUGE)
    hover_color = (ORANGE)
    button_width, button_height = 200, 50

    ia_button = Button("IA", 450, 450, button_width, button_height, button_color, hover_color)
    player_button = Button ("Jouer !", 150, 450, button_width, button_height, button_color, hover_color)

    running = True

    # Boucle principale du menu
    while running:
        ecran.fill(NOIR)

        texte = font.render("TETRIS", True, BLANC) 
        texte_rect = texte.get_rect(center=player_pos)
        ecran.blit(texte, texte_rect)
        ecran.blit(new_img_ia, position_img_ia)
        ecran.blit(new_img_j, position_img_j)

        # Detection de la souris
        mouse_pos = pygame.mouse.get_pos ()
        mouse_clicked = False

    # ================================
    # BOUCLE PRINCIPALE DU JEU
    # ================================

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_clicked = True
        
        # Création des boutons
        ia_button.update(mouse_pos)
        player_button.update(mouse_pos)

        ia_button.draw(ecran)
        player_button.draw(ecran)
        
        if ia_button.check_clicked (mouse_pos, mouse_clicked):
            running = False
            tetris_ia.main()

        elif player_button.check_clicked (mouse_pos, mouse_clicked):
            running = False
            tetris_j.main()

        pygame.display.flip()
        clock.tick(30)
        

if __name__ == "__main__":
    show_menu()