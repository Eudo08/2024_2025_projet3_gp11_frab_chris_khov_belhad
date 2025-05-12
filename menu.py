import pygame
import sys 

pygame.init()

NOIR = (0, 0, 0)
BLANC = (255, 255, 255)
GRIS = (193, 193, 193)
BLEU = (0, 150, 255)
BLEU_FONCE = (2, 25, 98)
ROUGE = (255, 0, 0)

ecran = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Tetris")
font = pygame.font.Font(None, 74)
img = pygame.image.load('image/tetris.jfif')
button = pygame.draw.rect(BLANC, (300, 250, 200, 50), "Jouer !", BLANC)

player_pos = pygame.Vector2(ecran.get_width() / 2, ecran.get_height() / 4)

running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.Rect(300, 250, 200, 50).collidepoint(event.pos):
                    main.py()
        # if event.type == pygame.KEYDOWN: 
        #     if event.key == pygame.player_button.K_RIGHT:

    
    ecran.fill(NOIR)

    texte = font.render("TETRIS", True, BLANC)
    texte_rect = texte.get_rect(center=player_pos)
    ecran.blit(texte, texte_rect)

    pygame.display.set_icon(img)

    # player_button = Button("Jouer !", BLANC)

    pygame.display.flip()
    
    clock.tick(60)

pygame.quit()


