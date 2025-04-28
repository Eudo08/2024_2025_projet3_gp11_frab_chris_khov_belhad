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
piece_pos_x = grid_width // 2 - 2
piece_pos_y = -1
gravity_time = 1
timerdrop = gravity_time

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

def dessiner_piece(piece_id, rotation, case_x, case_y):
    piece = pieces.tetros[piece_id]["rotations"][rotation]
    couleur = pieces.tetros[piece_id]["couleur"]
    for i in range(4):
        for j in range(4):
            if piece[i][j]:
                x= grid_centerX + (case_x + j) * grid_cellsize
                y= grid_centerY + (case_y + i) * grid_cellsize
                pygame.draw.rect(fenetre, couleur, (x, y, grid_cellsize, grid_cellsize))
                pygame.draw.rect(fenetre, GRIS, (x, y, grid_cellsize, grid_cellsize), 1)



def next_drop(dt):
    global timerdrop, piece_pos_y
    timerdrop -= dt
    if timerdrop <= 0:
        piece_pos_y += 1
        timerdrop = gravity_time  



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
            elif evenement.key == pygame.K_LEFT:
                piece_pos_x -= 1
                piece = pieces.tetros[piece_id]["rotations"][rotation]
                for i in range(4):
                    for j in range(4):
                        if piece[i][j]:  
                            if piece_pos_x + j < 0: 
                                piece_pos_x += 1  
                                break
            elif evenement.key == pygame.K_RIGHT:
                piece_pos_x += 1
                piece = pieces.tetros[piece_id]["rotations"][rotation]
                for i in range(4):
                    for j in range(4):
                        if piece[i][j]:  
                            if piece_pos_x + j >= grid_width:  
                                piece_pos_x -= 1  
                                break




    fenetre.fill(NOIR)
    draw_grid()
    dessiner_piece(piece_id, rotation, piece_pos_x, piece_pos_y)

    dt = clock.tick(30) 
    next_drop(dt)

    pygame.display.flip()
    clock.tick(1)
pygame.quit ()