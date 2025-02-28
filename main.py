import tkinter as tk
from views.menu import MenuScreen

class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Bird Quiz")
        self.root.geometry("600x700")  # Agrandir légèrement la fenêtre
        self.root.configure(bg="white")  # Définir la couleur de fond en blanc
        self.current_screen = None
        self.show_menu()

    def show_menu(self):
        if self.current_screen is not None:
            self.current_screen.frame.pack_forget()
        self.current_screen = MenuScreen(self.root)
        self.current_screen.show_menu()

if __name__ == "__main__":
    app = App()
    app.root.mainloop()
