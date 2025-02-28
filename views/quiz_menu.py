import tkinter as tk
from views.quiz import QuizScreen

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

        tk.Button(self.button_frame, text="Favoris", command=self.show_favorites_quiz, bg="orange", fg="white", bd=0).pack(pady=20, padx=200, fill=tk.BOTH, expand=True)
        tk.Button(self.button_frame, text="Tous", command=self.show_all_quiz, bg="blue", fg="white", bd=0).pack(pady=20, padx=200, fill=tk.BOTH, expand=True)
        tk.Button(self.button_frame, text="Retour", command=self.retour_menu, bg="red", fg="white", bd=0).pack(pady=20, padx=200, fill=tk.BOTH, expand=True)

    def show_favorites_quiz(self):
        self.frame.pack_forget()
        QuizScreen(self.root, self.menu, commun=True, type_oiseau=None)

    def show_all_quiz(self):
        self.frame.pack_forget()
        QuizScreen(self.root, self.menu, commun=False, type_oiseau=None)

    def retour_menu(self):
        self.frame.pack_forget()
        self.menu.show_menu()
