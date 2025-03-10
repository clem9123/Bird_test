import tkinter as tk
from tkinter import ttk
import json
import os
import webbrowser
from utils.images import charger_image
from utils.audio import jouer_son, arreter_son
from utils.data_loader import charger_donnees, sauvegarder_donnees, add_to_list
from tkinter import messagebox
from tkinter import simpledialog

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

        search_frame = tk.Frame(self.frame, bg="white")
        search_frame.pack(pady=10, fill=tk.X)

        self.search_entry = tk.Entry(search_frame, textvariable=self.search_var, width=50)
        self.search_entry.pack(side=tk.LEFT, padx=(0, 10))

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

        # Ajout d'une variable pour stocker le groupe sélectionné
        self.group_var = tk.StringVar()
        self.group_var.trace("w", self.update_list)

        # Récupération des groupes uniques à partir des données
        groupes = set()
        for bird in self.birds:
            groupes.update(bird["liste"])  # Ajout des familles de chaque oiseau

        self.groupes = sorted(groupes)

        # Création de la Combobox
        self.group_filter = ttk.Combobox(search_frame, textvariable=self.group_var, values=["Tous"] + self.groupes)
        self.group_filter.current(0)  # Sélectionner "Tous" par défaut
        self.group_filter.pack(side=tk.LEFT)

        self.add_list_button = tk.Button(search_frame, text="Ajouter une liste", command=self.ajouter_liste)
        self.add_list_button.pack(side=tk.LEFT, padx=(10, 0))

        self.context_menu = tk.Menu(self.root, tearoff=0)
        for groupe in self.groupes:
            self.context_menu.add_command(label=groupe, command=lambda g=groupe: self.ajouter_a_liste(g))

        # Liaison du clic droit à la Listbox
        self.listbox.bind("<Button-3>", self.show_context_menu)  # "<Button-3>" = clic droit

        self.update_list()

    def update_list(self, *args):
        search_term = self.search_var.get().lower()
        selected_group = self.group_var.get()

        self.filtered_birds = [
            bird for bird in self.birds
            if (search_term in bird["nom"].lower()) and 
               (selected_group == "Tous" or selected_group in bird["liste"])
        ]

        self.listbox.delete(0, tk.END)
        for bird in self.filtered_birds:
            self.listbox.insert(tk.END, bird["nom"])


    def on_select(self, event):
        selected_index = self.listbox.curselection()
        if selected_index:
            bird = self.filtered_birds[selected_index[0]]
            self.frame.pack_forget()
            BirdDetailScreen(self.root, self.menu, bird, self.birds)

    def retour_menu(self):
        self.frame.pack_forget()
        self.menu.show_menu()

    def show_context_menu(self, event):
        try:
            self.listbox.selection_clear(0, tk.END)
            self.listbox.selection_set(self.listbox.nearest(event.y))
            self.context_menu.delete(0, tk.END)  # Clear existing menu items

            selected_index = self.listbox.curselection()
            if selected_index:
                bird = self.filtered_birds[selected_index[0]]
                for groupe in self.groupes:
                    if groupe in bird["liste"]:
                        self.context_menu.add_command(label=f"Supprimer de {groupe}", command=lambda g=groupe: self.supprimer_de_liste(bird, g))
                    else:
                        self.context_menu.add_command(label=f"Ajouter à {groupe}", command=lambda g=groupe: self.ajouter_a_liste(bird, g))

            self.context_menu.post(event.x_root, event.y_root)
        finally:
            self.context_menu.grab_release()

    def ajouter_a_liste(self, bird, liste):
        add_to_list(bird["nom"], liste, self.birds)
        sauvegarder_donnees({"oiseaux": self.birds})
        self.update_list()

    def supprimer_de_liste(self, bird, liste):
        bird["liste"].remove(liste)
        sauvegarder_donnees({"oiseaux": self.birds})
        self.update_list()

    def ajouter_liste(self):
        new_list = simpledialog.askstring("Ajouter une liste", "Entrez le nom de la nouvelle liste:")
        if new_list:
            if new_list not in self.groupes:
                self.groupes.append(new_list)
                self.group_filter.config(values=["Tous"] + self.groupes)
                messagebox.showinfo("Succès", f"La liste '{new_list}' a été ajoutée. \n N'oubliez pas de l'ajouter à un oiseau pour qu'elle soit enregistrée.")
            else:
                messagebox.showwarning("Erreur", f"La liste '{new_list}' existe déjà.")

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

        self.lists_label = tk.Label(self.frame, text="Listes:", font=("Arial", 14), anchor=tk.W, bg="white")
        self.lists_label.pack(pady=5)

        self.lists_frame = tk.Frame(self.frame, bg="white")
        self.lists_frame.pack(pady=5)

        for liste in sorted(set([g for b in birds for g in b["liste"]])):
            if liste in bird["liste"]:
                btn = tk.Button(self.lists_frame, text=f"Supprimer de {liste}", bg="green", fg="white", command=lambda l=liste: self.toggle_liste(bird, l))
            else:
                btn = tk.Button(self.lists_frame, text=f"Ajouter à {liste}", bg="red", fg="white", command=lambda l=liste: self.toggle_liste(bird, l))
            btn.pack(pady=2, fill=tk.X)

    def retour_liste(self):
        arreter_son()
        self.frame.pack_forget()
        BirdListScreen(self.root, self.menu)

    def ouvrir_page_web(self):
        arreter_son()
        webbrowser.open(self.bird["URL"])

    def save_data(self):
        sauvegarder_donnees({"oiseaux": self.birds})

    def toggle_liste(self, bird, liste):
        if liste in bird["liste"]:
            bird["liste"].remove(liste)
        else:
            bird["liste"].append(liste)
        sauvegarder_donnees({"oiseaux": self.birds})
        self.update_buttons(bird)

    def update_buttons(self, bird):
        for widget in self.lists_frame.winfo_children():
            widget.destroy()

        for liste in sorted(set([g for b in self.birds for g in b["liste"]])):
            if liste in bird["liste"]:
                btn = tk.Button(self.lists_frame, text=f"Supprimer de {liste}", bg="green", fg="white", command=lambda l=liste: self.toggle_liste(bird, l))
            else:
                btn = tk.Button(self.lists_frame, text=f"Ajouter à {liste}", bg="red", fg="white", command=lambda l=liste: self.toggle_liste(bird, l))
            btn.pack(pady=2, fill=tk.X)