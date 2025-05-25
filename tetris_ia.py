# import pygame
# import random
# import pieces
# import utils
# import copy
# import time

# # ================================
# # INITIALISATION DE BASE
# # ================================

# pygame.init()

# # Fenêtre et grille
# largeur = 800
# hauteur = 600
# taille_bloc = 25
# grid_height = 20
# grid_width = 6
# fenetre = pygame.display.set_mode((largeur, hauteur))
# pygame.display.set_caption("Tetris")

# # Grille logique
# grid = []
# grid_cellsize = int(hauteur // grid_height)
# grid_cells = []
# grid_centerX = 0
# grid_centerY = 0

# piece_types = [1, 2]  # 1 = I, 2 = carré
# current_piece_id = random.choice(piece_types)

# # Position de la pièce
# piece_pos_x = grid_width // 2 - 2
# piece_pos_y = 0

# # Couleurs
# NOIR = (0, 0, 0)
# BLANC = (255, 255, 255)
# GRIS = (193, 193, 193)
# BLEU = (0, 150, 255)
# ROUGE = (255, 0, 0)

# # Polices
# font = pygame.font.Font("assets/font/Drawliner.ttf", 30)
# font2 = pygame.font.Font("assets/font/game_over.ttf", 50)

# # Variables de jeu
# score = 0
# game_over = False
# lignes_supprimees = 0
# etat_id = 0
# rotation = 0
# piece_id = 2
# gravity_time = 200
# timerdrop = gravity_time
# player_pos = pygame.Vector2(largeur / 2, hauteur / 4)

# # Hyperparamètres de l'IA
# epsilon = 0.1
# alpha = 0.1
# gamma = 0.9

# # Bordures / états
# dico_bordures = utils.charger_dico_json("bordures.json")
# if dico_bordures:
#     etat_id = max(map(int, dico_bordures.keys())) + 1

# # ================================
# # INITIALISATION DE LA GRILLE
# # ================================

# def init_grid():
#     """
#     Initialise la grille de jeu vide et les coordonnées de placement.
#     """
#     global grid_cellsize, grid_cells, grid_centerX, grid_centerY
#     grid_cellsize = int(hauteur // grid_height)
#     grid_centerX = (largeur / 2) - (grid_cellsize * grid_width) / 2
#     grid_centerY = 0

#     grid_cells = []
#     for i in range(grid_height):
#         row = []
#         for j in range(grid_width):
#             row.append(0)
#         grid_cells.append(row)

# # ================================
# # AFFICHAGE
# # ================================

# def draw_grid():
#     """
#     Dessine la grille en fil de fer.
#     """
#     h = grid_cellsize
#     w = h
#     for i in range(grid_height):
#         for j in range(grid_width):
#             x = grid_centerX + j * grid_cellsize
#             y = grid_centerY + i * grid_cellsize
#             pygame.draw.rect(fenetre, BLANC, (x, y, grid_cellsize, grid_cellsize), 1)

# def draw_current_piece(piece_id):
#     piece = pieces.tetros[piece_id]["rotations"][0]  # On prend la première rotation
#     couleur = pieces.tetros[piece_id]["couleur"]
#     # Position de départ (en haut, centré)
#     start_x = grid_width // 2 - 2
#     start_y = 0
#     for i in range(4):
#         for j in range(4):
#             if piece[i][j]:
#                 x = grid_centerX + (start_x + j) * grid_cellsize
#                 y = grid_centerY + (start_y + i) * grid_cellsize
#                 pygame.draw.rect(fenetre, couleur, (x, y, grid_cellsize, grid_cellsize))
#                 pygame.draw.rect(fenetre, GRIS, (x, y, grid_cellsize, grid_cellsize), 1)

# def draw_locked_cells(cells):
#     """
#     Affiche les blocs déjà posés dans la grille.
#     """
#     for i in range(grid_height):
#         for j in range(grid_width):
#             if isinstance(cells[i][j], tuple):
#                 x = grid_centerX + j * grid_cellsize
#                 y = grid_centerY + i * grid_cellsize
#                 couleur = cells[i][j]
#                 pygame.draw.rect(fenetre, couleur, (x, y, grid_cellsize, grid_cellsize))
#                 pygame.draw.rect(fenetre, GRIS, (x, y, grid_cellsize, grid_cellsize), 1)


# def supprimer_lignes(cells):
#     """
#     Supprime les lignes pleines et les remplace par des lignes vides.
#     """
#     nouvelles_lignes = []
#     lignes_supprimees = 0
#     for i in range(grid_height):
#         if all(cells[i][j] != 0 for j in range(grid_width)):
#             lignes_supprimees += 1
#         else:
#             nouvelles_lignes.append(cells[i])
#     # Ajoute des lignes vides en haut
#     while len(nouvelles_lignes) < grid_height:
#         nouvelles_lignes.insert(0, [0] * grid_width)
#     return nouvelles_lignes, lignes_supprimees

# def get_possibles_grids(grid_cells, piece_id):
#     result_grids = []
#     piece = pieces.tetros[piece_id]["rotations"][0]  # On prend la première rotation pour simplifier

#     # Largeur de la pièce (pour éviter de sortir de la grille)
#     largeur_piece = max(j for i in range(4) for j in range(4) if piece[i][j]) + 1

#     for start_col in range(grid_width - largeur_piece + 1):
#         new_grid = copy.deepcopy(grid_cells)
#         current_y = 0
#         good = False
#         while not good and current_y < grid_height - 4 + 1:
#             collision = False
#             for i in range(4):
#                 for j in range(4):
#                     if piece[i][j]:
#                         grid_y = current_y + i
#                         grid_x = start_col + j
#                         if grid_y >= grid_height or new_grid[grid_y][grid_x] != 0:
#                             collision = True
#             if not collision:
#                 current_y += 1
#             else:
#                 current_y -= 1
#                 good = True

#         # Pose la pièce à la dernière position valide
#         for i in range(4):
#             for j in range(4):
#                 if piece[i][j]:
#                     grid_y = current_y + i
#                     grid_x = start_col + j
#                     if 0 <= grid_y < grid_height and 0 <= grid_x < grid_width:
#                         new_grid[grid_y][grid_x] = pieces.tetros[piece_id]["couleur"]

#         result_grids.append(new_grid)

#     return result_grids


# def calculer_recompense(game_over, lignes_supprimees, ancienne_hauteur, nouvelle_hauteur, has_collision=False):
#     """
#     Détermine une récompense pour l'IA selon l'état du jeu.
#     """
#     recompense = 1
#     if has_collision:
#         recompense -= 100
#     if game_over:
#         recompense -= 50
#     recompense += 20 * lignes_supprimees
#     if nouvelle_hauteur > ancienne_hauteur:
#         recompense -= 5
#     return recompense



# en_cours = True                    # Booléen de contrôle pour savoir si le jeu tourne encore
# clock = pygame.time.Clock()       # Horloge pour réguler les FPS
# init_grid()                       # Initialisation de la grille de jeu


# class Q_Table():
#     def __init__(self):
#         self.data = {}

#     def add(self,current,scores):
#         self.data[str(current)] = scores

#     def get_best(self,current):
#         if str(current) in self.data:
#             return self.data[str(current)].index(max(self.data[str(current)]))
#         return random.randint(0,5)

#     def save(self):
#         utils.sauvegarder_dico_json(self.data, "bordures.json")

#     def load(self):
#         self.data = utils.charger_dico_json("bordures.json")

# table = Q_Table()
# training = True

# if not training:
#     table.load()

# while en_cours:
#     dt = clock.tick(1)           # Limite la boucle à 60 FPS et récupère le temps écoulé depuis le dernier tick


#     if training:
#         current_piece_id = random.choice(piece_types)
#         results = get_possibles_grids(grid_cells, current_piece_id)
#         game_over = False
#         scores = []

#         for b in results:
#             previous_max = grid_height-next((i for i, sub in enumerate(grid_cells) if any(x != 0 for x in sub)), -1)
#             a,lignes_supprimees = supprimer_lignes(b)
#             new_max = grid_height-next((i for i, sub in enumerate(a) if any(x != 0 for x in sub)), -1)
#             if next((i for i, sub in enumerate(a) if any(x != 0 for x in sub)), 100) > 0:
#                 scores.append(calculer_recompense(False,lignes_supprimees,previous_max,new_max,False))
#             else:
#                 scores.append(-1000)

#         if sum(scores) / len(scores) <= -1000:
#             game_over = True

#         if game_over:
#             en_cours = False

#         new_move = scores.index(max(scores))
#         current_id = int(''.join(str(int(bool(x))) for sub in grid_cells for x in sub), 2)
#         grid_cells = results[new_move]
#         grid_cells,num_deleted_lines = supprimer_lignes(grid_cells)
#         new_id = int(''.join(str(int(bool(x))) for sub in grid_cells for x in sub), 2)

#         score += max(scores)
#     else:
#         previous_max = grid_height-next((i for i, sub in enumerate(grid_cells) if any(x != 0 for x in sub)), -1)
#         results = get_possibles_grids(grid_cells, piece_id)
#         current_id = int(''.join(str(int(bool(x))) for sub in grid_cells for x in sub), 2)
#         print(current_id)
#         new_move = table.get_best(current_id)
#         grid_cells = results[new_move]
#         grid_cells,num_deleted_lines = supprimer_lignes(grid_cells)
#         new_max = grid_height-next((i for i, sub in enumerate(grid_cells) if any(x != 0 for x in sub)), -1)
#         new_id = int(''.join(str(int(bool(x))) for sub in grid_cells for x in sub), 2)
#         current_piece_id = random.choice(piece_types)

#         score += calculer_recompense(False,num_deleted_lines,previous_max,new_max,False)

#     if training:
#         table.add(current_id,scores)

#     fenetre.fill(NOIR)
#     draw_grid()
#     draw_locked_cells(grid_cells)

#     score_text = font.render(f"score: {score}", True, BLANC)      # Prépare le texte du score
#     fenetre.blit(score_text, (10, 10))
#     draw_current_piece(current_piece_id)                            # Affiche le score à l'écran
#     pygame.display.flip()        # Met à jour l'affichage

#     # Gestion des événements (clics, fermeture de la fenêtre, etc.)
#     for evenement in pygame.event.get():
#         if evenement.type == pygame.QUIT:      
#             if training:            # Si l'utilisateur ferme la fenêtre
#                 table.save()
#             en_cours = False                               # Quitte la boucle


# import pygame
# import random
# import pieces
# import utils
# import copy
# import time

# # ================================
# # INITIALISATION DE BASE
# # ================================

# pygame.init()

# # Fenêtre et grille
# largeur = 800
# hauteur = 600
# taille_bloc = 25
# grid_height = 20
# grid_width = 6
# fenetre = pygame.display.set_mode((largeur, hauteur))
# pygame.display.set_caption("Tetris")

# # Grille logique
# grid = []
# grid_cellsize = 0
# grid_cells = []
# grid_centerX = 0
# grid_centerY = 0

# # Position de la pièce
# piece_pos_x = grid_width // 2 - 2
# piece_pos_y = 0

# piece_types = [1, 2]  # 1 = I, 2 = carré
# current_piece_id = random.choice(piece_types)

# # Couleurs
# NOIR = (0, 0, 0)
# BLANC = (255, 255, 255)
# GRIS = (193, 193, 193)
# BLEU = (0, 150, 255)
# ROUGE = (255, 0, 0)

# # Polices
# font = pygame.font.Font("assets/font/Drawliner.ttf", 30)
# font2 = pygame.font.Font("assets/font/game_over.ttf", 50)

# # Variables de jeu
# score = 0
# game_over = False
# lignes_supprimees = 0
# etat_id = 0
# rotation = 0
# piece_id = 2
# gravity_time = 200
# timerdrop = gravity_time
# player_pos = pygame.Vector2(largeur / 2, hauteur / 4)

# # Hyperparamètres de l'IA
# epsilon = 0.1
# alpha = 0.1
# gamma = 0.9

# # Bordures / états
# dico_bordures = utils.charger_dico_json("bordures.json")
# if dico_bordures:
#     etat_id = max(map(int, dico_bordures.keys())) + 1

# # ================================
# # INITIALISATION DE LA GRILLE
# # ================================

# def init_grid():
#     """
#     Initialise la grille de jeu vide et les coordonnées de placement.
#     """
#     global grid_cellsize, grid_cells, grid_centerX, grid_centerY
#     h = hauteur / grid_height
#     grid_cellsize = h
#     grid_centerX = (largeur / 2) - (h * grid_width) / 2
#     grid_centerY = 0

#     grid_cells = []
#     for i in range(grid_height):
#         row = []
#         for j in range(grid_width):
#             row.append(0)
#         grid_cells.append(row)

# # ================================
# # AFFICHAGE
# # ================================

# def draw_grid():
#     """
#     Dessine la grille en fil de fer.
#     """
#     h = grid_cellsize
#     w = h
#     for i in range(grid_height):
#         for j in range(grid_width):
#             x = grid_centerX + j * w
#             y = grid_centerY + i * h
#             pygame.draw.rect(fenetre, BLANC, (x, y, w, h), 1)

# def draw_locked_cells(cells):
#     """
#     Affiche les blocs déjà posés dans la grille.
#     """
#     for i in range(grid_height):
#         for j in range(grid_width):
#             if cells[i][j] != 0:
#                 x = grid_centerX + j * grid_cellsize
#                 y = grid_centerY + i * grid_cellsize
#                 couleur = cells[i][j]
#                 pygame.draw.rect(fenetre, couleur, (x, y, grid_cellsize, grid_cellsize))
#                 pygame.draw.rect(fenetre, GRIS, (x, y, grid_cellsize, grid_cellsize), 1)


# def supprimer_lignes(cells):
#     """
#     Supprime les lignes pleines et les remplace par des lignes vides.
#     """
#     lignes_supprimees = 0
#     i = grid_height - 1
#     while i >= 0:
#         if all(cells[i][j] != 0 for j in range(grid_width)):
#             del cells[i]
#             cells.insert(0, [0] * grid_width)
#             lignes_supprimees += 1
#         else:
#             i -= 1
#     return cells,lignes_supprimees

# def get_possibles_grids(grid_cells, piece_id):
#     result_grids = []
#     piece = pieces.tetros[piece_id]["rotations"][0]  # On prend la première rotation pour simplifier

#     # Largeur de la pièce (pour éviter de sortir de la grille)
#     largeur_piece = max(j for i in range(4) for j in range(4) if piece[i][j]) + 1

#     for start_col in range(grid_width - largeur_piece + 1):
#         new_grid = copy.deepcopy(grid_cells)
#         current_y = 0
#         good = False
#         while not good and current_y < grid_height - 4 + 1:
#             collision = False
#             for i in range(4):
#                 for j in range(4):
#                     if piece[i][j]:
#                         grid_y = current_y + i
#                         grid_x = start_col + j
#                         if grid_y >= grid_height or new_grid[grid_y][grid_x] != 0:
#                             collision = True
#             if not collision:
#                 current_y += 1
#             else:
#                 current_y -= 1
#                 good = True

#         # Pose la pièce à la dernière position valide
#         for i in range(4):
#             for j in range(4):
#                 if piece[i][j]:
#                     grid_y = current_y + i
#                     grid_x = start_col + j
#                     if 0 <= grid_y < grid_height and 0 <= grid_x < grid_width:
#                         new_grid[grid_y][grid_x] = pieces.tetros[piece_id]["couleur"]

#         result_grids.append(new_grid)

#     return result_grids

# def calculer_recompense(game_over, lignes_supprimees, ancienne_hauteur, nouvelle_hauteur, has_collision=False):
#     """
#     Détermine une récompense pour l'IA selon l'état du jeu.
#     """
#     recompense = 1
#     if has_collision:
#         recompense -= 100
#     if game_over:
#         recompense -= 50
#     recompense += 20 * lignes_supprimees
#     if nouvelle_hauteur > ancienne_hauteur:
#         recompense -= 5
#     return recompense



# en_cours = True                    # Booléen de contrôle pour savoir si le jeu tourne encore
# clock = pygame.time.Clock()       # Horloge pour réguler les FPS
# init_grid()                       # Initialisation de la grille de jeu


# class Q_Table():
#     def __init__(self):
#         self.data = {}

#     def add(self,current,scores):
#         self.data[str(current)] = scores

#     def get_best(self,current):
#         if str(current) in self.data:
#             return self.data[str(current)].index(max(self.data[str(current)]))
#         return random.randint(0,5)

#     def save(self):
#         utils.sauvegarder_dico_json(self.data, "bordures.json")

#     def load(self):
#         self.data = utils.charger_dico_json("bordures.json")

# table = Q_Table()
# training = True

# if not training:
#     table.load()

# while en_cours:
#     dt = clock.tick(1)           # Limite la boucle à 60 FPS et récupère le temps écoulé depuis le dernier tick


#     if training:
#         results = get_possibles_grids(grid_cells, current_piece_id)
#         game_over = False
#         scores = []

#         for b in results:
#             previous_max = grid_height-next((i for i, sub in enumerate(grid_cells) if any(x != 0 for x in sub)), -1)
#             a,lignes_supprimees = supprimer_lignes(b)
#             new_max = grid_height-next((i for i, sub in enumerate(a) if any(x != 0 for x in sub)), -1)
#             if next((i for i, sub in enumerate(a) if any(x != 0 for x in sub)), 100) > 0:
#                 scores.append(calculer_recompense(False,lignes_supprimees,previous_max,new_max,False))
#             else:
#                 scores.append(-1000)

#         if sum(scores) / len(scores) <= -1000:
#             game_over = True

#         if game_over:
#             en_cours = False

#         new_move = scores.index(max(scores))
#         current_id = int(''.join(str(int(bool(x))) for sub in grid_cells for x in sub), 2)
#         grid_cells = results[new_move]
#         grid_cells,num_deleted_lines = supprimer_lignes(grid_cells)
#         new_id = int(''.join(str(int(bool(x))) for sub in grid_cells for x in sub), 2)

#         score += max(scores)
#     else:
#         previous_max = grid_height-next((i for i, sub in enumerate(grid_cells) if any(x != 0 for x in sub)), -1)
#         results = get_possibles_grids(grid_cells, current_piece_id)
#         current_id = int(''.join(str(int(bool(x))) for sub in grid_cells for x in sub), 2)
#         print(current_id)
#         new_move = table.get_best(current_id)
#         grid_cells = results[new_move]
#         grid_cells,num_deleted_lines = supprimer_lignes(grid_cells)
#         new_max = grid_height-next((i for i, sub in enumerate(grid_cells) if any(x != 0 for x in sub)), -1)
#         new_id = int(''.join(str(int(bool(x))) for sub in grid_cells for x in sub), 2)
#         current_piece_id = random.choice(piece_types)

#         score += calculer_recompense(False,num_deleted_lines,previous_max,new_max,False)

#     if training:
#         table.add(current_id,scores)

#     fenetre.fill(NOIR)
#     draw_grid()
#     draw_locked_cells(grid_cells)

#     score_text = font.render(f"score: {score}", True, BLANC)      # Prépare le texte du score
#     fenetre.blit(score_text, (10, 10))                            # Affiche le score à l'écran
#     pygame.display.flip()        # Met à jour l'affichage

#     # Gestion des événements (clics, fermeture de la fenêtre, etc.)
#     for evenement in pygame.event.get():
#         if evenement.type == pygame.QUIT:      
#             if training:            # Si l'utilisateur ferme la fenêtre
#                 table.save()
#             en_cours = False                               # Quitte la boucle

import pygame
import utils
import copy
import random
import numpy as np
import données_ia



# ================================
# INITIALISATION DE LA GRILLE
# ================================

def init_grid():
    """
    Initialise la grille de jeu vide et les coordonnées de placement.
    """
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

# ================================
# AFFICHAGE
# ================================

def draw_grid():
    """
    Dessine la grille en fil de fer.
    """
    h = grid_cellsize
    w = h
    for i in range(grid_height):
        for j in range(grid_width):
            x = grid_centerX + j * w
            y = grid_centerY + i * h
            pygame.draw.rect(fenetre, BLANC, (x, y, w, h), 1)

def draw_locked_cells(cells):
    """
    Affiche les blocs déjà posés dans la grille.
    """
    for i in range(grid_height):
        for j in range(grid_width):
            if cells[i][j] != 0:
                x = grid_centerX + j * grid_cellsize
                y = grid_centerY + i * grid_cellsize
                couleur = cells[i][j]
                pygame.draw.rect(fenetre, couleur, (x, y, grid_cellsize, grid_cellsize))
                pygame.draw.rect(fenetre, GRIS, (x, y, grid_cellsize, grid_cellsize), 1)

def softmax(q_values, temperature=1.0):
    q = np.array(q_values)
    q = q - np.max(q)  # Pour la stabilité numérique
    exp_q = np.exp(q / temperature)
    return exp_q / np.sum(exp_q)

def supprimer_lignes(cells):
    """
    Supprime les lignes pleines et les remplace par des lignes vides.
    """
    lignes_supprimees = 0
    i = grid_height - 1
    while i >= 0:
        if all(cells[i][j] != 0 for j in range(grid_width)):
            del cells[i]
            cells.insert(0, [0] * grid_width)
            lignes_supprimees += 1
        else:
            i -= 1
    return cells,lignes_supprimees

def get_possibles_grids(grid_cells):

    result_grids = []

    for start_collumn in range(grid_width-1):
        new_grid = copy.deepcopy(grid_cells)
        current_y = 0
        good = False
        while (not good) and current_y < grid_height-2:

            top_left = new_grid[current_y][start_collumn]
            top_right = new_grid[current_y][start_collumn+1]
            bottom_left = new_grid[current_y+1][start_collumn]
            bottom_right = new_grid[current_y+1][start_collumn+1]

            if top_left == top_right == bottom_left == bottom_right == 0: #Every slot free
                current_y += 1
            else:
                current_y-=1
                good = True

        new_grid[current_y][start_collumn] = ROUGE
        new_grid[current_y][start_collumn+1] = ROUGE
        new_grid[current_y+1][start_collumn] = ROUGE
        new_grid[current_y+1][start_collumn+1] = ROUGE

        result_grids.append(new_grid)

    return result_grids

def calculer_recompense(game_over, lignes_supprimees, ancienne_hauteur, nouvelle_hauteur, has_collision=False):
    """
    Détermine une récompense pour l'IA selon l'état du jeu.
    """
    recompense = 1 
    if has_collision:
        recompense -= 100
    if game_over:
        recompense -= 50
    recompense += 20 * lignes_supprimees
    if nouvelle_hauteur > ancienne_hauteur:
        recompense -= 5
    return recompense



en_cours = True                    # Booléen de contrôle pour savoir si le jeu tourne encore
clock = pygame.time.Clock()       # Horloge pour réguler les FPS
init_grid()                       # Initialisation de la grille de jeu


class Q_Table():
    def __init__(self):
        self.data = {}

    def add(self,current,Q):
        self.data[str(current)] = Q
        print(f"Ajout de l'état {current} avec Q-values: {Q}")

    def get_best(self,current):
        if str(current) in self.data:
            return self.data[str(current)].index(max(self.data[str(current)]))
        return random.randint(0,5)

    def save(self):
        print("Sauvegarde de la Q-table...")
        utils.sauvegarder_dico_json(self.data, "bordures.json")

    def load(self):
        self.data = utils.charger_dico_json("bordures.json")

table = Q_Table()
training = True
repeat = True

if not training:
    table.load()

while repeat:
    init_grid()
    score = 0
    game_over = False
    grid_cells = [[0 for _ in range(grid_width)] for _ in range(grid_height)]
    en_cours = True

    while en_cours:
        dt = clock.tick(1)           # Limite la boucle à 60 FPS et récupère le temps écoulé depuis le dernier tick


        if training:
            results = get_possibles_grids(grid_cells)
            game_over = False
            scores = []

            for action, b in enumerate(results):
                previous_max = grid_height-next((i for i, sub in enumerate(grid_cells) if any(x != 0 for x in sub)), -1)
                a,lignes_supprimees = supprimer_lignes(b)
                new_max = grid_height-next((i for i, sub in enumerate(a) if any(x != 0 for x in sub)), -1)

                if next((i for i, sub in enumerate(a) if any(x != 0 for x in sub)), 100) > 0:
                    scores.append(calculer_recompense(False,lignes_supprimees,previous_max,new_max,False))
                    reward = calculer_recompense(False, lignes_supprimees, previous_max, new_max, False)

                else:
                    reward = -1000
                    scores.append(-1000)
            
                # --- Mise à jour Q-learning pour chaque test ---
                current_id = int(''.join(str(int(bool(x))) for sub in grid_cells for x in sub), 2)
                Q = table.data.get(str(current_id), [0]*len(results))
                next_Q = max(Q)
                Q[action] = Q[action] + alpha * (reward + gamma * next_Q - Q[action])
                table.data[str(current_id)] = Q
                print (f"Action: {action}, Q-value: {Q[action]}")

            


            


            Q = table.data.get(str(current_id), [0]*len(results))
            probas = softmax(Q, temperature=1.0)
            new_move = np.random.choice(len(results), p=probas)
            grid_cells = results[new_move]
            grid_cells,num_deleted_lines = supprimer_lignes(grid_cells)
            new_id = int(''.join(str(int(bool(x))) for sub in grid_cells for x in sub), 2)

            score += max(scores)

            if sum(scores) / len(scores) <= -1000:
                game_over = True

            if any(cell != 0 for cell in grid_cells[0]):
                game_over = True

            if game_over:
                table.save()
                en_cours = False
                break

        else:

            previous_max = grid_height-next((i for i, sub in enumerate(grid_cells) if any(x != 0 for x in sub)), -1)
            results = get_possibles_grids(grid_cells)
            current_id = int(''.join(str(int(bool(x))) for sub in grid_cells for x in sub), 2)
            print(current_id)
            print (Q := table.data.get(str(current_id), [0]*len(results)))
            new_move = table.get_best(current_id)
            grid_cells = results[new_move]
            grid_cells,num_deleted_lines = supprimer_lignes(grid_cells)
            new_max = grid_height-next((i for i, sub in enumerate(grid_cells) if any(x != 0 for x in sub)), -1)
            new_id = int(''.join(str(int(bool(x))) for sub in grid_cells for x in sub), 2)

            score += calculer_recompense(False,num_deleted_lines,previous_max,new_max,False)
            
            if any(cell != 0 for cell in grid_cells[0]):
                game_over = True

            if game_over:
                en_cours = False


        if training:
            table.add(current_id, Q)

        fenetre.fill(NOIR)
        draw_grid()
        draw_locked_cells(grid_cells)

        score_text = font.render(f"score: {score}", True, BLANC)      # Prépare le texte du score
        fenetre.blit(score_text, (10, 10))                            # Affiche le score à l'écran
        pygame.display.flip()                                         # Met à jour l'affichage

        # Gestion des événements (clics, fermeture de la fenêtre, etc.)
    for evenement in pygame.event.get():
        if evenement.type == pygame.QUIT:      
            if training:            # Si l'utilisateur ferme la fenêtre
                table.save()
            en_cours = False
            repeat = False
            break # Quitte la boucle