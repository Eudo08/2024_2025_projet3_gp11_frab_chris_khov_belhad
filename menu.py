import pygame

pygame.init()

NOIR = (0, 0, 0)
BLANC = (255, 255, 255)
GRIS = (193, 193, 193)
BLEU = (0, 150, 255)
BLEU_FONCE = (2, 25, 98)

ecran = pygame.display.set_mode((800, 600))

running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    ecran.fill(BLEU_FONCE)
    pygame.display.update()

    clock.tick(60)

pygame.quit()