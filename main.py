import pygame
import random
import pieces


pygame.init()

largeur = 800
hauteur = 600
taille_bloc = 25


grid = []
grid_height = 20
grid_width = 10
grid_cellsize = 0
grid_cells = []
grid_centerX = 0
grid_centerY = 0

def init_grid():
    global grid_cellsize, grid_cells, grid_centerX, grid_centerY
    h = hauteur / grid_height
    grid_cellsize = h
    grid_centerX = (largeur / 2) - (h * grid_width) / 2
    grid_centerY = 0

    grid_cells = []
    for i in range(grid_height):
        row = []
        for j in range(grid_width):
            row.append(0)
        grid_cells.append(row)

def draw_grid():
    h = grid_cellsize
    w = h
    for i in range(grid_height):
        for j in range(grid_width):
            x = grid_centerX + j * w
            y = grid_centerY + i * h
            pygame.draw.rect(fenetre, BLANC, (x, y, w, h), 1)

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
init_grid()
origine_x = grid_centerX
origine_y = grid_centerY
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
    draw_grid()
    dessiner_piece(piece_id, rotation, origine_x, origine_y)

    pygame.display.flip()
    clock.tick(30)
pygame.quit ()