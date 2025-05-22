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

# Paramètres de la fenêtre
largeur = 800
hauteur = 600
taille_bloc = 25
score = 0
font = pygame.font.Font("assets/font/Drawliner.ttf",30)
font2 = pygame.font.Font("assets/font/game_over.ttf", 50)
grid = []
grid_height = 20
grid_width = 6
grid_cellsize = 0
grid_cells = []
grid_centerX = 0
grid_centerY = 0
piece_pos_x = grid_width // 2 - 2
piece_pos_y = 0
# gravity_time = 200
# timerdrop = gravity_time
player_pos = pygame.Vector2(largeur / 2, hauteur / 4)
fenetre = pygame.display.set_mode((largeur, hauteur))
pygame.display.set_caption("Tetris")
# Couleurs
NOIR = (0, 0, 0)
BLANC = (255, 255, 255)
GRIS = (193, 193, 193)
BLEU = (0, 150, 255)

# Paramètres de l'IA
epsilon = 0.1
alpha=0.1
gamma=0.9




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

print(grid_cells)



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



piece_id = 2
rotation = 0



def reset_game():
    global grid_cells, score, piece_pos_x, piece_pos_y, piece_id, rotation
    init_grid()
    score = 0
    piece_pos_x = random.randint(0, grid_width - 2)
    piece_pos_y = 0
    piece_id = 2
    rotation = 0
    action_to_do()


print("Après reset_game, grille :")
for row in grid_cells:
    print(row)
print("piece_pos_x:", piece_pos_x, "piece_pos_y:", piece_pos_y)


def nouvelle_piece():
    global piece_id, rotation
    piece_id = 2
    rotation = 0


print("Première pièce posée :", piece_id, "rotation :", rotation, "pos_x :", piece_pos_x, "pos_y :", piece_pos_y)
for row in grid_cells:
    print(row)


def action_to_do():
    """
    Choisit une colonne au hasard pour placer la pièce courante, en tenant compte de sa largeur réelle et de son décalage.
    """
    global piece_pos_x, piece_id, rotation
    piece = pieces.tetros[piece_id]["rotations"][rotation]

    # Trouver les colonnes occupées par la pièce
    colonnes_occupees = [j for i in range(4) for j in range(4) if piece[i][j]]
    if not colonnes_occupees:
        piece_pos_x = 0
        return

    min_col = min(colonnes_occupees)
    max_col = max(colonnes_occupees)
    largeur_piece = max_col - min_col + 1

    # Pour permettre à la pièce de toucher le bord gauche ET droit
    min_x = 0
    max_x = grid_width - largeur_piece
    piece_pos_x = random.randint(min_x, max_x)



def calculer_recompense(game_over, lignes_supprimees, ancienne_hauteur, nouvelle_hauteur):
    """
    Calcule la récompense pour l'IA :
    - -50 si game over
    - +20 par ligne supprimée
    - -5 si la hauteur maximale augmente
    """
    recompense = 0
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
    global dico_bordures, grid_width, piece_pos_x

    Q = dico_bordures[str(etat_id)]["Q_table"]
    # Politique epsilon-greedy
    if random.random() < epsilon:
        action = random.randint(0, grid_width - 2)
    else:
        maxQ = max(Q)
        actions = [i for i, q in enumerate(Q) if q == maxQ]
        action = random.choice(actions)
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



def entrainer_sur_bordure(etat_id, bordure, max_iterations=1000):
    """
    Fait tourner la Q-table sur la même bordure jusqu'à ce qu'une action soit préférée (Q > 0.80).
    Puis pose la pièce à l'endroit choisi et met à jour la grille.
    """
    global dico_bordures, grid_width, alpha, gamma, epsilon, piece_pos_x, piece_pos_y, piece_id, rotation, grid_cells, score

    Q = dico_bordures[str(etat_id)]["Q_table"]
    iteration = 0
    while max(Q) < 0.80 and iteration < max_iterations:
        # Choix d'action selon epsilon-greedy
        if random.random() < epsilon:
            action = random.randint(0, grid_width - 2)
        else:
            maxQ = max(Q)
            actions = [i for i, q in enumerate(Q) if q == maxQ]
            action = random.choice(actions)

        # Ici, tu dois simuler la récompense pour cet état/action
        # Simule la pose de la pièce à la colonne 'action' sur une copie de la grille
        grille_temp = copy.deepcopy(grid_cells)

        # Hauteur avant pose
        ancienne_hauteur = max((row for row in range(grid_height) if any(grille_temp[row][col] != 0 for col in range(grid_width))), default=-1) + 1

        # Pose la pièce sur la grille temporaire
        piece = pieces.tetros[piece_id]["rotations"][rotation]
        for i in range(4):
            for j in range(4):
                if piece[i][j]:
                    grid_y = i
                    grid_x = action + j
                    if 0 <= grid_y < grid_height and 0 <= grid_x < grid_width:
                        grille_temp[grid_y][grid_x] = pieces.tetros[piece_id]["couleur"]

        # Supprime les lignes pleines sur la grille temporaire
        lignes_supprimees = 0
        i = grid_height - 1
        while i >= 0:
            if all(grille_temp[i][j] != 0 for j in range(grid_width)):
                del grille_temp[i]
                grille_temp.insert(0, [0] * grid_width)
                lignes_supprimees += 1
            else:
                i -= 1

        # Nouvelle hauteur après pose
        nouvelle_hauteur = max((row for row in range(grid_height) if any(grille_temp[row][col] != 0 for col in range(grid_width))), default=-1) + 1
        # Game over si la pièce touche le haut
        game_over = any(grille_temp[0][col] != 0 for col in range(grid_width))

        reward = calculer_recompense(game_over, lignes_supprimees, ancienne_hauteur, nouvelle_hauteur)
        next_etat_id = etat_id  # Ici, tu peux simuler ou garder le même état
        update_Q_table(etat_id, action, reward, next_etat_id, alpha, gamma)
        iteration += 1
        

    # Quand une action est préférée, on pose la pièce à l'endroit optimal
    meilleure_action = Q.index(max(Q))
    piece_pos_x = meilleure_action
    piece_pos_y = 0  # On pose la pièce en haut

    # Pose la pièce dans la grille réelle
    piece = pieces.tetros[piece_id]["rotations"][rotation]
    for i in range(4):
        for j in range(4):
            if piece[i][j]:
                grid_y = piece_pos_y + i
                grid_x = piece_pos_x + j
                if 0 <= grid_y < grid_height and 0 <= grid_x < grid_width:
                    grid_cells[grid_y][grid_x] = pieces.tetros[piece_id]["couleur"]

    # Supprime les lignes pleines et mets à jour le score
    lignes_supprimees = supprimer_lignes()
    score += lignes_supprimees * 100

    # Calcule la nouvelle bordure
    nouvelle_bordure = matrice_bordure_superieure()

    # Enregistre la Q-table et la nouvelle bordure immédiatement
    utils.enregistrer_bordure(dico_bordures, etat_id, nouvelle_bordure, grid_width)
    utils.sauvegarder_dico_json(dico_bordures, "bordures.json")

    # Prépare la prochaine pièce
    nouvelle_piece()
    action_to_do()
    piece_pos_y = 0

    return nouvelle_bordure



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



def next_drop(dt):
    global piece_pos_y, piece_pos_x, score, etat_id, en_cours

    timerdrop -= dt
    if timerdrop <= 0:
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
            # Fixer la pièce dans la grille
            for i in range(4):
                for j in range(4):
                    if piece[i][j]:
                        grid_y = piece_pos_y + i
                        grid_x = piece_pos_x + j
                        if grid_y >= 0:
                            grid_cells[grid_y][grid_x] = pieces.tetros[piece_id]["couleur"]
                    
            lignes_supprimees = supprimer_lignes()
            score += lignes_supprimees * 100

            # Affichage de la bordure supérieure à chaque pose de bloc
            bordure = matrice_bordure_superieure()
            for row in bordure:
                print(row)
            print("-" * 30)
            bordure = matrice_bordure_superieure()
            if not utils.matrice_deja_presente(dico_bordures, bordure):
                utils.enregistrer_bordure(dico_bordures, etat_id, bordure, grid_width)
                utils.sauvegarder_dico_json(dico_bordures, "bordures.json")  # <-- Sauvegarde immédiate
                etat_id += 1  


            # Nouvelle pièce
            nouvelle_piece()
            action_to_do()
            piece_pos_y = -1

             # Vérifie si la nouvelle pièce peut être placée
            piece = pieces.tetros[piece_id]["rotations"][rotation]
            for i in range(4):
                for j in range(4):
                    if piece[i][j]:
                        grid_y = piece_pos_y + i
                        grid_x = piece_pos_x + j
                        if grid_y >= 0 and grid_y < grid_height and grid_cells[grid_y][grid_x] != 0:
                            en_cours = False  # Fin du jeu

        # timerdrop = gravity_time



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
action_to_do()
# origine_x = grid_centerX
# origine_y = grid_centerY
apprentissage_en_cours = True



while apprentissage_en_cours:  # Boucle infinie pour l'apprentissage
    en_cours = True
    reset_game()
    while en_cours:
        for evenement in pygame.event.get():
            if evenement.type == pygame.QUIT:
                en_cours = False
                apprentissage_en_cours = False  # Quitte aussi la boucle principale
            elif evenement.type == pygame.KEYDOWN:
                if evenement.key == pygame.K_ESCAPE:
                    en_cours = False
                    apprentissage_en_cours = False

        fenetre.fill(NOIR)
        draw_grid()

        draw_locked_cells()
        dessiner_piece(piece_id, rotation, piece_pos_x, piece_pos_y)

        # dt = clock.tick(30) 
        # next_drop(dt)
        score_text = font.render(f"score: {score}", True, BLANC)
        fenetre.blit(score_text, (10, 10))
        pygame.display.flip()

        # 1. Calcul de la bordure actuelle
        bordure = matrice_bordure_superieure()

        # 2. Recherche ou création de l'état pour cette bordure
        etat_id = None
        for k, v in dico_bordures.items():
            if v["bordure"] == bordure:
                etat_id = int(k)
                break
        if etat_id is None:
            etat_id = max(map(int, dico_bordures.keys()), default=-1) + 1
            utils.enregistrer_bordure(dico_bordures, etat_id, bordure, grid_width)
            utils.sauvegarder_dico_json(dico_bordures, "bordures.json")

        # 3. Entraînement et pose de la pièce (ceci crée aussi la nouvelle pièce)
        nouvelle_bordure = entrainer_sur_bordure(etat_id, bordure)
        print("Après reset_game, grille :")
        for row in grid_cells:
            print(row)
        print("piece_pos_x:", piece_pos_x, "piece_pos_y:", piece_pos_y)

        # 4. Vérifie si la nouvelle pièce peut être placée (game over)
        piece = pieces.tetros[piece_id]["rotations"][rotation]
        for i in range(4):
            for j in range(4):
                if piece[i][j]:
                    grid_y = piece_pos_y + i
                    grid_x = piece_pos_x + j
                    if grid_y < 0:
                        continue
                    if grid_y >= grid_height or grid_cells[grid_y][grid_x] != 0:
                        en_cours = False
                        apprentissage_en_cours = False
                        break
            if not en_cours:
                break



text_gameover = font2.render("Game over", True, BLANC)
text_rect = text_gameover.get_rect(center=player_pos)
fenetre.blit(text_gameover, text_rect)
pygame.display.flip()

attente = True
while attente:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            attente = False



pygame.quit()


# print("Dictionnaire des bordures enregistrées :")
# for k, v in dico_bordures.items():
#     print(f"État {k}:")
#     for row in v:
#         print(row)
#     print("-" * 30)





