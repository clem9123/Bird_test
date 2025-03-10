import tkinter as tk
from PIL import Image, ImageTk
import random
import os
import webbrowser
from utils.data_loader import charger_donnees
from utils.images import charger_image
from utils.audio import jouer_son, arreter_son

class QuizScreen:
    def __init__(self, root, menu, commun, type_oiseau):
        self.root = root
        self.menu = menu
        self.frame = tk.Frame(root, bg="white")
        self.frame.pack(expand=True, fill=tk.BOTH)

        self.oiseaux = charger_donnees()["oiseaux"]
        if type_oiseau:
            self.oiseaux = [o for o in self.oiseaux if type_oiseau in o["liste"]]

        self.oiseau_actuel = None

        self.retour_button = tk.Button(self.frame, text="Retour", command=self.retour_menu, bd=0, bg="white")
        self.retour_button.place(x=10, y=10)

        self.title_label = tk.Label(self.frame, text="Quiz", font=("Arial", 24), bg="white")
        self.title_label.pack(pady=40)

        button_frame = tk.Frame(self.frame, bg="white")
        button_frame.pack(pady=10, fill=tk.X)

        self.play_image = self.load_image("data/ui/play.jpg", 50, 50)
        self.reveal_image = self.load_image("data/ui/reveal.jpg", 50, 50)
        self.yes_image = self.load_image("data/ui/yes.png", 50, 50)
        self.no_image = self.load_image("data/ui/no.jpg", 50, 50)

        tk.Button(button_frame, image=self.play_image, command=self.jouer_son, bd=0, bg="white").pack(side=tk.LEFT, padx=5, pady=5, expand=True)
        tk.Button(button_frame, image=self.reveal_image, command=self.reveler_nom, bd=0, bg="white").pack(side=tk.RIGHT, padx=5, pady=5, expand=True)

        self.label_nom = tk.Label(self.frame, text="Qui est cet oiseau ?", font=("Arial", 16, "bold"), bg="white")
        self.label_nom.pack(pady=10, fill=tk.X)

        self.image_frame = tk.Frame(self.frame, width=300, height=300)
        self.image_frame.pack(pady=10)
        self.image_frame.pack_propagate(False)

        self.default_image = self.load_image("data/ui/blur.png", 300, 300)
        self.label_image = tk.Label(self.image_frame, image=self.default_image)
        self.label_image.pack()

        self.web_button = tk.Button(self.frame, text="Page Web", command=self.ouvrir_page_web, bd=0, bg="white")
        self.web_button.pack(pady=10)

        button_frame_bottom = tk.Frame(self.frame, bg="white")
        button_frame_bottom.pack(pady=10, fill=tk.X)

        tk.Button(button_frame_bottom, image=self.no_image, command=lambda: self.reponse_utilisateur(False), bd=0, bg="white").pack(side=tk.LEFT, padx=10, pady=5, expand=True)
        tk.Button(button_frame_bottom, image=self.yes_image, command=lambda: self.reponse_utilisateur(True), bd=0, bg="white").pack(side=tk.RIGHT, padx=10, pady=5, expand=True)

        self.charger_nouvel_oiseau()

    def load_image(self, path, width, height):
        image = Image.open(path)
        image = image.resize((width, height), Image.LANCZOS)
        return ImageTk.PhotoImage(image)

    def charger_nouvel_oiseau(self):
        while True:
            self.oiseau_actuel = random.choice(self.oiseaux)
            image_path = os.path.join("data", self.oiseau_actuel.get("image_url", ""))
            mp3_path = os.path.join("data", self.oiseau_actuel.get("mp3_url", ""))
            if os.path.exists(image_path) and os.path.exists(mp3_path):
                break
        self.label_nom.config(text="Qui est cet oiseau ?")
        self.label_image.config(image=self.default_image)
        self.image_path = image_path

    def reveler_image(self):
        image = charger_image(self.image_path, height=300)  # Ajuster la hauteur de l'image
        self.label_image.config(image=image)
        self.label_image.image = image  # Important pour conserver l’image en mémoire

    def jouer_son(self):
        if self.oiseau_actuel and "mp3_url" in self.oiseau_actuel:
            jouer_son(self.oiseau_actuel["mp3_url"])
        else:
            print("Aucun son disponible pour cet oiseau.")

    def reveler_nom(self):
        self.label_nom.config(text=self.oiseau_actuel["nom"])
        self.reveler_image()

    def reponse_utilisateur(self, connu):
        arreter_son()
        if connu:
            self.oiseau_actuel["niveau"] = max(0, self.oiseau_actuel["niveau"] - 1)
        else:
            self.oiseau_actuel["niveau"] += 1
        self.charger_nouvel_oiseau()

    def ouvrir_page_web(self):
        if self.oiseau_actuel and "URL" in self.oiseau_actuel:
            webbrowser.open(self.oiseau_actuel["URL"])
        else:
            print("Aucune URL disponible pour cet oiseau.")

    def retour_menu(self):
        arreter_son()
        self.frame.pack_forget()
        self.menu.show_menu()
