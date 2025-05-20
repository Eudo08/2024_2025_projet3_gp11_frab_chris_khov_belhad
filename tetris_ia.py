import pygame
import random
import pieces
import utils


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
font = pygame.font.Font("assets/font/Drawliner.ttf",30)
# font = pygame.font.SysFont("Drawliner", 30)
grid = []
grid_height = 20
grid_width = 6
grid_cellsize = 0
grid_cells = []
grid_centerX = 0
grid_centerY = 0
piece_pos_x = 0
piece_pos_y = -1
gravity_time = 200
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

piece_id = 2
rotation = 0

def nouvelle_piece():
    global piece_id, rotation, piece_pos_x, en_cours
    piece_id = 2
    rotation = 0
    col = action_to_do()
    if col is None:
        en_cours = False  # Plus de placement possible, fin du jeu
    else:
        piece_pos_x = col

def state_of_object ():
    pass

def matrice_envrionnement ():
    pass

def action_to_do():
    largeur_piece = 2
    colonnes_valides = []
    for col in range(grid_width - largeur_piece + 1):
        collision = False
        for i in range(largeur_piece):
            for j in range(largeur_piece):
                grid_x = col + j
                grid_y = piece_pos_y + i  # piece_pos_y vaut -1 au début
                # On vérifie que grid_x est dans la grille
                if not (0 <= grid_x < grid_width):
                    collision = True
                # On vérifie la collision uniquement si grid_y >= 0 (dans la grille)
                elif grid_y >= 0 and grid_cells[grid_y][grid_x] != 0:
                    collision = True
        if not collision:
            colonnes_valides.append(col)
    if colonnes_valides:
        return random.choice(colonnes_valides)
    else:
        # Si aucune colonne n'est valide, retourne None pour signaler la fin du jeu
        return None

def Q_table():
    pass


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
    global timerdrop, piece_pos_y, piece_pos_x, score, etat_id, en_cours

    timerdrop -= dt
    if timerdrop <= 0:
        piece = pieces.tetros[piece_id]["rotations"][rotation]
        can_move = True

        for i in range(4):
            for j in range(4):
                if piece[i][j]:
                    new_y = piece_pos_y + i + 1
                    new_x = piece_pos_x + j
                    # Correction : on vérifie que new_x est dans la grille avant d'accéder à grid_cells
                    if new_y >= grid_height or not (0 <= new_x < grid_width) or (new_y >= 0 and grid_cells[new_y][new_x] != 0):
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
                        # Correction : on vérifie que grid_y et grid_x sont dans la grille avant d'écrire
                        if 0 <= grid_y < grid_height and 0 <= grid_x < grid_width:
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
                utils.enregistrer_bordure(dico_bordures, etat_id, bordure)
                etat_id += 1 


            # Nouvelle pièce
            nouvelle_piece()
            # piece_pos_x = grid_width // 2 - 2
            piece_pos_y = -1

             # Vérifie si la nouvelle pièce peut être placée
            piece = pieces.tetros[piece_id]["rotations"][rotation]
            for i in range(4):
                for j in range(4):
                    if piece[i][j]:
                        grid_y = piece_pos_y + i
                        grid_x = piece_pos_x + j
                        # Correction ici : vérifie que grid_y est dans la grille avant d'accéder à grid_cells
                        if (
                            0 <= grid_y < grid_height and
                            0 <= grid_x < grid_width and
                            grid_cells[grid_y][grid_x] != 0
                        ):
                            en_cours = False  # Fin du jeu

        timerdrop = gravity_time



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
    
    fenetre.fill(NOIR)
    draw_grid()
    draw_locked_cells()
    dessiner_piece(piece_id, rotation, piece_pos_x, piece_pos_y)

    dt = clock.tick(30) 
    next_drop(dt)
    score_text = font.render(f"score: {score}", True, BLANC)
    fenetre.blit(score_text, (10, 10))
    pygame.display.flip()

        # elif evenement.type == pygame.KEYDOWN:
        #     if evenement.key == pygame.K_SPACE:
        #         new_rotation = (rotation + 1) % len(pieces.tetros[piece_id]["rotations"])
        #         new_piece = pieces.tetros[piece_id]["rotations"][new_rotation]

        #         valide = True
        #         for i in range(4):
        #             for j in range(4):
        #                 if new_piece[i][j]:
        #                     x = piece_pos_x + j
        #                     y = piece_pos_y + i

        #                     if x < 0 or x >= grid_width or y >= grid_height:
        #                         valide = False
        #                         break  
        #                     elif y >= 0 and grid_cells[y][x] != 0:
        #                         valide = False
        #                         break 
        #             if not valide:
        #                 break  
        #         if valide:
        #             rotation = new_rotation

        #     elif evenement.key == pygame.K_ESCAPE:
        #         en_cours = False
        #     elif evenement.key == pygame.K_LEFT:
        #         piece_pos_x -= 1
        #         piece = pieces.tetros[piece_id]["rotations"][rotation]
        #         for i in range(4):
        #             for j in range(4):
        #                 if piece[i][j]:
        #                     new_x = piece_pos_x + j
        #                     new_y = piece_pos_y + i
        #                     if new_x < 0 or (new_y >= 0 and grid_cells[new_y][new_x] != 0):
        #                         piece_pos_x += 1  
        #                         break
        #     elif evenement.key == pygame.K_RIGHT:
        #         piece_pos_x += 1
        #         piece = pieces.tetros[piece_id]["rotations"][rotation]
        #         for i in range(4):
        #             for j in range(4):
        #                 if piece[i][j]:
        #                     new_x = piece_pos_x + j
        #                     new_y = piece_pos_y + i
        #                     if new_x >= grid_width or (new_y >= 0 and grid_cells[new_y][new_x] != 0):
        #                         piece_pos_x -= 1  # annule le déplacement
        #                         break
            # elif evenement.key == 
    



    fenetre.fill(NOIR)
    draw_grid()

    draw_locked_cells()
    dessiner_piece(piece_id, rotation, piece_pos_x, piece_pos_y)

    dt = clock.tick(30) 
    next_drop(dt)
    score_text = font.render(f"score: {score}", True, BLANC)
    fenetre.blit(score_text, (10, 10))
    pygame.display.flip()

    # def appliquer_situation1_situation2():
    #     for col in range(grid_width):
    #         for row in range(grid_height - 1):
    #             if [1 if grid_cells[row][col] != 0 else 0, 1 if grid_cells[row+1][col] != 0 else 0] == [1, 1]:
    #                 grid_cells[row+1][col] = 0        
    # for row in grid_cells:
        # appliquer_situation1_situation2(row)
    #     print([1 if cell != 0 else 0 for cell in row])
    # print("-"*30)
    # clock.tick(5)

print("Dictionnaire des bordures enregistrées :")
for k, v in dico_bordures.items():
    print(f"État {k}:")
    for row in v:
        print(row)
    print("-" * 30)

pygame.quit ()

utils.sauvegarder_dico_json(dico_bordures, "bordures.json")
print("Dictionnaire des bordures sauvegardé dans bordures.json")



