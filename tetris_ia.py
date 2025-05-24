import pygame
import random
import pieces
import utils
import copy


pygame.init()




dico_bordures = utils.charger_dico_json("bordures.json")
# Trouver le prochain etat_id disponible
if dico_bordures:
    etat_id = max(map(int, dico_bordures.keys())) + 1
else:
    etat_id = 0
largeur = 800
hauteur = 600
taille_bloc = 25
score = 0
font = pygame.font.Font("assets/font/Drawliner.ttf", 30)
font2 = pygame.font.Font("assets/font/game_over.ttf", 50)
epsilon = 0.1
alpha=0.1
gamma=0.9
grid = []
grid_height = 20
grid_width = 6
grid_cellsize = 0
grid_cells = []
grid_centerX = 0
grid_centerY = 0
piece_pos_x = grid_width // 2 - 2
piece_pos_y = 0
gravity_time = 200
timerdrop = gravity_time
player_pos = pygame.Vector2(largeur / 2, hauteur / 4)
fenetre = pygame.display.set_mode((largeur, hauteur))
pygame.display.set_caption("Tetris")
game_over = False
lignes_supprimees = 0

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

def draw_locked_cells():
    for i in range(grid_height):
        for j in range(grid_width):
            if grid_cells[i][j] != 0:
                x = grid_centerX + j * grid_cellsize
                y = grid_centerY + i * grid_cellsize
                couleur = grid_cells[i][j]
                pygame.draw.rect(fenetre, couleur, (x, y, grid_cellsize, grid_cellsize))
                pygame.draw.rect(fenetre, GRIS, (x, y, grid_cellsize, grid_cellsize), 1)

# Couleurs
NOIR = (0, 0, 0)
BLANC = (255, 255, 255)
GRIS = (193, 193, 193)
BLEU = (0, 150, 255)
ROUGE = (255, 0, 0)

piece_id = 2
rotation = 0



def nouvelle_piece():
    global piece_id, rotation, piece_pos_x
    piece_id = 2
    rotation = 0
    piece_pos_x = len(grid_cells[0]) // 2 - 2  # Centrer la nouvelle pièce
    if hasattr(next_drop, "colonne_fixee"):
        del next_drop.colonne_fixee



def calculer_recompense(game_over, lignes_supprimees, ancienne_hauteur, nouvelle_hauteur, has_collision=False):
    """
    Calcule la récompense pour l'IA :
    - -50 si game over
    - +20 par ligne supprimée
    - -5 si la hauteur maximale augmente
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


def Q_table():
    """
    Choisit la colonne selon la Q-table de l'état courant (bordure).
    Avec epsilon, fait parfois un choix aléatoire (exploration).
    """
    global dico_bordures, grid_width, piece_pos_x, etat_id

    bordure = matrice_bordure_superieure()
    if not utils.matrice_deja_presente(dico_bordures, bordure):
        utils.enregistrer_bordure(dico_bordures, etat_id, bordure, grid_width)
        utils.sauvegarder_dico_json(dico_bordures, "bordures.json")
    # Trouve le bon etat_id pour la bordure courante
    for k, v in dico_bordures.items():
        if v["bordure"] == bordure:
            etat_id = int(k)
            break

    Q = dico_bordures[str(etat_id)]["Q_table"]

    # Politique epsilon-greedy
    if random.random() < epsilon:
        # Exploration : choix uniforme
        action = random.randint(0, len(Q) - 1)
    else:
        # Exploitation : tirage pondéré selon les Q (softmax ou normalisation)
        Q_min = min(Q)
        Q_shifted = [q - Q_min + 1e-6 for q in Q]  # Décale pour éviter les valeurs négatives
        total = sum(Q_shifted)
        if total == 0:
            # Si toutes les Q sont égales, choix uniforme
            proba = [1/len(Q)] * len(Q)
        else:
            proba = [q/total for q in Q_shifted]
        action = random.choices(range(len(Q)), weights=proba, k=1)[0]

    piece_pos_x = action
    return action  # Utile pour la mise à jour de la Q-table


def update_Q_table(etat_id, action, reward, next_etat_id, alpha, gamma):
    """
    Met à jour la Q-table pour l'état et l'action donnés.
    """
    Q = dico_bordures[str(etat_id)]["Q_table"]
    if next_etat_id is not None and "Q_table" in dico_bordures[str(next_etat_id)]:
        next_Q = max(dico_bordures[str(next_etat_id)]["Q_table"])
    else:
        next_Q = 0
    Q[action] = Q[action] + alpha * (reward + gamma * next_Q - Q[action])
    print (Q[action])




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


def matrice_bordure_superieure():
    # Crée une matrice de zéros
    bordure = [[0 for _ in range(grid_width)] for _ in range(grid_height)]
    for col in range(grid_width):
        for row in range(grid_height):
            if grid_cells[row][col] != 0:
                bordure[row][col] = 1
                break  # On ne garde que le premier "1" de la colonne
    return bordure

def piece_collides(piece, x, y, grid):
    for i in range(4):
        for j in range(4):
            if piece[i][j]:
                grid_x = x + j
                grid_y = y + i
                if (
                    grid_x < 0 or grid_x >= grid_width or
                    grid_y >= grid_height or
                    (grid_y >= 0 and grid[grid_y][grid_x] != 0)
                ):
                    return True
    return False

def trouver_hauteur_finale(piece, x, grid):
    for y in range(grid_height):
        if piece_collides(piece, x, y, grid):
            return y - 1  # Last safe position before collision
    return grid_height - len(piece)  # If no collision, go to the bottom

def poser_piece(piece, x, y, grille, couleur):
    for i in range(4):
        for j in range(4):
            if piece[i][j]:
                grid_y = y + i
                grid_x = x + j
                if 0 <= grid_y < grid_height and 0 <= grid_x < grid_width:
                    grille[grid_y][grid_x] = couleur

def next_drop(dt):
    global timerdrop, piece_pos_y, piece_pos_x, score, etat_id, en_cours

    piece = pieces.tetros[piece_id]["rotations"][rotation]
    can_move = True
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

    if can_move:
        piece_pos_y += 1
    else:
        poser_piece(piece, piece_pos_x, piece_pos_y, grid_cells, pieces.tetros[piece_id]["couleur"])
        lignes_supprimees = supprimer_lignes()
        score += lignes_supprimees * 100

        nouvelle_piece()
        piece_pos_y = 0

    
        
def entrainer_IA():
    global piece_pos_x
    for _ in range(10): 
        action = Q_table()  # Choisit la colonne selon la Q-table

        # Simule la pose de la pièce à la colonne 'action' sur une copie de la grille
        grille_temp = copy.deepcopy(grid_cells)
        ancienne_hauteur = max((row for row in range(grid_height) if any(grille_temp[row][col] != 0 for col in range(grid_width))), default=-1) + 1
        piece = pieces.tetros[piece_id]["rotations"][rotation]

        # Vérification collision latérale AVANT de simuler la pose
        if piece_collides(piece, action, 0, grille_temp):
            # Collision latérale immédiate : très mauvaise récompense et on passe au test suivant
            reward = calculer_recompense(
                game_over=False,
                lignes_supprimees=0,
                ancienne_hauteur=ancienne_hauteur,
                nouvelle_hauteur=ancienne_hauteur,  # pas de changement de hauteur
                has_collision=True
            )
            update_Q_table(etat_id, action, reward, etat_id, alpha, gamma)
            continue  # Passe au test suivant

        # Simulation de la pose (descente jusqu'à collision)
        y = 0
        while not piece_collides(piece, action, y, grille_temp):
            y += 1
        y -= 1  # Dernière position valide

        # Pose la pièce simulée
        poser_piece(piece, action, y, grille_temp, pieces.tetros[piece_id]["couleur"])

        # Calcul des autres variables
        lignes_supprimees = 0
        i = grid_height - 1
        while i >= 0:
            if all(grille_temp[i][j] != 0 for j in range(grid_width)):
                del grille_temp[i]
                grille_temp.insert(0, [0] * grid_width)
                lignes_supprimees += 1
            else:
                i -= 1
        nouvelle_hauteur = max((row for row in range(grid_height) if any(grille_temp[row][col] != 0 for col in range(grid_width))), default=-1) + 1
        game_over = any(grille_temp[0][col] != 0 for col in range(grid_width))
        reward = calculer_recompense(game_over, lignes_supprimees, ancienne_hauteur, nouvelle_hauteur, has_collision=False)
        update_Q_table(etat_id, action, reward, etat_id, alpha, gamma)

    piece = pieces.tetros[piece_id]["rotations"][rotation]
    hauteur_finale = trouver_hauteur_finale(piece, piece_pos_x, grid_cells)
    if piece_pos_y + 1 >= hauteur_finale and not hasattr(next_drop, "colonne_fixee"):
        # Pose la pièce selon la Q-table (choix définitif)
        piece_pos_x = Q_table()
        next_drop.colonne_fixee = True
        piece = pieces.tetros[piece_id]["rotations"][rotation]
        for i in range(4):
            for j in range(4):
                if piece[i][j]:
                    grid_y = piece_pos_y + i
                    grid_x = piece_pos_x + j
                    if 0 <= grid_y < grid_height and 0 <= grid_x < grid_width:
                        grid_cells[grid_y][grid_x] = pieces.tetros[piece_id]["couleur"]

               
                    

def nouv_tetros():
    global piece_pos_x, piece_pos_y, grid_cells

    piece = pieces.tetros[piece_id]["rotations"][rotation]
    
    
    for i in range(4):
        for j in range(4):
            if piece[i][j]:  
                grid_y = piece_pos_y + i
                grid_x = piece_pos_x + j

               
                if grid_y >= grid_height or grid_x < 0 or grid_x >= grid_width or (grid_y >= 0 and grid_cells[grid_y][grid_x] != 0):

                   
                    for k in range(4):
                        for l in range(4):
                            if piece[k][l]: 
                                grid_y = piece_pos_y + k
                                grid_x = piece_pos_x + l
                                if 0 <= grid_y < grid_height and 0 <= grid_x < grid_width:
                                    grid_cells[grid_y][grid_x] = pieces.tetros[piece_id]["couleur"]
                                    cell_state = 1
                                    

                    # Générer une nouvelle pièce
                    piece_pos_x = grid_width // 2 - 2
                    piece_pos_y = 0
                    nouvelle_piece()
                    return cell_state

# comptage des points + suppression des lignes
def supprimer_lignes():
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




en_cours = True
clock = pygame.time.Clock()
init_grid()
origine_x = grid_centerX
origine_y = grid_centerY
descente_timer = 0
descente_intervalle = 500



while en_cours:
     
    dt = clock.tick(60)
    descente_timer += dt
    # Affichage
    fenetre.fill(NOIR)
    draw_grid()
    draw_locked_cells()
    dessiner_piece(piece_id, rotation, piece_pos_x, piece_pos_y)
    score_text = font.render(f"score: {score}", True, BLANC)
    fenetre.blit(score_text, (10, 10))
    pygame.display.flip()


    # 2. Boucle d'entraînement Q-table toutes les 100 ms
    bordure = matrice_bordure_superieure()
    if not utils.matrice_deja_presente(dico_bordures, bordure):
        utils.enregistrer_bordure(dico_bordures, etat_id, bordure, grid_width)
        utils.sauvegarder_dico_json(dico_bordures, "bordures.json")
    for k, v in dico_bordures.items():
        if v["bordure"] == bordure:
            etat_id = int(k)
            break
        Q = dico_bordures[str(etat_id)]["Q_table"]

    for evenement in pygame.event.get():
            if evenement.type == pygame.QUIT:
                utils.sauvegarder_dico_json(dico_bordures, "bordures.json")
                en_cours = False
    
    entrainer_IA()
    if descente_timer >= descente_intervalle:
        next_drop(dt)
        descente_timer = 0
    




attente = True
while attente:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            attente = False
pygame.quit()

print("Dictionnaire des bordures enregistrées :")
for k, v in dico_bordures.items():
    print(f"État {k}:")
    for row in v:
        print(row)
    print("-" * 30)








