import pygame
import utils


# ================================
# INITIALISATION DE BASE
# ================================


# Fenêtre et grille
largeur = 800
hauteur = 600
taille_bloc = 25
grid_height = 20
grid_width = 6
fenetre = pygame.display.set_mode((largeur, hauteur))
pygame.display.set_caption("Tetris")

# Grille logique
grid = []
grid_cellsize = 0
grid_cells = []
grid_centerX = 0
grid_centerY = 0

# Position de la pièce
piece_pos_x = grid_width // 2 - 2
piece_pos_y = 0

# Couleurs
NOIR = (0, 0, 0)
BLANC = (255, 255, 255)
GRIS = (193, 193, 193)
BLEU = (0, 150, 255)
ROUGE = (255, 0, 0)

# Polices
font = pygame.font.Font("assets/font/Drawliner.ttf", 30)
font2 = pygame.font.Font("assets/font/game_over.ttf", 50)

# Variables de jeu
score = 0
game_over = False
lignes_supprimees = 0
etat_id = 0
rotation = 0
piece_id = 2
gravity_time = 200
timerdrop = gravity_time
player_pos = pygame.Vector2(largeur / 2, hauteur / 4)

# Hyperparamètres de l'IA
epsilon = 0.1
alpha = 0.2
gamma = 0.99

# Bordures / états
dico_bordures = utils.charger_dico_json("bordures.json")
if dico_bordures:
    etat_id = max(map(int, dico_bordures.keys())) + 1