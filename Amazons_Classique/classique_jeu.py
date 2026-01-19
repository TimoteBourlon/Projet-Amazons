#Librairies
from tkinter import *
from tkinter import messagebox
from classique_algo import algorithmes

class Jeu:
    def __init__(self):
        self.__algo = algorithmes()

        # Taille des cases par défaut
        self.__case = 40

        # Lancement de l'interface
        self.__root = Tk()
        self.__root.config(bg='black')
        self.__root.title("Amazons Classique")
        self.__root.resizable(False, False)

        self.__canvas = Canvas(self.__root)

        # Configuration de la partie
        self.__textAmazonsGame = Label(self.__root, text="Amazons Classique", bg="black", fg="white", font=("Courier", 12))
        self.__textAmazonsGame.pack(padx=10, pady=20)

        self.__askStart = Label(self.__root, text="Party settings", bg="black", fg="white", font=("Courier", 12))
        self.__askStart.pack(padx=10, pady=20)

        # Tailles des cases
        self.__texteSizeCase = Label(self.__root, text="Size of boxes", bg="black", fg="white")
        self.__texteSizeCase.pack()
        self.__choiceSizeCase = Scale(self.__root, orient='horizontal', from_=40, to=70, command=self.sizeCase, bg="black", fg="white", highlightthickness=0)
        self.__choiceSizeCase.pack()

        # Taille du plateau
        self.__textSizeBoard = Label(self.__root, text="Size of board", bg="black", fg="white")
        self.__textSizeBoard.pack(pady=(20, 0))
        self.__choice = Spinbox(self.__root, from_=6, to=10)
        self.__choice.pack()


        self.__btnStart = Button(self.__root, text='Start', command=self.startDisplay)
        self.__btnStart.pack(pady=20)

        # Information du tour
        self.__playerText = StringVar()
        self.__text1 = Label(self.__root, textvariable=self.__playerText, bg="black", fg="white", font=("Courier", 18))
        self.__phaseGame = StringVar()
        self.__text2 = Label(self.__root, textvariable=self.__phaseGame, bg="black", fg="white", font=("Courier", 18))

        # Rafraîchissement
        self.__root.mainloop()

    def startDisplay(self):
        # Initialisation du plateau
        n = int(self.__choice.get())

        self.__algo.setN(n)
        self.__algo.initBoard()

        # Mis en forme de la grille en canvas
        self.__canvas.config(width=self.__algo.getN() * self.__case + 1, height=self.__algo.getN() * self.__case + 1, highlightthickness=0, bd=0, bg="black")
        self.__canvas.pack(padx=50, pady=50)

        # Gestion clique
        self.__canvas.bind('<Button-1>', self.processPhase)

        # Texte affiché durant la partie
        self.__text1.pack(padx=50)
        self.__text2.pack(padx=50, pady=20)

        # Retrait des objets inutiles en partie
        self.__askStart.destroy()
        self.__choice.destroy()
        self.__btnStart.destroy()
        self.__textSizeBoard.destroy()
        self.__choiceSizeCase.destroy()
        self.__texteSizeCase.destroy()

        self.updateDisplay()

    def display(self):
        self.__canvas.delete("all")
        board = self.__algo.getBoard()

        for i in range(self.__algo.getN()):
            for j in range(self.__algo.getN()):
                color = self.__algo.color(i, j)
                self.__canvas.create_rectangle(self.__case * j, self.__case * i, self.__case * (j + 1), self.__case * (i + 1), outline='white', fill='black')
                if board[i][j] == 1 or board[i][j] == 2:
                    if i == self.__algo.getSelectedI() and j == self.__algo.getSelectedJ():
                        self.__canvas.create_oval(self.__case * j + 10, self.__case * i + 10, self.__case * (j + 1) - 10, self.__case * (i + 1) - 10, outline="white", width=3, fill="black")
                        self.__canvas.create_oval(self.__case * j + 15, self.__case * i + 15, self.__case * (j + 1) - 15, self.__case * (i + 1) - 15, outline="", fill=color)
                    else:
                        self.__canvas.create_oval(self.__case * j + 10, self.__case * i + 10, self.__case * (j + 1) - 10, self.__case * (i + 1) - 10, fill=color)
                elif board[i][j] == 3:
                    self.__canvas.create_line(self.__case * j + 10, self.__case * i + 10, self.__case * (j + 1) - 10, self.__case * (i + 1) - 10, width=4, fill=color)
                    self.__canvas.create_line(self.__case * j + 10, self.__case * (i + 1) - 10, self.__case * (j + 1) - 10, self.__case * i + 10, width=4, fill=color)

    def processPhase(self, event):
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
                self.updateWinner()

    # Taille des cases
    def sizeCase(self, event):
        self.__case = self.__choiceSizeCase.get()

        # Ne met à jour que si plateau chargé
        if self.__algo.getBoard() and len(self.__algo.getBoard()) > 0:
            self.updateDisplay()

    # Mise à jour des données du plateau
    def updateDisplay(self):
        self.__playerText.set('Player: ' + str(self.__algo.getPlayer()))
        self.__phaseGame.set(self.__algo.getPhase())
        self.display()

    # Mise à jour des données de la partie
    def updateLogic(self):
        self.__algo.updatePlayer()
        self.__player = self.__algo.getPlayer()
        self.updateDisplay()

    # Cherche s'il y a un vainqueur
    def updateWinner(self):
        winner = self.__algo.winner()
        if winner != 0:
            self.updateDisplay()
            messagebox.showinfo("End of party", f"The player {winner} is a winner !")
            reponse = messagebox.askyesno("New Game", "Do you want play another game?")
            self.__root.destroy()
            if reponse:
                Jeu()

jeu = Jeu()