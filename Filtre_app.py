import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageFilter

class MiniImageApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Mini-App de Traitement d'Images")
        self.root.geometry("1000x600")
        
        # Variables de stockage pour les images
        self.original_pil_image = None
        self.display_size = (400, 400)
        
        # Initialisation de l'interface
        self.create_menu()
        self.create_layout()

    def create_menu(self):
        """Crée la barre de menu supérieure selon le schéma fourni."""
        menubar = tk.Menu(self.root)
        
        # 1er Menu: File (Fichier)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Uploader Image", command=self.upload_image)
        file_menu.add_separator()
        file_menu.add_command(label="Quitter", command=self.root.quit)
        menubar.add_cascade(label="File", menu=file_menu)
        
        # 2ème Menu: Filtres
        filters_menu = tk.Menu(menubar, tearoff=0)
        filters_menu.add_command(label="Filtre Moyenneur (Flou)", command=self.apply_filter_moyenneur)
        filters_menu.add_command(label="Filtre Médian", command=self.apply_filter_median)
        filters_menu.add_command(label="Filtre Nagao (Simulé)", command=self.apply_filter_nagao_dummy)
        filters_menu.add_separator()
        filters_menu.add_command(label="Tous les filtres", command=self.apply_all_filters)
        menubar.add_cascade(label="Filtres", menu=filters_menu)
        
        # 3ème Menu: Contour
        contour_menu = tk.Menu(menubar, tearoff=0)
        contour_menu.add_command(label="Détection de Contours (Simple)", command=self.apply_contour_simple)
        menubar.add_cascade(label="Contour", menu=contour_menu)
        
        self.root.config(menu=menubar)

    def create_layout(self):
        """Organise l'interface en deux zones principales : Image originale et Résultats."""
        main_frame = tk.Frame(self.root, bg="#f0f0f0")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Zone Gauche : Image Originale
        self.left_frame = tk.LabelFrame(main_frame, text="Image Originale", labelanchor="n", font=("Arial", 12, "bold"))
        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.label_original = tk.Label(self.left_frame, text="Aucune image chargée", bg="white")
        self.label_original.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Zone Droite : Résultats
        self.right_frame = tk.LabelFrame(main_frame, text="Résultats", labelanchor="n", font=("Arial", 12, "bold"))
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Un conteneur interne pour pouvoir afficher un ou plusieurs résultats de manière flexible
        self.results_container = tk.Frame(self.right_frame, bg="white")
        self.results_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.label_result_placeholder = tk.Label(self.results_container, text="Les résultats s'afficheront ici", bg="white")
        self.label_result_placeholder.pack(fill=tk.BOTH, expand=True)

    def upload_image(self):
        """Permet de charger une image depuis le disque et l'affiche à gauche."""
        file_path = filedialog.askopenfilename(
            filetypes=[("Images", "*.png *.jpg *.jpeg *.bmp *.gif")]
        )
        if file_path:
            try:
                # Chargement et sauvegarde de l'image originale
                self.original_pil_image = Image.open(file_path)
                
                # Redimensionnement pour l'affichage sans déformer l'original
                preview_image = self.original_pil_image.copy()
                preview_image.thumbnail(self.display_size)
                
                photo = ImageTk.PhotoImage(preview_image)
                self.label_original.config(image=photo, text="")
                self.label_original.image = photo  # Garder une référence
                
                # Réinitialiser la zone de résultats
                self.clear_results_area()
                self.label_result_placeholder = tk.Label(self.results_container, text="Choisissez un traitement dans le menu", bg="white")
                self.label_result_placeholder.pack(fill=tk.BOTH, expand=True)
                
            except Exception as e:
                messagebox.showerror("Erreur", f"Impossible de charger l'image : {e}")

    def clear_results_area(self):
        """Vide le panneau de droite pour préparer un nouvel affichage."""
        for widget in self.results_container.winfo_children():
            widget.destroy()

    def display_single_result(self, processed_image, title="Résultat"):
        """Affiche un seul résultat dans la zone de droite."""
        self.clear_results_area()
        
        # Frame pour structurer le titre et l'image
        result_box = tk.Frame(self.results_container, bg="white")
        result_box.pack(fill=tk.BOTH, expand=True)
        
        title_label = tk.Label(result_box, text=title, font=("Arial", 10, "italic"), bg="white")
        title_label.pack(pady=5)
        
        # Redimensionnement temporaire pour l'affichage
        preview = processed_image.copy()
        preview.thumbnail(self.display_size)
        photo = ImageTk.PhotoImage(preview)
        
        img_label = tk.Label(result_box, image=photo, bg="white")
        img_label.image = photo
        img_label.pack(fill=tk.BOTH, expand=True)

    # --- Fonctions de traitement d'images (Exemples pour l'Étape 1) ---

    def apply_filter_moyenneur(self):
        if self.original_pil_image is None:
            messagebox.showwarning("Attention", "Veuillez d'abord charger une image.")
            return
        # Simulation d'un filtre linéaire passe-bas (Moyenneur) avec un flou de boîte (BoxBlur)
        result = self.original_pil_image.filter(ImageFilter.BoxBlur(radius=3))
        self.display_single_result(result, title="Filtre Moyenneur (Radius = 3)")

    def apply_filter_median(self):
        if self.original_pil_image is None:
            messagebox.showwarning("Attention", "Veuillez d'abord charger une image.")
            return
        # Filtre non-linéaire Médian
        result = self.original_pil_image.filter(ImageFilter.MedianFilter(size=3))
        self.display_single_result(result, title="Filtre Médian (Size = 3)")

    def apply_filter_nagao_dummy(self):
        if self.original_pil_image is None:
            messagebox.showwarning("Attention", "Veuillez d'abord charger une image.")
            return
        # Nagao demande un algorithme spécifique. Pour cette maquette, nous simulons
        # un effet d'atténuation de bruit en combinant un flou bilatéral ou un filtre de lissage (Smooth)
        result = self.original_pil_image.filter(ImageFilter.SMOOTH_MORE)
        self.display_single_result(result, title="Filtre de Nagao (Simulation - Smooth)")

    def apply_contour_simple(self):
        if self.original_pil_image is None:
            messagebox.showwarning("Attention", "Veuillez d'abord charger une image.")
            return
        # Extraction de contour de base avec Pillow
        result = self.original_pil_image.convert("L").filter(ImageFilter.FIND_EDGES)
        self.display_single_result(result, title="Contours Détectés (Simple)")

    def apply_all_filters(self):
        """Affiche les résultats de plusieurs filtres côte à côte dans la zone droite."""
        if self.original_pil_image is None:
            messagebox.showwarning("Attention", "Veuillez d'abord charger une image.")
            return
        
        self.clear_results_area()
        
        # Création d'une grille 2x2 dans la zone de droite pour présenter les filtres
        grid_frame = tk.Frame(self.results_container, bg="white")
        grid_frame.pack(fill=tk.BOTH, expand=True)
        
        # Liste des filtres à appliquer pour la démonstration globale
        filters_to_run = [
            ("Moyenneur", self.original_pil_image.filter(ImageFilter.BoxBlur(radius=3))),
            ("Médian", self.original_pil_image.filter(ImageFilter.MedianFilter(size=3))),
            ("Nagao (Simulé)", self.original_pil_image.filter(ImageFilter.SMOOTH_MORE)),
            ("Contour", self.original_pil_image.convert("L").filter(ImageFilter.FIND_EDGES))
        ]
        
        # Génération des vignettes
        for index, (title, img) in enumerate(filters_to_run):
            row = index // 2
            col = index % 2
            
            cell = tk.Frame(grid_frame, bd=1, relief=tk.RIDGE, bg="white")
            cell.grid(row=row, column=col, sticky="nsew", padx=5, pady=5)
            
            lbl_title = tk.Label(cell, text=title, font=("Arial", 8, "bold"), bg="white")
            lbl_title.pack(anchor="n")
            
            # Ajustement de taille plus petite pour la grille
            thumb = img.copy()
            thumb.thumbnail((180, 180))
            photo = ImageTk.PhotoImage(thumb)
            
            lbl_img = tk.Label(cell, image=photo, bg="white")
            lbl_img.image = photo  # conserver la référence
            lbl_img.pack(fill=tk.BOTH, expand=True)
            
        # Configurer la grille pour qu'elle s'étende uniformément
        grid_frame.rowconfigure(0, weight=1)
        grid_frame.rowconfigure(1, weight=1)
        grid_frame.columnconfigure(0, weight=1)
        grid_frame.columnconfigure(1, weight=1)

if __name__ == "__main__":
    root = tk.Tk()
    app = MiniImageApp(root)
    root.mainloop()