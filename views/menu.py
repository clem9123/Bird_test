import tkinter as tk
from views.list import BirdListScreen
from views.quiz import QuizScreen
from views.stats import StatsScreen
from views.quiz_menu import QuizMenuScreen

class MenuScreen:
    def __init__(self, root):
        self.root = root
        self.frame = tk.Frame(root, padx=10, pady=10, bg="white")
        self.frame.pack(expand=True, fill=tk.BOTH)

        self.title_label = tk.Label(self.frame, text="Menu Principal", font=("Arial", 24), anchor=tk.CENTER, bg="white")
        self.title_label.pack(pady=40)

        self.button_frame = tk.Frame(self.frame, bg="white")
        self.button_frame.pack(expand=True, fill=tk.BOTH)

        self.create_buttons()

    def create_buttons(self):
        for widget in self.button_frame.winfo_children():
            widget.destroy()

        tk.Button(self.button_frame, text="Quiz", command=self.show_quiz_menu, bg="green", fg="white", bd=0).pack(pady=20, padx=200, fill=tk.BOTH, expand=True)
        tk.Button(self.button_frame, text="Liste des Oiseaux", command=self.show_list, bg="blue", fg="white", bd=0).pack(pady=20, padx=200, fill=tk.BOTH, expand=True)
        tk.Button(self.button_frame, text="Statistiques", command=self.show_stats, bg="orange", fg="white", bd=0).pack(pady=20, padx=200, fill=tk.BOTH, expand=True)

    def show_list(self):
        self.frame.pack_forget()
        BirdListScreen(self.root, self)

    def show_quiz_menu(self):
        self.frame.pack_forget()
        QuizMenuScreen(self.root, self)

    def show_quiz(self, commun=False):
        self.frame.pack_forget()
        QuizScreen(self.root, self, commun=commun, type_oiseau=None)

    def show_stats(self):
        self.frame.pack_forget()
        StatsScreen(self.root, self)

    def show_menu(self):
        self.create_buttons()
        self.frame.pack(expand=True, fill=tk.BOTH)
