#Librairies
from tkinter import *
from tkinter import messagebox

from PIL import Image, ImageTk
from PIL.Image import Resampling

from variante_algo import algorithmes

class Jeu:
    def __init__(self):
        self.__algo = algorithmes()
        self.__case = 40

        # Démarrage de l'interface
        self.__root = Tk()
        self.__root.config(bg='white')
        self.__root.title("Amazons Game")
        self.__root.resizable(False, False)

        self.__canvas = Canvas(self.__root)

        # Configuration de la partie
        self.__frameMain = Frame(self.__root, bg="white")
        self.__frameMain.pack(pady=20)

        self.__askStart = Label(self.__frameMain, text="Party settings", bg="white", fg="black", font=("Courier", 16, "bold"), activebackground="white", activeforeground="white")
        self.__askStart.pack(padx=10, pady=(10,30))

        # Reprendre une partie interrompue
        self.__textSaveGame = Label(self.__frameMain, text="Back to game ?", bg="white", fg="black", font=("Courier", 12))
        self.__textSaveGame.pack(padx=10)

        self.__canvasToggleSaveGame = Canvas(self.__frameMain, width=50, height=25, bg="white", highlightthickness=0)
        self.__canvasToggleSaveGame.pack(pady=20)
        self.__toggleStateSaveGame = False
        self.__toggleRectangleSaveGame = self.__canvasToggleSaveGame.create_rectangle(1, 1, 47, 25, fill="red", outline="")
        self.__toggleSquareSaveGame = self.__canvasToggleSaveGame.create_rectangle(4, 4, 22, 22, fill="white", outline="")
        self.__canvasToggleSaveGame.bind("<Button-1>", self.setToggleSaveGame)

        # Choix de la variante
        self.__textVariant = Label(self.__frameMain, text="Do you want to play the variant ?", bg="white", fg="black", font=("Courier", 12))
        self.__textVariant.pack(padx=10)

        self.__canvasToggleVariant = Canvas(self.__frameMain, width=50, height=25, bg="white", highlightthickness=0)
        self.__canvasToggleVariant.pack(pady=20)

        self.__toggleStateVariant = False
        self.__toggleRectangleVariant = self.__canvasToggleVariant.create_rectangle(1, 1, 47, 25, fill="red", outline="")
        self.__toggleSquareVariant = self.__canvasToggleVariant.create_rectangle(4, 4, 22, 22, fill="white", outline="")
        self.__canvasToggleVariant.bind("<Button-1>", self.setToggleVariant)

        # Sélection de l'adversaire
        self.__textVsBot = Label(self.__frameMain, text="Do you want to play versus bot ?", bg="white", fg="black", font=("Courier", 12))
        self.__textVsBot.pack(padx=10)
        self.__canvasToggleVsBot = Canvas(self.__frameMain, width=50, height=25, bg="white", highlightthickness=0)
        self.__canvasToggleVsBot.pack(pady=20)
        self.__toggleStateVsBot = False
        self.__toggleRectangleVsBot = self.__canvasToggleVsBot.create_rectangle(1,1,47,25,fill="red", outline="")
        self.__toggleSquareVsBot = self.__canvasToggleVsBot.create_rectangle(4, 4, 22, 22, fill="white", outline="")
        self.__canvasToggleVsBot.bind("<Button-1>", self.setToggleVsBot)

        # Tailles des cases
        self.__frameSec = Frame(self.__frameMain, bg="white")
        self.__frameSec.pack(side="left", padx=20, pady=20)

        self.__textSizeCase = Label(self.__frameSec, text="Size of boxes", bg="white", fg="black", font=("Courier", 12))
        self.__textSizeCase.pack()
        self.__choiceSizeCase = Scale(self.__frameSec, orient='horizontal', from_=40, to=70, command=self.setSizeCase, bg="white", fg="black", highlightthickness=0)
        self.__choiceSizeCase.pack()

        # Taille du plateau
        self.__frameDuo = Frame(self.__frameMain, bg="white")
        self.__frameDuo.pack(side="right", padx=20)

        self.__textSizeBoard = Label(self.__frameDuo, text="Size of board", bg="white", fg="black", font=("Courier", 12))
        self.__textSizeBoard.pack(pady=(0,20))
        self.__choice = Spinbox(self.__frameDuo, from_=6, to=10)
        self.__choice.pack()

        # Information du tour
        self.__playerText = StringVar()
        self.__text1 = Label(self.__root, textvariable=self.__playerText, bg="white", fg="black", font=("Courier", 18))
        self.__phaseGame = StringVar()
        self.__text2 = Label(self.__root, textvariable=self.__phaseGame, bg="white", fg="black", font=("Courier", 18))

        # Images
        self.__imgPlayer1 = Image.open("assets/player1.png")
        self.__imgPlayer2 = Image.open("assets/player2.png")
        self.__imgBloc = Image.open("assets/wall.png")
        self.__imgSharderBoard = Image.open("assets/shaderBoard.png")
        self.__imgGold = Image.open("assets/gold.png")
        self.__imgFire = Image.open("assets/fire.png")
        self.__imgSelectP1 = Image.open("assets/selectP1.png")
        self.__imgSelectP2 = Image.open("assets/selectP2.png")
        self.__imgStart = Image.open("assets/settings/start.png")
        self.__imgSave = Image.open("assets/save.png")

        self.updateImage()

        # Lancement du jeu
        self.__imgStartLabel = Label(self.__root, image=self.__imgStartSet, bg="white", cursor="hand2")  # type: ignore
        self.__imgStartLabel.pack()
        self.__imgStartLabel.bind("<Button-1>", self.startDisplay)

        # Image décorative
        illustration = Image.open("assets/settings/illustration.png")
        self.__illustrationPhoto = ImageTk.PhotoImage(illustration)
        self.__illustrationLabel = Label(self.__root, image=self.__illustrationPhoto, bg="white")  # type: ignore
        self.__illustrationLabel.pack()

        # Rafraîchissement
        self.__root.mainloop()

    def startDisplay(self, event = None):
        # Initialisation du plateau
        n = int(self.__choice.get())

        # Lancement sous-programmes
        self.setVariantOption()
        self.setVsBotOption()

        self.__algo.setN(n)
        self.__algo.initBoard()

        self.setReplayGame()

        # Affichage du nom (UX)
        self.__textAmazonsGame = Label(self.__root, text="Amazons Game", bg="white", fg="black", font=("Courier", 22))
        self.__textAmazonsGame.pack(padx=10, pady=10)

        # Création de la grille en canvas
        self.__canvas.config(width=self.__algo.getN() * self.__case + 1, height=self.__algo.getN() * self.__case + 1, highlightthickness=0, bd=0, bg="#ece9e1")
        self.__canvas.pack(padx=50, pady=30)

        # Détection du cliqué
        self.__canvas.bind('<Button-1>', self.processPhase)

        # Texte affiché durant la partie
        self.__text1.pack(padx=50)
        self.__text2.pack(padx=50, pady=10)

        # Retrait des objets inutiles en partie
        self.__frameMain.destroy()
        self.__illustrationLabel.destroy()
        self.__askStart.destroy()
        self.__choice.destroy()
        self.__imgStartLabel.destroy()
        self.__textSizeBoard.destroy()
        self.__choiceSizeCase.destroy()
        self.__textSizeCase.destroy()
        self.__textVariant.destroy()
        self.__textSaveGame.destroy()
        self.__textVsBot.destroy()
        self.__canvasToggleVsBot.destroy()
        self.__canvasToggleSaveGame.destroy()
        self.__canvasToggleVariant.destroy()

        # Sauvegarde de la partie en cours
        self.__imgSaveLabel = Label(self.__root, image=self.__imgSaveSet, bg="white", cursor="hand2")  # type: ignore
        self.__imgSaveLabel.pack(pady=10)
        self.__imgSaveLabel.bind("<Button-1>", self.setSave)

        self.updateDisplay()

    # Actualisation des informations du plateau
    def display(self):
        self.__canvas.delete("all")
        board = self.__algo.getBoard()

        # Évaluation des coups réalisables
        coups_jouables = []

        # Prévisualisation selon la phase
        if self.__algo.getPhase() == "Move" and self.__algo.getSelectedI() is not None:
            coups_jouables = self.__algo.possibleMoves(self.__algo.getSelectedI(), self.__algo.getSelectedJ())
        elif self.__algo.getPhase() == "Fire" and self.__algo.getSelectedI() is not None:
            coups_jouables = self.__algo.possibleShoots(self.__algo.getSelectedI(), self.__algo.getSelectedJ())

        # Parcours de la grille
        for i in range(self.__algo.getN()):
            for j in range(self.__algo.getN()):
                self.__canvas.create_image(self.__case * j, self.__case * i, anchor=NW, image=self.__imgSharderSet)
                #Possibilités de coups
                if (i, j) in coups_jouables:
                    if self.__algo.getPhase() == "Move":
                        if self.__algo.getVariant():
                            if board[i][j] == 1:
                                self.__canvas.create_image(self.__case * j, self.__case * i, anchor=NW,
                                                           image=self.__imgSelectP1Set)
                            elif board[i][j] == 2:
                                self.__canvas.create_image(self.__case * j, self.__case * i, anchor=NW,
                                                           image=self.__imgSelectP2Set)
                        self.__canvas.create_image((self.__case * j + 8), self.__case * i, anchor=NW,
                                                   image=self.__imgGoldSet)
                    elif self.__algo.getPhase() == "Fire":
                        self.__canvas.create_image((self.__case * j + 17, self.__case * i + 15), anchor=NW,
                                                   image=self.__imgFireSet)

                # Affichage des éléments du plateau
                if board[i][j] == 1:
                    self.__canvas.create_image(self.__case * j, self.__case * i, anchor=NW,
                                               image=self.__imgPlayer1Set)
                elif board[i][j] == 2:
                    self.__canvas.create_image(self.__case * j + 1, self.__case * i, anchor=NW,
                                               image=self.__imgPlayer2Set)
                elif board[i][j] == 3:
                    self.__canvas.create_image(self.__case * j, self.__case * i, anchor=NW, image=self.__imgBlocSet)

    # Mise à jour des données du plateau
    def updateDisplay(self):
        self.__playerText.set('Player: ' + str(self.__algo.getPlayer()))
        self.__phaseGame.set(self.__algo.getPhase())
        self.display()

    # Mise à jour des données de la partie
    def updateLogic(self):
        self.__algo.updatePlayer()  # ou switchPlayer
        self.updateWinner()
        self.__player = self.__algo.getPlayer()
        self.updateDisplay()

        if self.__algo.getVsBot() and self.__algo.getPlayer() == 2:
            played = self.__algo.botTurn()
            # S'occupe de la clôture de la partie si nécessaire
            if played:
                self.updateWinner()
                self.__root.after(1500, self.updateLogic)  # type: ignore

    # Cherche s'il y a un vainqueur
    def updateWinner(self):
        winner = self.__algo.winner()
        if winner != 0:
            self.updateDisplay()
            messagebox.showinfo("End of party", f"The player : {winner} is a winner !")
            reponse = messagebox.askyesno("New Game", "Do you want play another game?")
            self.__root.destroy()
            if reponse:
                Jeu()

    # Définition des imgs à la fenêtre
    def updateImage(self):
        size = self.__case

        # Fond du plateau
        shader = self.__imgSharderBoard.resize((size, size), Resampling.LANCZOS)
        self.__imgSharderSet = ImageTk.PhotoImage(shader)

        # Murs
        bloc = self.__imgBloc.resize((size, size), Resampling.LANCZOS)
        self.__imgBlocSet = ImageTk.PhotoImage(bloc)

        # Joueur 1
        p1 = self.__imgPlayer1.resize((size, size), Resampling.LANCZOS)
        self.__imgPlayer1Set = ImageTk.PhotoImage(p1)

        # Joueur 2
        p2 = self.__imgPlayer2.resize((size, size), Resampling.LANCZOS)
        self.__imgPlayer2Set = ImageTk.PhotoImage(p2)

        # Pièces
        coin = self.__imgGold.resize((size - 15, size - 15), Resampling.LANCZOS)
        self.__imgGoldSet = ImageTk.PhotoImage(coin)

        # Possibilité de tirs
        fireCase = self.__imgFire.resize((size - 30, size - 30), Resampling.LANCZOS)
        self.__imgFireSet = ImageTk.PhotoImage(fireCase)

        # Selection joueur 1
        selectP1 = self.__imgSelectP1.resize((size, size), Resampling.LANCZOS)
        self.__imgSelectP1Set = ImageTk.PhotoImage(selectP1)

        # Selection joueur 2
        selectP2 = self.__imgSelectP2.resize((size, size), Resampling.LANCZOS)
        self.__imgSelectP2Set = ImageTk.PhotoImage(selectP2)

        # Img début du jeu
        startGame = self.__imgStart.resize((size + 15, size), Resampling.LANCZOS)
        self.__imgStartSet = ImageTk.PhotoImage(startGame)

        # img sauvegarde du jeu
        saveGame = self.__imgSave.resize((size + 15, size), Resampling.LANCZOS)
        self.__imgSaveSet = ImageTk.PhotoImage(saveGame)

    def processPhase(self, event):
        # Conversion des coordonnées
        j = event.x // self.__case
        i = event.y // self.__case

        # Sélection d'un pion
        if self.__algo.getPhase() == "Select":
            if self.__algo.selectPawn(i, j):
                self.__algo.setSelectedI(i)
                self.__algo.setSelectedJ(j)

                self.__algo.setPhase("Move")
                self.updateDisplay()

        # Déplacement du pion sélectionné
        elif self.__algo.getPhase() == "Move":
            if self.__algo.canMove(self.__algo.getSelectedI(), self.__algo.getSelectedJ(), i, j):
                self.__algo.move(self.__algo.getSelectedI(), self.__algo.getSelectedJ(), i, j)

                self.__algo.setSelectedI(i)
                self.__algo.setSelectedJ(j)

                self.__algo.setPhase("Fire")
                self.updateDisplay()

        # Tir d'un bloc
        elif self.__algo.getPhase() == "Fire":
            if self.__algo.canShootArrows(self.__algo.getSelectedI(), self.__algo.getSelectedJ(), i, j):
                self.__algo.shootArrows(self.__algo.getSelectedI(), self.__algo.getSelectedJ(), i, j)

                self.__algo.setSelectedI(None)
                self.__algo.setSelectedJ(None)

                self.__algo.setPhase("Select")
                self.updateWinner()
                self.updateLogic()

    # État du bouton sauvegarde
    def setToggleSaveGame(self, event):
        self.__toggleStateSaveGame = not self.__toggleStateSaveGame
        if self.__toggleStateSaveGame:
            self.__canvasToggleSaveGame.itemconfig(self.__toggleSquareSaveGame, fill="white")
            self.__canvasToggleSaveGame.itemconfig(self.__toggleRectangleSaveGame, fill="green")
            self.__canvasToggleSaveGame.coords(self.__toggleSquareSaveGame, 26, 4, 44, 22)
        else:
            self.__canvasToggleSaveGame.itemconfig(self.__toggleSquareSaveGame, fill="white")
            self.__canvasToggleSaveGame.itemconfig(self.__toggleRectangleSaveGame, fill="red")
            self.__canvasToggleSaveGame.coords(self.__toggleSquareSaveGame, 4, 4, 22, 22)

    # État du bouton variante
    def setToggleVariant(self, event):
        self.__toggleStateVariant = not self.__toggleStateVariant
        if self.__toggleStateVariant:
            self.__canvasToggleVariant.itemconfig(self.__toggleSquareVariant, fill="white")
            self.__canvasToggleVariant.itemconfig(self.__toggleRectangleVariant, fill="green")
            self.__canvasToggleVariant.coords(self.__toggleSquareVariant, 26, 4, 44, 22)
        else:
            self.__canvasToggleVariant.itemconfig(self.__toggleSquareVariant, fill="white")
            self.__canvasToggleVariant.itemconfig(self.__toggleRectangleVariant, fill="red")
            self.__canvasToggleVariant.coords(self.__toggleSquareVariant, 4, 4, 22, 22)

    # État du bouton robot
    def setToggleVsBot(self, event):
        self.__toggleStateVsBot = not self.__toggleStateVsBot
        if self.__toggleStateVsBot:
            self.__canvasToggleVsBot.itemconfig(self.__toggleSquareVsBot, fill="white")
            self.__canvasToggleVsBot.itemconfig(self.__toggleRectangleVsBot, fill="green")
            self.__canvasToggleVsBot.coords(self.__toggleSquareVsBot, 26, 4, 44, 22)
        else:
            self.__canvasToggleVsBot.itemconfig(self.__toggleSquareVsBot, fill="white")
            self.__canvasToggleVsBot.itemconfig(self.__toggleRectangleVsBot, fill="red")
            self.__canvasToggleVsBot.coords(self.__toggleSquareVsBot, 4, 4, 22, 22)

    # Taille des cases pour les images
    def setSizeCase(self, value):
        self.__case = int(float(value))
        self.updateImage()
        self.__imgStartLabel.config(image=self.__imgStartSet)

    # Choix de la version
    def setVariantOption(self):
        self.__algo.setVariant(self.__toggleStateVariant)

    # Choix du robot
    def setVsBotOption(self):
        self.__algo.setVsBot(self.__toggleStateVsBot)

    # Bonus : chargement d'une partie sauvegardée
    def setReplayGame(self):
        self.__algo.setReplayGame(self.__toggleStateSaveGame)

        if self.__algo.getReplayGame():
            # Gestion du fichier
            save = open('boards/save.txt', "r")
            lignes = save.readlines()
            lignesBoard = lignes[:-4]
            lignePlayer = lignes[-4].strip()
            lignePhase = lignes[-3].strip()
            ligneSelectedI = lignes[-2].strip()
            ligneSelectedJ = lignes[-1].strip()
            save.close()

            # Conversion des lignes du plateau en matrice
            l = [line.strip() for line in lignesBoard]
            replayBoard = [[int(c) for c in line] for line in l]

            # Vérifie que la taille du plateau correspond à celle choisie
            while len(replayBoard) != self.__algo.getN():
                messagebox.showwarning("Error",f"The selected board size is not the right. The right size is {len(replayBoard)}")
                self.__root.mainloop()

            # Chargement des informations de la partie
            self.__algo.setPlayer(int(lignePlayer))
            self.__algo.setPhase(str(lignePhase))

            # Gestion des valeurs None pour la sélection
            if ligneSelectedI == "None":
                self.__algo.setSelectedI(ligneSelectedI)
            else:
                self.__algo.setSelectedI(int(ligneSelectedI))
            if ligneSelectedJ == "None":
                self.__algo.setSelectedJ(ligneSelectedJ)
            else:
                self.__algo.setSelectedJ(int(ligneSelectedJ))

            # Application du plateau reconstitué
            self.__algo.setBoard(replayBoard)
            self.display()

            # Si le bot doit jouer immédiatement après chargement
            if self.__algo.getVsBot() and self.__algo.getPlayer() == 2:
                self.__algo.updatePlayer()
                self.__root.after(500, self.updateLogic)  # type: ignore

    # Alerte de sauvegarde écrasant l'ancienne
    def setSave(self, event = None):
        self.updateDisplay()
        reponse = messagebox.askyesno(
            "Sauvegarde game",
            "Do you want to save your actual game? If you have another current game saved, it will be deleted."
        )
        if reponse:
            self.__algo.saveBoard()

jeu = Jeu()