import pygame
import random
import pieces

pygame.init()  # Initialisation de Pygame

# ================================
# INITIALISATION DE BASE
# ================================


# Fenêtre et grille
largeur = 800
hauteur = 600
grid_height = 20
grid_width = 10
taille_bloc = 25
grid_cellsize = 0
grid_cells = []
grid_centerX = 0
grid_centerY = 0
grid = []

# Variables de jeu
score = 0
lignes_supprimees = 0
en_cours = True
gravity_time = 1
timerdrop = gravity_time

# Position de la pièce
piece_pos_x = grid_width // 2 - 2
piece_pos_y = -1
rotation = 0
piece_id = random.choice(list(pieces.tetros.keys()))

# Couleurs
NOIR = (0, 0, 0)
BLANC = (255, 255, 255)
GRIS = (193, 193, 193)
BLEU = (0, 150, 255)

# Polices
font = pygame.font.Font("assets/font/Drawliner.ttf", 30)
font2 = pygame.font.Font("assets/font/game_over.ttf", 50)

# Fenêtre et autres objets
fenetre = pygame.display.set_mode((largeur, hauteur))
pygame.display.set_caption("Tetris")
clock = pygame.time.Clock()
player_pos = pygame.Vector2(largeur / 2, hauteur / 4)


def main():

    global largeur, hauteur, grid_height, grid_width, taille_bloc, grid_cellsize, grid_cells
    global grid_centerX, grid_centerY, score, lignes_supprimees, en_cours, gravity_time
    global timerdrop, piece_pos_x, piece_pos_y, rotation, piece_id
    global NOIR, BLANC, GRIS, BLEU, font, font2, fenetre, clock, player_pos

    # pygame.init()  # Initialisation de Pygame


    # ================================
    # INITIALISATION DE LA GRILLE
    # ================================


    def init_grid():
        """
        Initialise la grille de jeu avec des cellules vides.
        """

        largeur = 800
        hauteur = 600
        grid_height = 20
        grid_width = 10

        global grid_cellsize, grid_cells, grid_centerX, grid_centerY
        h = hauteur / grid_height
        grid_cellsize = h
        grid_centerX = (largeur / 2) - (h * grid_width) / 2
        grid_centerY = 0
        grid_cells = [[0 for _ in range(grid_width)] for _ in range(grid_height)]

        taille_bloc = 25
        score = 0
        font = pygame.font.Font("assets/font/Drawliner.ttf",30)
        font2 = pygame.font.Font("assets/font/game_over.ttf", 50)
        grid = []
        grid_cellsize = 0
        grid_cells = []
        grid_centerX = 0
        grid_centerY = 0
        piece_pos_x = grid_width // 2 - 2
        piece_pos_y = -1
        gravity_time = 1
        timerdrop = gravity_time
        player_pos = pygame.Vector2(largeur / 2, hauteur / 4)
        
        def init_grid():
            global grid_cellsize, grid_cells, grid_centerX, grid_centerY
            h = hauteur / grid_height
            grid_cellsize = h
            grid_centerX = (largeur / 2) - (h * grid_width) / 2
            grid_centerY = 0


    def draw_grid():
        """
        Dessine la grille de jeu sur la fenêtre.
        """
        h = grid_cellsize
        w = h
        for i in range(grid_height):
            for j in range(grid_width):
                x = grid_centerX + j * w
                y = grid_centerY + i * h
                pygame.draw.rect(fenetre, BLANC, (x, y, w, h), 1)


    def draw_locked_cells():
        """
        Dessine les cellules verrouillées de la grille.
        """
        for i in range(grid_height):
            for j in range(grid_width):
                if grid_cells[i][j] != 0:
                    x = grid_centerX + j * grid_cellsize
                    y = grid_centerY + i * grid_cellsize
                    couleur = grid_cells[i][j]
                    pygame.draw.rect(fenetre, couleur, (x, y, grid_cellsize, grid_cellsize))
                    pygame.draw.rect(fenetre, GRIS, (x, y, grid_cellsize, grid_cellsize), 1)



    # ================================
    # INITIALISATION DES PIECES
    # ================================


    def nouvelle_piece():
        """
        Génère une nouvelle pièce aléatoire et réinitialise la rotation.
        """
        global piece_id, rotation
        piece_id = random.choice(list(pieces.tetros.keys()))
        rotation = 0

        def nouvelle_piece():
            global piece_id, rotation
            piece_id = random.choice(list(pieces.tetros.keys()))
            rotation = 0

    def dessiner_piece(piece_id, rotation, case_x, case_y):
        """
        Dessine la pièce actuelle sur la grille.
        """
        piece = pieces.tetros[piece_id]["rotations"][rotation]
        couleur = pieces.tetros[piece_id]["couleur"]
        for i in range(4):
            for j in range(4):
                if piece[i][j]:
                    x= grid_centerX + (case_x + j) * grid_cellsize
                    y= grid_centerY + (case_y + i) * grid_cellsize
                    pygame.draw.rect(fenetre, couleur, (x, y, grid_cellsize, grid_cellsize))
                    pygame.draw.rect(fenetre, GRIS, (x, y, grid_cellsize, grid_cellsize), 1)



    # ================================
    # FONCTIONS D'AIDE PRINCIPALES
    # ================================


    def next_drop(dt):
        """
        Gère la chute de la pièce actuelle en fonction du temps écoulé.
        """
        global timerdrop, piece_pos_y, piece_pos_x, score

        timerdrop -= dt
        if timerdrop <= 0:
            piece = pieces.tetros[piece_id]["rotations"][rotation]
            couleur = pieces.tetros[piece_id]["couleur"]
            for i in range(4):
                for j in range(4):
                    if piece[i][j]:
                        x= grid_centerX + (piece_pos_x + j) * grid_cellsize
                        y= grid_centerY + (piece_pos_y + i) * grid_cellsize
                        pygame.draw.rect(fenetre, couleur, (x, y, grid_cellsize, grid_cellsize))
                        pygame.draw.rect(fenetre, GRIS, (x, y, grid_cellsize, grid_cellsize), 1)



        def next_drop(dt):
            global timerdrop, piece_pos_y, piece_pos_x, score

            timerdrop -= dt
            if timerdrop <= 0:
                piece = pieces.tetros[piece_id]["rotations"][rotation]
                can_move = True

            if can_move:
                piece_pos_y += 1
            else:
                for i in range(4):
                    for j in range(4):
                        if piece[i][j]:
                            new_y = piece_pos_y + i + 1
                            new_x = piece_pos_x + j
                            if new_y >= grid_height or (new_y >= 0 and grid_cells[new_y][new_x] != 0):
                                can_move = False
                                break
                        
                                
                    if not can_move:
                        break

                nouvelle_piece()
                piece_pos_x = grid_width // 2 - 2
                piece_pos_y = -1

            timerdrop = gravity_time


    def nouv_tetros():
        """
        Vérifie si la pièce actuelle peut être placée dans la grille.
        """
        global piece_pos_x, piece_pos_y, grid_cells

        piece = pieces.tetros[piece_id]["rotations"][rotation]
        
        
        for i in range(4):
            for j in range(4):
                if piece[i][j]:  
                    grid_y = piece_pos_y + i
                    grid_x = piece_pos_x + j

                
                    if grid_y >= grid_height or grid_x < 0 or grid_x >= grid_width:
                        place_piece_in_grid(piece, piece_pos_y, piece_pos_x)
                        piece_pos_x = grid_width // 2 - 2
                        piece_pos_y = 0
                        nouvelle_piece()
                        return
                    
                    if grid_y >= 0 and grid_cells[grid_y][grid_x] != 0:
                       place_piece_in_grid(piece, piece_pos_y, piece_pos_x)
                       piece_pos_x = grid_width // 2 - 2
                       piece_pos_y = 0
                       nouvelle_piece()
                       return
                    
    def place_piece_in_grid(piece, pos_y, pos_x):
        """
        Place la pièce dans la grille en la verrouillant à sa position actuelle.
        """
        for i in range(4):
            for j in range(4):
                if piece[i][j]:
                    grid_y = pos_y + i
                    grid_x = pos_x + j
                    if 0 <= grid_y < grid_height and 0 <= grid_x < grid_width:
                        grid_cells[grid_y][grid_x] = pieces.tetros[piece_id]["couleur"]


    def supprimer_lignes():
        """
        Supprime les lignes complètes de la grille et renvoie le nombre de lignes supprimées.
        """
        global grid_cells
        lignes_supprimees = 0
        i = grid_height - 1
        while i >= 0:
            if all(grid_cells[i][j] != 0 for j in range(grid_width)):
                del grid_cells[i]
                grid_cells.insert(0, [0] * grid_width)
                lignes_supprimees += 1
            else:
                i -= 1
        return lignes_supprimees



    # ================================
    # BOUCLE PRINCIPALE
    # ================================


    # Initialisation de la fenêtre et de la grille
    clock = pygame.time.Clock()
    init_grid()
    origine_x = grid_centerX
    origine_y = grid_centerY


    while en_cours:
        """
        Boucle principale du jeu, gère les événements, le dessin de la grille
        """
        for evenement in pygame.event.get():
            if evenement.type == pygame.QUIT:
                en_cours = False

            elif evenement.type == pygame.KEYDOWN:
                if evenement.key == pygame.K_SPACE:
                    new_rotation = (rotation + 1) % len(pieces.tetros[piece_id]["rotations"])
                    new_piece = pieces.tetros[piece_id]["rotations"][new_rotation]

                    valide = True
                    for i in range(4):
                        for j in range(4):
                            if new_piece[i][j]:
                                x = piece_pos_x + j
                                y = piece_pos_y + i

                                if x < 0 or x >= grid_width or y >= grid_height:
                                    valide = False
                                    break  
                                elif y >= 0 and grid_cells[y][x] != 0:
                                    valide = False
                                    break 

                        if not valide:
                            break  

                    if valide:
                        rotation = new_rotation

                elif evenement.key == pygame.K_ESCAPE:
                    en_cours = False

                elif evenement.key == pygame.K_LEFT:
                    piece_pos_x -= 1
                    piece = pieces.tetros[piece_id]["rotations"][rotation]

                    for i in range(4):
                        for j in range(4):
                            if piece[i][j]:
                                new_x = piece_pos_x + j
                                new_y = piece_pos_y + i
                                if new_x < 0 or (new_y >= 0 and grid_cells[new_y][new_x] != 0):
                                    piece_pos_x += 1  
                                    break

                elif evenement.key == pygame.K_RIGHT:
                    piece_pos_x += 1
                    piece = pieces.tetros[piece_id]["rotations"][rotation]

                    for i in range(4):
                        for j in range(4):
                            if piece[i][j]:
                                new_x = piece_pos_x + j
                                new_y = piece_pos_y + i
                                if new_x >= grid_width or (new_y >= 0 and grid_cells[new_y][new_x] != 0):
                                    piece_pos_x -= 1  # annule le déplacement
                                    break


        # Dessin de la grille et des pièces
        fenetre.fill(NOIR)
        draw_grid()

        # Dessiner la pièce actuelle
        nouv_tetros()
        draw_locked_cells()
        dessiner_piece(piece_id, rotation, piece_pos_x, piece_pos_y)

        # Paramètres de jeu
        dt = clock.tick(30) 
        next_drop(dt)
        score_text = font.render(f"score: {score}", True, BLANC)
        fenetre.blit(score_text, (10, 10))
        pygame.display.flip()


    # ================================
    # GAME OVER
    # ================================


    # Affichage du message de fin de jeu
    text_gameover = font2.render("Game over", True, BLANC)
    text_rect = text_gameover.get_rect(center=player_pos)
    fenetre.blit(text_gameover, text_rect)
    pygame.display.flip()

    # Attente de la fermeture de la fenêtre
    attente = True
    while attente:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                attente = False



    pygame.quit()

if __name__ == "__main__":
    main()