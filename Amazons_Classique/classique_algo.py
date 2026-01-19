class algorithmes:

    def __init__(self, n=8):
        # Taille du plateau
        self.__n = n

        # Matrice représentant l'état du plateau
        self.__board = []

        # Joueur courant
        self.__player = 1

        # Phase du jeu
        self.__phase = "Select"

        # Coordonné pion
        self.__selected_i = None
        self.__selected_j = None

        # Directions autorisées pour déplacements et tirs
        self.__directions = [(1, 0), (-1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, 1), (1, -1)]

    # Getter, Setter
    def getN(self):
        return self.__n

    def setN(self, n):
        self.__n = n

    def getBoard(self):
        return self.__board

    def getPlayer(self):
        return self.__player

    def getPhase(self):
        return self.__phase

    def setPhase(self, phase):
        self.__phase = phase

    def getSelectedI(self):
        return self.__selected_i

    def setSelectedI(self, i):
        self.__selected_i = i

    def getSelectedJ(self):
        return self.__selected_j

    def setSelectedJ(self, j):
        self.__selected_j = j

    # Configuration du plateau
    def initBoard(self):
        # Choix du bon fichier suivant la taille du plateau
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

    # Sélection de la couleur du plateau
    def color(self, i, j):
        val = self.__board[i][j]
        if val == 0:
            return 'black'
        elif val == 1:
            return 'red'
        elif val == 2:
            return 'orange'
        elif val == 3:
            return 'green'

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

        # Gestion des règles
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

    # Effectue le tir
    def shootArrows(self, i, j, i_to, j_to):
        if self.canShootArrows(i, j, i_to, j_to):
            self.__board[i_to][j_to] = 3

    # Change le joueur
    def updatePlayer(self):
        if self.__player == 1:
            self.__player += 1
        else:
            self.__player -= 1

    # Définis le vainqueur
    def winner(self):
        for i in range(self.__n):
            for j in range(self.__n):
                if self.__board[i][j] == self.__player:
                    if self.selectPawn(i, j):
                        return 0

        return 2 if self.__player == 1 else 1
