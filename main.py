import pygame
import random

pygame.init()

largeur = 800
hauteur = 600

fenetre = pygame.display.set_mode((largeur, hauteur))
pygame.display.set_caption("Tetris")

en_cours = True
while en_cours:
    for evenement in pygame.event.get():
        if evenement.type == pygame.QUIT:
            en_cours = False

pygame.quit ()