import pygame
import sys 
import tetris_ia
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

clock = pygame.time.Clock()

def show_menu(): 
    button_color = (ROUGE)
    hover_color = (BLEU)
    button_width, button_height = 200, 50
    start_x = ecran.get_width() / 2 - ecran.get_height() / 2
    player_button = Button("Joueur", start_x, 200, button_width, button_height, button_color, hover_color)
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

        player_button.update(mouse_pos)

        player_button.draw(ecran)
        
        if player_button.check_clicked (mouse_pos, mouse_clicked):
            running = False
            tetris_ia()

        pygame.display.flip()
        clock.tick(30)
        

if __name__ == "__main__":
    show_menu()
