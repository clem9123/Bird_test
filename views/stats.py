import tkinter as tk

class StatsScreen:
    def __init__(self, root, menu):
        self.root = root
        self.menu = menu
        self.frame = tk.Frame(root)
        self.frame.pack(expand=True)

        tk.Button(self.frame, text="Retour", command=self.retour_menu).pack(anchor=tk.NW, pady=10, padx=10)

        # Ajoutez ici le code pour afficher les statistiques

    def retour_menu(self):
        self.frame.pack_forget()
        self.menu.show_menu()

    def display_stats(self):
        # Method to display stats
        pass

    def update_stats(self, new_stats):
        # Method to update stats
        pass