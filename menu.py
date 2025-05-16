import pygame
import sys 
import tetris_j
from tools import Button

pygame.init()

NOIR = (0, 0, 0)
BLANC = (255, 255, 255)
GRIS = (193, 193, 193)
BLEU = (0, 150, 255)
BLEU_FONCE = (2, 25, 98)
ROUGE = (255, 0, 0)

ecran = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Tetris")
font = pygame.font.Font("image/Drawliner.ttf",30)
img = pygame.image.load('image/tetris.jfif')
pygame.display.set_icon(img)

player_pos = pygame.Vector2(ecran.get_width() / 2, ecran.get_height() / 4)

running = True
clock = pygame.time.Clock()


# # while running:
# #     ecran.fill(NOIR)
# #     draw_button(ecran, (300, 250, 200, 50), "Jouer !", BLANC, ROUGE)
# #     texte = font.render("TETRIS", True, BLANC)
# #     texte_rect = texte.get_rect(center=player_pos)
# #     ecran.blit(texte, texte_rect)

# #     for event in pygame.event.get():
# #         if event.type == pygame.QUIT:
# #             running = False
# #             sys.exit()
# #         elif event.type == pygame.MOUSEBUTTONDOWN:
# #                 if 300 <= event.pos[0] <= 500 and 250 <= event.pos[1] <= 300:
# #                     en_cours()

# etat_jeu = "menu"

# while running:
#     ecran.fill(NOIR)

#     if etat_jeu == "menu":
#         draw_button(ecran, "Jouer !", 300, 250, 200, 50, BLANC, ROUGE)
#         texte = font.render("TETRIS", True, BLANC)
#         texte_rect = texte.get_rect(center=player_pos)
#         ecran.blit(texte, texte_rect)

#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 running = False
#                 sys.exit()
#             elif event.type == pygame.MOUSEBUTTONDOWN:
#                 if 300 <= event.pos[0] <= 500 and 250 <= event.pos[1] <= 300:
#                     etat_jeu = "jeu"  # Change l'état du jeu

#     elif etat_jeu == "jeu":
#         en_cours()

# pygame.quit()

# def draw_button(ecran, text, x, y, w, h, color, text_color):
#     pygame.draw.rect(ecran, (x, y, w, h))
#     text_surface = font.render(text, True, text_color)
#     text_rect = text_surface.get_rect(center=(x + w // 2, y + h // 2))
#     ecran.blit(text_surface, text_rect)

def show_menu():
    button_color = (ROUGE)
    hover_color = (BLEU)
    button_width, button_height = 200, 50
    start_x = ecran.get_width() / 2 - ecran.get_height() / 2
    player_button = Button("Joueur", start_x, 200, button_width, button_height, button_color, hover_color)

    menu_running = True
    while menu_running:
        ecran.fill(NOIR)

        font_title = pygame.font.SysFont (None, 60)
        texte = font.render("TETRIS", True, BLANC) 
        texte_rect = texte.get_rect(center=player_pos)
        ecran.blit(texte, texte_rect)

        mouse_pos = pygame.mouse.get_pos ()
        mouse_clicked = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_clicked = True

        player_button.update(mouse_pos)

        player_button.draw(ecran)
        
        if player_button.check_cliked (mouse_pos, mouse_clicked):
            menu_running = False
            tetris_j()
        




# while running: 
#     ecran.fill(NOIR) 
#     texte = font.render("TETRIS", True, BLANC) 
#     texte_rect = texte.get_rect(center=player_pos)
#     ecran.blit(texte, texte_rect)
#     draw_button(BLANC, (300, 250, 200, 50), "Jouer !", BLANC) 

#     for event in pygame.event.get(): 
#         if event.type == pygame.QUIT: 
#             running = False 
#             sys.exit()
#         elif event.type == pygame.MOUSEBUTTONDOWN: 
#             if 300 <= event.pos[0] <= 500 and 250 <= event.pos[1] <= 300: 
#                 en_cours() 
    
#     ecran.fill(NOIR) 
#     texte = font.render("TETRIS", True, BLANC) 
#     texte_rect = texte.get_rect(center=player_pos)
#     ecran.blit(texte, texte_rect)  
                                                            
#     pygame.display.flip() 
#     clock.tick(60) 
    
#     pygame.quit()
