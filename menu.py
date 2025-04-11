import pygame

pygame.init()

NOIR = (0, 0, 0)
BLANC = (255, 255, 255)
GRIS = (193, 193, 193)
BLEU = (0, 150, 255)

ecran = pygame.display.set_mode((800, 600))

continuer = True

while continuer:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            continuer = False

ecran.fill(NOIR)
clock = pygame.time.Clock()

pygame.quit()