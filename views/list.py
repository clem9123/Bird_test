import tkinter as tk
import json
import os
import webbrowser
from utils.images import charger_image
from utils.audio import jouer_son, arreter_son
from utils.data_loader import charger_donnees, sauvegarder_donnees

class BirdListScreen:
    def __init__(self, root, menu):
        self.root = root
        self.menu = menu
        self.frame = tk.Frame(root, padx=10, pady=10, bg="white")
        self.frame.pack(expand=True, fill=tk.BOTH)

        self.root.configure(bg="white")

        self.title_label = tk.Label(self.frame, text="Liste des Oiseaux", font=("Arial", 24), anchor=tk.CENTER, bg="white")
        self.title_label.pack(pady=10)

        self.retour_button = tk.Button(self.frame, text="Retour", command=self.retour_menu, bd=0, bg="white")
        self.retour_button.place(x=10, y=10)

        self.search_var = tk.StringVar()
        self.search_var.trace("w", self.update_list)
        self.search_entry = tk.Entry(self.frame, textvariable=self.search_var, width=50)
        self.search_entry.pack(pady=10)

        self.filter_communs = tk.BooleanVar()
        self.filter_communs.set(False)
        self.filter_button = tk.Checkbutton(self.frame, text="Afficher seulement les communs", variable=self.filter_communs, command=self.update_list, bg="white")
        self.filter_button.pack(pady=10)

        self.birds = charger_donnees()["oiseaux"]
        self.filtered_birds = self.birds

        self.listbox_frame = tk.Frame(self.frame, bg="white")
        self.listbox_frame.pack(pady=10, fill=tk.BOTH, expand=True)

        self.listbox = tk.Listbox(self.listbox_frame, width=90, height=20)
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.listbox.bind('<<ListboxSelect>>', self.on_select)

        self.scrollbar = tk.Scrollbar(self.listbox_frame, orient=tk.VERTICAL, command=self.listbox.yview)
        self.scrollbar.pack(side=tk.LEFT, fill=tk.Y)
        self.listbox.config(yscrollcommand=self.scrollbar.set)

        self.update_list()

    def update_list(self, *args):
        search_term = self.search_var.get().lower()
        self.filtered_birds = [bird for bird in self.birds if search_term in bird["nom"].lower()]
        if self.filter_communs.get():
            self.filtered_birds = [bird for bird in self.filtered_birds if bird["abondance"] == "commun"]
        self.listbox.delete(0, tk.END)
        for bird in self.filtered_birds:
            display_name = bird["nom"]
            if bird["abondance"] == "commun":
                display_name += " *"
            self.listbox.insert(tk.END, display_name)

    def on_select(self, event):
        selected_index = self.listbox.curselection()
        if selected_index:
            bird = self.filtered_birds[selected_index[0]]
            self.frame.pack_forget()
            BirdDetailScreen(self.root, self.menu, bird, self.birds)

    def retour_menu(self):
        self.frame.pack_forget()
        self.menu.show_menu()

class BirdDetailScreen:
    def __init__(self, root, menu, bird, birds):
        self.root = root
        self.menu = menu
        self.bird = bird
        self.birds = birds
        self.frame = tk.Frame(root, padx=10, pady=10, bg="white")
        self.frame.pack(expand=True, fill=tk.BOTH)

        self.root.configure(bg="white")

        self.title_label = tk.Label(self.frame, text=bird["nom"], font=("Arial", 24), anchor=tk.CENTER, bg="white")
        self.title_label.pack(pady=10)

        self.retour_button = tk.Button(self.frame, text="Retour", command=self.retour_liste, bd=0, bg="white")
        self.retour_button.place(x=10, y=10)

        image_path = os.path.join("data", bird["image_url"])
        image = charger_image(image_path, height=300)
        label_image = tk.Label(self.frame, image=image, bg="white")
        label_image.image = image  # Important pour conserver l’image en mémoire
        label_image.pack(pady=10)

        tk.Button(self.frame, text="Écouter le son", command=lambda: jouer_son(bird["mp3_url"]), bg="green", fg="white", bd=0).pack(pady=10)
        tk.Button(self.frame, text="Voir la page web", command=self.ouvrir_page_web, bg="blue", fg="white", bd=0).pack(pady=10)

        self.toggle_button = tk.Button(self.frame, text="Ajouter à Commun", command=self.toggle_abondance, bg="orange", fg="white", bd=0)
        self.toggle_button.pack(pady=10)
        self.update_toggle_button()

    def retour_liste(self):
        arreter_son()
        self.frame.pack_forget()
        BirdListScreen(self.root, self.menu)

    def ouvrir_page_web(self):
        arreter_son()
        webbrowser.open(self.bird["URL"])

    def toggle_abondance(self):
        if self.bird["abondance"] == "commun":
            self.bird["abondance"] = "non commun"
        else:
            self.bird["abondance"] = "commun"
        self.update_toggle_button()
        self.save_data()

    def update_toggle_button(self):
        if self.bird["abondance"] == "commun":
            self.toggle_button.config(text="Retirer de Commun")
        else:
            self.toggle_button.config(text="Ajouter à Commun")

    def save_data(self):
        sauvegarder_donnees({"oiseaux": self.birds})