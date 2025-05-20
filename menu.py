import pygame
import sys 
import tetris_ia
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
font = pygame.font.Font("assets/font/Drawliner.ttf",150)
img = pygame.image.load('image/tetris.jfif')
pygame.display.set_icon(img)

player_pos = pygame.Vector2(ecran.get_width() / 2, ecran.get_height() / 4)

clock = pygame.time.Clock()

def show_menu(): 

    button_color = (ROUGE)
    hover_color = (BLEU)
    button_width, button_height = 200, 50

    start_x = ecran.get_width() / 2 - ecran.get_height() / 2

    ia_button = Button("IA", 150, 450, button_width, button_height, button_color, hover_color)
    player_button = Button("Jouer !", 450, 450, button_width, button_height, button_color, hover_color)

    running = True

    while running:
        ecran.fill(NOIR)

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

        ia_button.update(mouse_pos)
        player_button.update(mouse_pos)

        ia_button.draw(ecran)
        player_button.draw(ecran)
        
        if ia_button.check_clicked (mouse_pos, mouse_clicked):
            running = False
            tetris_ia()

        if player_button.check_clicked (mouse_pos, mouse_clicked):
            running = False
            tetris_j()

        pygame.display.flip()
        clock.tick(30)
        

if __name__ == "__main__":
    show_menu()
