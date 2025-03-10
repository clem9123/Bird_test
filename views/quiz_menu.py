import tkinter as tk
from views.quiz import QuizScreen
from utils.data_loader import charger_donnees

class QuizMenuScreen:
    def __init__(self, root, menu):
        self.root = root
        self.menu = menu
        self.frame = tk.Frame(root, padx=10, pady=10, bg="white")
        self.frame.pack(expand=True, fill=tk.BOTH)

        self.title_label = tk.Label(self.frame, text="Choisissez une option", font=("Arial", 24), anchor=tk.CENTER, bg="white")
        self.title_label.pack(pady=40)

        self.button_frame = tk.Frame(self.frame, bg="white")
        self.button_frame.pack(expand=True, fill=tk.BOTH)

        # Charger les listes depuis le fichier JSON en utilisant la fonction charger_données
        data = charger_donnees()
        
        # Récupérer toutes les listes uniques
        listes = set()
        for oiseau in data['oiseaux']:
            listes.update(oiseau['liste'])

        # Créer un bouton pour chaque liste
        for liste in listes:
            tk.Button(self.button_frame, text=liste.capitalize(), command=lambda l=liste: self.show_list_quiz(l), bg="green", fg="white", bd=0).pack(pady=10, padx=200, fill=tk.BOTH, expand=True)

        # Bouton pour tous les oiseaux
        tk.Button(self.button_frame, text="Tous", command=self.show_all_quiz, bg="blue", fg="white", bd=0).pack(pady=20, padx=200, fill=tk.BOTH, expand=True)
        tk.Button(self.button_frame, text="Retour", command=self.retour_menu, bg="red", fg="white", bd=0).pack(pady=20, padx=200, fill=tk.BOTH, expand=True)

    def show_list_quiz(self, liste):
        self.frame.pack_forget()
        QuizScreen(self.root, self.menu, commun=False, type_oiseau=liste)

    def show_all_quiz(self):
        self.frame.pack_forget()
        QuizScreen(self.root, self.menu, commun=False, type_oiseau=None)

    def retour_menu(self):
        self.frame.pack_forget()
        self.menu.show_menu()
