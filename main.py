import pygame
import random
import pieces


pygame.init()

largeur = 800
hauteur = 600
taille_bloc = 25
origine_x = 330
origine_y = 0

# Couleurs
NOIR = (0, 0, 0)
BLANC = (255, 255, 255)
GRIS = (193, 193, 193)
BLEU = (0, 150, 255)

piece_id = random.choice(list(pieces.tetros.keys()))
rotation = 0

def nouvelle_piece():
    global piece_id, rotation
    piece_id = random.choice(list(pieces.tetros.keys()))
    rotation = 0

def dessiner_piece(piece_id, rotation, x, y):
    piece = pieces.tetros[piece_id]["rotations"][rotation]
    couleur = pieces.tetros[piece_id]["couleur"]
    for i in range(4):
        for j in range(4):
            if piece[i][j]:
                pygame.draw.rect(fenetre, couleur, (x + j * taille_bloc, y + i * taille_bloc, taille_bloc, taille_bloc))
                pygame.draw.rect(fenetre, GRIS, (x + j * taille_bloc, y + i * taille_bloc, taille_bloc, taille_bloc), 1)


fenetre = pygame.display.set_mode((largeur, hauteur))
pygame.display.set_caption("Tetris")

en_cours = True
clock = pygame.time.Clock()

while en_cours:
    for evenement in pygame.event.get():
        if evenement.type == pygame.QUIT:
            en_cours = False
        elif evenement.type == pygame.KEYDOWN:
            if evenement.key == pygame.K_SPACE:
                nouvelle_piece()  
            elif evenement.key == pygame.K_DOWN:
                rotation = (rotation + 1) % len(pieces.tetros[piece_id]["rotations"])
            elif evenement.key == pygame.K_ESCAPE:
                en_cours = False




    fenetre.fill(NOIR)
    dessiner_piece(piece_id, rotation, origine_x, origine_y)

    pygame.display.flip()
    clock.tick(30)
pygame.quit ()