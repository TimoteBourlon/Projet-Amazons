import random

class algorithmes:

    def __init__(self, n=8):
        # Taille du plateau
        self.__n = n

        # Matrice représentant l'état du plateau
        self.__board = []

        # Joueur courant
        self.__player = 1

        # Variante activée ou non
        self.__variant = False

        # Choix de relancer une partie sauvegardée
        self.__replayGame = False

        # Phase du tour : "Select", "Move", "Shoot"
        self.__phase = "Select"

        # Position du pion actuellement sélectionné
        self.__selected_i = None
        self.__selected_j = None

        # Directions autorisées pour déplacements et tirs
        self.__directions = [(1, 0), (-1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, 1), (1, -1)]

        # Contre le robot ou non
        self.__vsBot = False

    # Getter, Setter
    def getN(self):
        return self.__n

    def setN(self, n):
        self.__n = n

    def getBoard(self):
        return self.__board

    def setBoard(self, board):
        self.__board = board

    def getPlayer(self):
        return self.__player

    def setPlayer(self, player):
        self.__player = int(player)

    def getVariant(self):
        return self.__variant

    def setVariant(self, value):
        self.__variant = value

    def getPhase(self):
        return self.__phase

    def setPhase(self, phase):
        self.__phase = phase

    def getSelectedI(self):
        return self.__selected_i

    def setSelectedI(self, selected_i):
        self.__selected_i = selected_i

    def getSelectedJ(self):
        return self.__selected_j

    def setSelectedJ(self, selected_j):
        self.__selected_j = selected_j

    def getReplayGame(self):
        return self.__replayGame

    def setReplayGame(self, value):
        self.__replayGame = value

    def getVsBot(self):
        return self.__vsBot

    def setVsBot(self, value):
        self.__vsBot = value

    # Configuration du plateau
    def initBoard(self):
        # Choix du fichier suivant la taille du plateau
        if self.__n == 6:
            self.__file = 'boards/six.txt'
        elif self.__n == 7:
            self.__file = 'boards/seven.txt'
        elif self.__n == 8:
            self.__file = 'boards/eight.txt'
        elif self.__n == 9:
            self.__file = 'boards/nine.txt'
        elif self.__n == 10:
            self.__file = 'boards/ten.txt'

        # Gestion du fichier
        myFile = open(self.__file, "r")
        lignes = myFile.readlines()
        myFile.close()

        # Conversion des lignes du plateau en matrice
        l = [line.strip() for line in lignes]
        self.__board = [[int(c) for c in line] for line in l]

    # Sélection du pion
    def selectPawn(self, i, j):
        if self.__board[i][j] != self.__player:
            return False

        for dx, dy in self.__directions:
            x = i + dx
            y = j + dy
            if 0 <= x < self.__n and 0 <= y < self.__n:
                if self.__board[x][y] == 0:
                    return True
        return False

    # Possibilité de déplacements
    def canMove(self, i, j, i_to, j_to):
        if not (0 <= i_to < self.__n and 0 <= j_to < self.__n):
            return False

        # Gestion des règles selon la variante
        if not self.__variant:
            if self.__board[i_to][j_to] != 0:
                return False
        elif self.__variant:
            if self.__board[i_to][j_to] == 3:
                return False

        # Calcul du déplacement en coordonnées
        di = i_to - i
        dj = j_to - j

        # Calcul du pas en ligne
        if di > 0:
            step_i = 1
        elif di < 0:
            step_i = -1
        else:
            step_i = 0

        # Calcul du pas en colonne
        if dj > 0:
            step_j = 1
        elif dj < 0:
            step_j = -1
        else:
            step_j = 0

        # Vérifie que la direction est valide
        if (step_i, step_j) not in self.__directions:
            return False

        # Position courante en avançant d'un pas vers la cible
        current_i = i + step_i
        current_j = j + step_j

        # Parcourt chaque case du chemin jusqu'à la case d'arrivée
        while current_i != i_to or current_j != j_to:
            if self.__board[current_i][current_j] != 0:
                return False
            current_i += step_i
            current_j += step_j
        return True

    # Mouvements Possibles
    def possibleMoves(self, i, j):
        moves = []

        for dx, dy in self.__directions:
            current_i = i + dx
            current_j = j + dy

            # Explore en ligne droite tant que le mouvement est valide
            while 0 <= current_i < self.__n and 0 <= current_j < self.__n and self.canMove(i, j, current_i, current_j):
                moves.append((current_i, current_j))
                current_i += dx
                current_j += dy
        return moves

    # Effectue le déplacement
    def move(self, i, j, i_to, j_to):
        if self.canMove(i, j, i_to, j_to):
            self.__board[i][j] = 0
            self.__board[i_to][j_to] = self.__player

    # Possibilité de tirer une flèche
    def canShootArrows(self, i, j, i_to, j_to):
        if not (0 <= i_to < self.__n and 0 <= j_to < self.__n):
            return False

        if self.__board[i_to][j_to] != 0:
            return False

        di = i_to - i
        dj = j_to - j

        # Calcul du pas en ligne
        if di > 0:
            step_i = 1
        elif di < 0:
            step_i = -1
        else:
            step_i = 0

        # Calcul du pas en colonne
        if dj > 0:
            step_j = 1
        elif dj < 0:
            step_j = -1
        else:
            step_j = 0

        # Vérifie que la direction est valide
        if (step_i, step_j) not in self.__directions:
            return False

        # Calcule la position actuelle
        current_i = i + step_i
        current_j = j + step_j

        # Parcours toutes les cases entre départ et arrivée pour vérifier que le chemin est libre
        while current_i != i_to or current_j != j_to:
            if self.__board[current_i][current_j] != 0:
                return False
            current_i += step_i
            current_j += step_j
        return True

    # Mouvements Possibles
    def possibleShoots(self, i, j):
        shoots = []

        for dx, dy in self.__directions:
            current_i = i + dx
            current_j = j + dy

            # Tant qu'on peut tirer dans cette direction, on ajoute la case
            while 0 <= current_i < self.__n and 0 <= current_j < self.__n and self.canShootArrows(i, j, current_i, current_j):
                shoots.append((current_i, current_j))
                current_i += dx
                current_j += dy
        return shoots

    # Effectue le tir
    def shootArrows(self, i, j, i_to, j_to):
        if self.canShootArrows(i, j, i_to, j_to):
            self.__board[i_to][j_to] = 3

    # Déplacement aléatoire du robot
    def botTurn(self):
        moves = []

        # Récupère toutes les options de déplacement
        for i in range(self.__n):
            for j in range(self.__n):
                if self.__board[i][j] == 2:  # pion du bot
                    for i_to, j_to in self.possibleMoves(i, j):
                        moves.append((i, j, i_to, j_to))

        # Sélectionne un déplacement aléatoire du bot
        i, j, i_to, j_to = random.choice(moves)
        self.move(i, j, i_to, j_to)

        # Tirs possibles depuis la nouvelle position
        shots = self.possibleShoots(i_to, j_to)
        if shots:
            i_shot, j_shot = random.choice(shots)
            self.shootArrows(i_to, j_to, i_shot, j_shot)
        return True

    # Change le joueur
    def updatePlayer(self):
        if self.__player == 1:
            self.__player += 1
        else:
            self.__player -= 1

    # Définis le gagnant
    def winner(self):
        for i in range(self.__n):
            for j in range(self.__n):
                if self.__board[i][j] == self.__player:
                    if self.selectPawn(i, j):
                        return 0

        return 2 if self.__player == 1 else 1

    # Gestion de la sauvegarde
    def saveBoard(self):
        # Gestion du fichier
        save = open('boards/save.txt', "w")
        for i in range(self.__n):
            for j in range(self.__n):
                save.write(f"{self.__board[i][j]}")
            save.write("\n")
        save.write(f"{self.__player}")
        save.write("\n")
        save.write(f"{self.__phase}")
        save.write("\n")
        save.write(f"{self.__selected_i}")
        save.write("\n")
        save.write(f"{self.__selected_j}")
        save.close()


algo = algorithmes()