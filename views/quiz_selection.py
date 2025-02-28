import tkinter as tk
from views.quiz import QuizScreen

class QuizSelectionScreen:
    def __init__(self, root, menu):
        self.root = root
        self.menu = menu
        self.frame = tk.Frame(root)
        self.frame.pack(expand=True)

        tk.Button(self.frame, text="Retour", command=self.retour_menu).pack(anchor=tk.NW, pady=10, padx=10)

        tk.Label(self.frame, text="Sélectionnez le type de quiz", font=("Arial", 20)).pack(pady=20)

        tk.Button(self.frame, text="Quiz Commun", command=self.select_commun).pack(pady=10)
        tk.Button(self.frame, text="Quiz Tous les Oiseaux", command=self.select_tous).pack(pady=10)

    def select_commun(self):
        self.frame.pack_forget()
        QuizTypeSelectionScreen(self.root, self.menu, commun=True)

    def select_tous(self):
        self.frame.pack_forget()
        QuizTypeSelectionScreen(self.root, self.menu, commun=False)

    def retour_menu(self):
        self.frame.pack_forget()
        self.menu.show_menu()

class QuizTypeSelectionScreen:
    def __init__(self, root, menu, commun):
        self.root = root
        self.menu = menu
        self.commun = commun
        self.frame = tk.Frame(root)
        self.frame.pack(expand=True)

        tk.Button(self.frame, text="Retour", command=self.retour_menu).pack(anchor=tk.NW, pady=10, padx=10)

        tk.Label(self.frame, text="Sélectionnez le type d'oiseau", font=("Arial", 20)).pack(pady=20)

        tk.Button(self.frame, text="Tous les Types", command=lambda: self.start_quiz(None)).pack(pady=10)
        tk.Button(self.frame, text="Passereaux", command=lambda: self.start_quiz("passereaux")).pack(pady=10)
        tk.Button(self.frame, text="Rapaces", command=lambda: self.start_quiz("rapaces")).pack(pady=10)
        # Ajoutez d'autres types d'oiseaux ici

    def start_quiz(self, type_oiseau):
        self.frame.pack_forget()
        QuizScreen(self.root, self.menu, commun=self.commun, type_oiseau=type_oiseau)

    def retour_menu(self):
        self.frame.pack_forget()
        self.menu.show_menu()
