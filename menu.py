import pygame

pygame.init()

NOIR = (0, 0, 0)
BLANC = (255, 255, 255)
GRIS = (193, 193, 193)
BLEU = (0, 150, 255)
BLEU_FONCE = (2, 25, 98)

ecran = pygame.display.set_mode((800, 600))
font = pygame.font.Font(None, 74)

player_pos = pygame.Vector2(ecran.get_width() / 2, ecran.get_height() / 4)

running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    ecran.fill(NOIR)

    texte = font.render("TETRIS", True, BLANC)
    texte_rect = texte.get_rect(center=player_pos)
    ecran.blit(texte, texte_rect)

    pygame.display.flip()
    
    clock.tick(60)

pygame.quit()


