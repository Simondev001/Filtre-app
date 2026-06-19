import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageFilter
import numpy as np

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
        # ============================================================
        #  SECTION FILTRES - réorganisée en deux catégories :
        #  Filtres Linéaires / Filtres Non-Linéaires
        # ============================================================
        filters_menu = tk.Menu(menubar, tearoff=0)

        # --- Sous-menu : Filtres Linéaires ---
        linear_filters_menu = tk.Menu(filters_menu, tearoff=0)
        linear_filters_menu.add_command(label="Filtre Moyenneur (Mean)", command=self.apply_filter_moyenneur)
        linear_filters_menu.add_command(label="Filtre Gaussien (Gaussian)", command=self.apply_filter_gaussian)
        linear_filters_menu.add_command(label="Filtre Passe-Haut (High Pass)", command=self.apply_filter_high_pass)
        linear_filters_menu.add_command(label="Filtre de Butterworth", command=self.apply_filter_butterworth)
        linear_filters_menu.add_command(label="Filtre de Netteté (Sharpen)", command=self.apply_filter_sharpen)
        filters_menu.add_cascade(label="Filtres Linéaires", menu=linear_filters_menu)

        filters_menu.add_separator()

        # --- Sous-menu : Filtres Non-Linéaires ---
        # ============================================================
        #  FILTRES NON-LINÉAIRES RETENUS (validés avec le professeur) :
        #  Médian, Nagao, Min-Max, Érosion, Ouverture (Opening)
        # ============================================================
        non_linear_filters_menu = tk.Menu(filters_menu, tearoff=0)
        non_linear_filters_menu.add_command(label="Filtre Médian", command=self.apply_filter_median)
        non_linear_filters_menu.add_command(label="Filtre Nagao (Simulé)", command=self.apply_filter_nagao_dummy)
        non_linear_filters_menu.add_command(label="Filtre Min-Max", command=self.apply_filter_min_max)
        non_linear_filters_menu.add_command(label="Érosion", command=self.apply_filter_erosion)
        non_linear_filters_menu.add_command(label="Ouverture (Opening)", command=self.apply_filter_opening)
        filters_menu.add_cascade(label="Filtres Non-Linéaires", menu=non_linear_filters_menu)
        # ============================================================
        #  FIN SOUS-MENU FILTRES NON-LINÉAIRES
        # ============================================================

        filters_menu.add_separator()
        filters_menu.add_command(label="Tous les filtres", command=self.apply_all_filters)
        menubar.add_cascade(label="Filtres", menu=filters_menu)
        # ============================================================
        #  FIN SECTION FILTRES
        # ============================================================
        # 3ème Menu: Contour

        contour_menu = tk.Menu(menubar, tearoff=0)
        # contour_menu.add_command(label="Détection de Contours (Simple)", command=self.apply_contour_simple)
        menubar.add_cascade(label="Contour", menu=contour_menu)
        self.root.config(menu=menubar)

    def create_layout(self):
        """Crée la disposition principale de la fenêtre : zone gauche (image
        originale) et zone droite (résultats des filtres)."""
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Zone Gauche : Image originale
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

    # ============================================================
    #  NOUVELLE MÉTHODE : affichage de DEUX résultats côte à côte
    #  (utilisée par le Filtre Min-Max, qui doit comparer le résultat
    #  du Filtre Minimum et celui du Filtre Maximum sur la même image)
    # ============================================================
    def display_two_results(self, img1, title1, img2, title2, main_title="Résultat"):
        """Affiche deux images de résultat côte à côte dans la zone de droite,
        chacune avec son propre sous-titre, sous un titre principal commun."""
        self.clear_results_area()

        # Titre principal (ex: "Filtre Min-Max")
        main_title_label = tk.Label(self.results_container, text=main_title,
                                     font=("Arial", 10, "italic"), bg="white")
        main_title_label.pack(pady=5)

        # Conteneur horizontal pour placer les deux images l'une à côté de l'autre
        pair_frame = tk.Frame(self.results_container, bg="white")
        pair_frame.pack(fill=tk.BOTH, expand=True)

        for img, sub_title in [(img1, title1), (img2, title2)]:
            cell = tk.Frame(pair_frame, bg="white")
            cell.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

            lbl_title = tk.Label(cell, text=sub_title, font=("Arial", 9, "bold"), bg="white")
            lbl_title.pack(pady=3)

            # Redimensionnement temporaire pour l'affichage (chaque vignette
            # prend la moitié de l'espace disponible, donc taille réduite)
            preview = img.copy()
            preview.thumbnail((self.display_size[0] // 2, self.display_size[1] // 2))
            photo = ImageTk.PhotoImage(preview)

            img_label = tk.Label(cell, image=photo, bg="white")
            img_label.image = photo  # conserver la référence (sinon le garbage collector l'efface)
            img_label.pack(fill=tk.BOTH, expand=True)
    # ============================================================
    #  FIN NOUVELLE MÉTHODE display_two_results
    # ============================================================

    

    def apply_filter_moyenneur(self):
        """[Linéaire] Filtre Moyenneur (Mean) - flou de boîte (BoxBlur)."""
        if self.original_pil_image is None:
            messagebox.showwarning("Attention", "Veuillez d'abord charger une image.")
            return
        result = self.original_pil_image.filter(ImageFilter.BoxBlur(radius=3))
        self.display_single_result(result, title="Filtre Moyenneur / Mean (Radius = 3)")

    def apply_filter_gaussian(self):
        """[Linéaire] Filtre Gaussien (Gaussian Blur)."""
        if self.original_pil_image is None:
            messagebox.showwarning("Attention", "Veuillez d'abord charger une image.")
            return
        result = self.original_pil_image.filter(ImageFilter.GaussianBlur(radius=2))
        self.display_single_result(result, title="Filtre Gaussien (Radius = 2)")

    def apply_filter_high_pass(self):
        """[Linéaire] Filtre Passe-Haut (High Pass) - noyau de convolution 3x3."""
        if self.original_pil_image is None:
            messagebox.showwarning("Attention", "Veuillez d'abord charger une image.")
            return
        result = self._compute_high_pass(self.original_pil_image)
        self.display_single_result(result, title="Filtre Passe-Haut (High Pass)")

    def apply_filter_butterworth(self):
        """[Linéaire] Filtre de Butterworth (passe-bas, domaine fréquentiel)."""
        if self.original_pil_image is None:
            messagebox.showwarning("Attention", "Veuillez d'abord charger une image.")
            return
        result = self._compute_butterworth(self.original_pil_image, cutoff=50, order=2)
        self.display_single_result(result, title="Filtre de Butterworth (D0=50, n=2)")

    def apply_filter_sharpen(self):
        """[Linéaire] Filtre de Netteté (Sharpen)."""
        if self.original_pil_image is None:
            messagebox.showwarning("Attention", "Veuillez d'abord charger une image.")
            return
        result = self.original_pil_image.filter(ImageFilter.SHARPEN)
        self.display_single_result(result, title="Filtre de Netteté (Sharpen)")

    def _compute_high_pass(self, pil_image):
        """Calcule (sans afficher) le résultat du filtre Passe-Haut linéaire.
        Utilisé à la fois par apply_filter_high_pass() et apply_all_filters()."""
        kernel = ImageFilter.Kernel(
            (3, 3),
            [-1, -1, -1,
             -1,  8, -1,
             -1, -1, -1],
            scale=1,
            offset=128
        )
        return pil_image.filter(kernel)

    def _compute_butterworth(self, pil_image, cutoff=50, order=2):
        """Calcule (sans afficher) le résultat du filtre de Butterworth linéaire
        dans le domaine fréquentiel (via FFT). Image traitée en niveaux de gris.
        Utilisé à la fois par apply_filter_butterworth() et apply_all_filters()."""
        img_gray = pil_image.convert("L")
        img_array = np.array(img_gray, dtype=np.float64)

        # Transformée de Fourier
        f = np.fft.fft2(img_array)
        fshift = np.fft.fftshift(f)

        rows, cols = img_array.shape
        crow, ccol = rows // 2, cols // 2

        # Construction du filtre de Butterworth (passe-bas)
        u = np.arange(rows) - crow
        v = np.arange(cols) - ccol
        V, U = np.meshgrid(v, u)
        D = np.sqrt(U ** 2 + V ** 2)

        H = 1 / (1 + (D / cutoff) ** (2 * order))

        # Application du filtre puis transformée inverse
        fshift_filtered = fshift * H
        f_ishift = np.fft.ifftshift(fshift_filtered)
        img_back = np.fft.ifft2(f_ishift)
        img_back = np.abs(img_back)
        img_back = np.clip(img_back, 0, 255).astype(np.uint8)

        return Image.fromarray(img_back)

    # ----------------------------------------------------------------
    # --------------------- FILTRES NON-LINÉAIRES ---------------------
    # ----------------------------------------------------------------

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

    # ============================================================
    #  FILTRES NON-LINÉAIRES RETENUS (validés avec le professeur) :
    #  Filtre Min-Max, Érosion, Ouverture (Opening)
    # ============================================================

    def _compute_erosion(self, pil_image, size=3):
        """Calcule (sans afficher) l'érosion morphologique en niveaux de gris.

        Principe : on fait glisser un élément structurant (ici un carré de
        taille `size`x`size`) sur l'image, et on remplace chaque pixel par
        la valeur MINIMALE des pixels couverts par cet élément structurant.
        -> Effet : les zones claires "rétrécissent", les zones sombres
        "s'étendent" ; les petits détails clairs/le bruit ponctuel disparaissent.

        Remarque : l'érosion en niveaux de gris avec un élément structurant
        carré est mathématiquement équivalente à un Filtre Minimum local,
        d'où l'utilisation de ImageFilter.MinFilter ci-dessous.
        Utilisée par apply_filter_erosion() et apply_filter_opening()."""
        return pil_image.filter(ImageFilter.MinFilter(size=size))

    def _compute_dilation(self, pil_image, size=3):
        """Calcule (sans afficher) la dilatation morphologique en niveaux de gris.

        Principe : opération duale de l'érosion : on remplace chaque pixel
        par la valeur MAXIMALE des pixels couverts par l'élément structurant.
        -> Effet : les zones claires "s'étendent", les zones sombres "rétrécissent".

        Équivalente à un Filtre Maximum local (ImageFilter.MaxFilter).
        Utilisée ici uniquement comme brique pour construire l'Ouverture
        (Opening = Érosion puis Dilatation) dans apply_filter_opening()."""
        return pil_image.filter(ImageFilter.MaxFilter(size=size))

    def apply_filter_min_max(self):
        """[Non-Linéaire] Filtre Min-Max.

        Ce "filtre" regroupe en fait les deux filtres d'ordre statistique de
        base (Min et Max), affichés ici côte à côte pour bien visualiser
        leur effet opposé sur l'image :
          - Filtre MIN : chaque pixel <- minimum de son voisinage
                          (assombrit l'image, base de l'Érosion)
          - Filtre MAX : chaque pixel <- maximum de son voisinage
                          (éclaircit l'image, base de la Dilatation)
        Ces deux filtres servent de fondation aux opérations morphologiques
        Érosion / Ouverture définies plus bas."""
        if self.original_pil_image is None:
            messagebox.showwarning("Attention", "Veuillez d'abord charger une image.")
            return

        # Calcul du Filtre Minimum (voisinage 3x3)
        min_result = self.original_pil_image.filter(ImageFilter.MinFilter(size=3))
        # Calcul du Filtre Maximum (voisinage 3x3)
        max_result = self.original_pil_image.filter(ImageFilter.MaxFilter(size=3))

        # Affichage côte à côte des deux résultats pour comparaison directe
        self.display_two_results(
            min_result, "Min (Size = 3)",
            max_result, "Max (Size = 3)",
            main_title="Filtre Min-Max"
        )

    def apply_filter_erosion(self):
        """[Non-Linéaire] Érosion morphologique (en niveaux de gris).

        Utilise _compute_erosion() : remplace chaque pixel par le minimum
        de son voisinage 3x3. Réduit les zones claires et élimine les petits
        détails clairs / le bruit ponctuel."""
        if self.original_pil_image is None:
            messagebox.showwarning("Attention", "Veuillez d'abord charger une image.")
            return
        result = self._compute_erosion(self.original_pil_image, size=3)
        self.display_single_result(result, title="Érosion Morphologique (Size = 3)")

    def apply_filter_opening(self):
        """[Non-Linéaire] Ouverture (Opening).

        Définition : Ouverture = Dilatation( Érosion( image ) )
        c'est-à-dire qu'on applique d'abord une Érosion, puis une Dilatation
        sur le résultat obtenu.

        Effet : supprime les petits détails clairs isolés et le bruit
        ponctuel (comme l'érosion seule), tout en restaurant ensuite la
        taille globale des objets restants grâce à la dilatation qui suit
        (contrairement à l'érosion seule, qui rétrécit tout durablement)."""
        if self.original_pil_image is None:
            messagebox.showwarning("Attention", "Veuillez d'abord charger une image.")
            return
        # Étape 1 : Érosion de l'image originale
        eroded = self._compute_erosion(self.original_pil_image, size=3)
        # Étape 2 : Dilatation appliquée sur le résultat de l'érosion
        result = self._compute_dilation(eroded, size=3)
        self.display_single_result(result, title="Ouverture / Opening (Érosion + Dilatation, Size = 3)")

   
    def apply_all_filters(self):
        """Affiche les résultats de tous les filtres (Linéaires + Non-Linéaires)
        côte à côte dans la zone droite, regroupés par catégorie."""
        if self.original_pil_image is None:
            messagebox.showwarning("Attention", "Veuillez d'abord charger une image.")
            return
        
        self.clear_results_area()
        
        # Création d'une grille dans la zone de droite pour présenter les filtres
        grid_frame = tk.Frame(self.results_container, bg="white")
        grid_frame.pack(fill=tk.BOTH, expand=True)
        
        # Liste des filtres à appliquer pour la démonstration globale,
        # regroupés par catégorie : Linéaires puis Non-Linéaires
        filters_to_run = [
            # --- Filtres Linéaires ---
            ("Moyenneur / Mean (Linéaire)", self.original_pil_image.filter(ImageFilter.BoxBlur(radius=3))),
            ("Gaussien (Linéaire)", self.original_pil_image.filter(ImageFilter.GaussianBlur(radius=2))),
            ("Passe-Haut (Linéaire)", self._compute_high_pass(self.original_pil_image)),
            ("Butterworth (Linéaire)", self._compute_butterworth(self.original_pil_image, cutoff=50, order=2)),
            ("Netteté / Sharpen (Linéaire)", self.original_pil_image.filter(ImageFilter.SHARPEN)),
            # --- Filtres Non-Linéaires ---
            ("Médian (Non-Linéaire)", self.original_pil_image.filter(ImageFilter.MedianFilter(size=3))),
            ("Nagao Simulé (Non-Linéaire)", self.original_pil_image.filter(ImageFilter.SMOOTH_MORE)),
            # --- Filtre Min-Max : on affiche ici les deux composantes (Min et Max) ---
            ("Min (Non-Linéaire)", self.original_pil_image.filter(ImageFilter.MinFilter(size=3))),
            ("Max (Non-Linéaire)", self.original_pil_image.filter(ImageFilter.MaxFilter(size=3))),
            # --- Érosion et Ouverture (Opening = Érosion puis Dilatation) ---
            ("Érosion (Non-Linéaire)", self._compute_erosion(self.original_pil_image, size=3)),
            ("Ouverture / Opening (Non-Linéaire)", self._compute_dilation(
                self._compute_erosion(self.original_pil_image, size=3), size=3)),
        ]
        
        # Génération des vignettes - grille à 4 colonnes pour accueillir
        # l'ensemble des filtres Linéaires + Non-Linéaires
        num_cols = 4
        for index, (title, img) in enumerate(filters_to_run):
            row = index // num_cols
            col = index % num_cols
            
            cell = tk.Frame(grid_frame, bd=1, relief=tk.RIDGE, bg="white")
            cell.grid(row=row, column=col, sticky="nsew", padx=5, pady=5)
            
            lbl_title = tk.Label(cell, text=title, font=("Arial", 8, "bold"), bg="white")
            lbl_title.pack(anchor="n")
            
            # Ajustement de taille plus petite pour la grille
            thumb = img.copy()
            thumb.thumbnail((150, 150))
            photo = ImageTk.PhotoImage(thumb)
            
            lbl_img = tk.Label(cell, image=photo, bg="white")
            lbl_img.image = photo  # conserver la référence
            lbl_img.pack(fill=tk.BOTH, expand=True)
        
        # Configurer la grille pour qu'elle s'étende uniformément
        num_rows = (len(filters_to_run) + num_cols - 1) // num_cols
        for r in range(num_rows):
            grid_frame.rowconfigure(r, weight=1)
        for c in range(num_cols):
            grid_frame.columnconfigure(c, weight=1)

    # ================================================================
    # ====================  FIN SECTION FILTRES  ====================
    # ================================================================

if __name__ == "__main__":
    root = tk.Tk()
    app = MiniImageApp(root)
    root.mainloop()