import os
import tkinter as tk
import pillow as PIL

from PIL import Image, ImageTk, ImageEnhance

from config import (
    LEFT_WIDTH,
    WINDOW_HEIGHT,
    DARK_BLUE,
    BLUE,
    WHITE,
    BACKGROUND_PATH
)

from utils import rounded_rectangle


class LeftPanel:
    """
    Panel izquierdo de la pantalla de inicio de sesión.
    """

    def __init__(self, parent):

        self.parent = parent

        self.background_image = None

        self.panel = tk.Frame(
            parent,
            width=LEFT_WIDTH,
            height=WINDOW_HEIGHT,
            bg=DARK_BLUE
        )

        self.panel.place(
            x=0,
            y=0,
            width=LEFT_WIDTH,
            height=WINDOW_HEIGHT
        )

        self.create_panel()

    # ========================================================
    # CREAR PANEL
    # ========================================================

    def create_panel(self):

        self.create_background()

        self.create_top_label()

        self.create_title()

        self.create_description()

        self.create_statistics()

        self.create_copyright()

    # ========================================================
    # FONDO
    # ========================================================

    def create_background(self):

        if os.path.exists(BACKGROUND_PATH):

            try:

                image = Image.open(
                    BACKGROUND_PATH
                )

                image = image.resize(
                    (
                        LEFT_WIDTH,
                        WINDOW_HEIGHT
                    ),
                    Image.Resampling.LANCZOS
                )

                enhancer = ImageEnhance.Brightness(
                    image
                )

                image = enhancer.enhance(
                    0.42
                )

                self.background_image = ImageTk.PhotoImage(
                    image
                )

                background = tk.Label(
                    self.panel,
                    image=self.background_image,
                    borderwidth=0
                )

                background.place(
                    x=0,
                    y=0,
                    width=LEFT_WIDTH,
                    height=WINDOW_HEIGHT
                )

            except Exception:

                self.panel.configure(
                    bg=DARK_BLUE
                )

        # Capa azul sobre la imagen
        self.overlay = tk.Frame(
            self.panel,
            bg=DARK_BLUE
        )

        self.overlay.place(
            x=0,
            y=0,
            width=LEFT_WIDTH,
            height=WINDOW_HEIGHT
        )

    # ========================================================
    # TEXTO SUPERIOR
    # ========================================================

    def create_top_label(self):

        indicator = tk.Canvas(
            self.overlay,
            width=8,
            height=8,
            bg=DARK_BLUE,
            highlightthickness=0
        )

        indicator.place(
            x=34,
            y=37
        )

        indicator.create_oval(
            1,
            1,
            7,
            7,
            fill=BLUE,
            outline=BLUE
        )

        title = tk.Label(
            self.overlay,
            text="GESTIÓN EDUCATIVA INTELIGENTE",
            font=("Arial", 7, "bold"),
            fg="#DCE8F8",
            bg=DARK_BLUE
        )

        title.place(
            x=48,
            y=36
        )

    # ========================================================
    # TÍTULO
    # ========================================================

    def create_title(self):

        title = tk.Label(
            self.overlay,
            text=(
                "Control total de los\n"
                "recursos de tu institución"
            ),
            font=("Arial", 29, "bold"),
            fg=WHITE,
            bg=DARK_BLUE,
            justify="left"
        )

        title.place(
            x=35,
            y=159
        )

    # ========================================================
    # DESCRIPCIÓN
    # ========================================================

    def create_description(self):

        description = tk.Label(
            self.overlay,
            text=(
                "Administra aulas, laboratorios y equipos especializados en una sola\n"
                "plataforma unificada de manera ágil y transparente."
            ),
            font=("Arial", 10),
            fg="#B7C8DF",
            bg=DARK_BLUE,
            justify="left"
        )

        description.place(
            x=36,
            y=247
        )

    # ========================================================
    # ESTADÍSTICAS
    # ========================================================

    def create_statistics(self):

        card = tk.Canvas(
            self.overlay,
            width=377,
            height=93,
            bg=DARK_BLUE,
            highlightthickness=0
        )

        card.place(
            x=35,
            y=392
        )

        rounded_rectangle(
            card,
            0,
            0,
            377,
            93,
            radius=12,
            fill="#365579",
            outline="#567292"
        )

        # Título
        card.create_text(
            15,
            16,
            text="Recursos Activos en Tiempo Real",
            anchor="w",
            font=("Arial", 8, "bold"),
            fill="#E4ECF6"
        )

        # Separadores
        card.create_line(
            102,
            42,
            102,
            67,
            fill="#59718E"
        )

        card.create_line(
            250,
            42,
            250,
            67,
            fill="#59718E"
        )

        # Laboratorios
        card.create_text(
            15,
            52,
            text="18",
            anchor="w",
            font=("Arial", 18, "bold"),
            fill=WHITE
        )

        card.create_text(
            15,
            73,
            text="Laboratorios",
            anchor="w",
            font=("Arial", 7),
            fill="#C6D3E4"
        )

        # Aulas
        card.create_text(
            116,
            52,
            text="120+",
            anchor="w",
            font=("Arial", 18, "bold"),
            fill=WHITE
        )

        card.create_text(
            116,
            73,
            text="Aulas y Espacios",
            anchor="w",
            font=("Arial", 7),
            fill="#C6D3E4"
        )

        # Equipos
        card.create_text(
            266,
            52,
            text="450+",
            anchor="w",
            font=("Arial", 18, "bold"),
            fill=WHITE
        )

        card.create_text(
            266,
            73,
            text="Equipos Registrados",
            anchor="w",
            font=("Arial", 7),
            fill="#C6D3E4"
        )

    # ========================================================
    # COPYRIGHT
    # ========================================================

    def create_copyright(self):

        copyright_label = tk.Label(
            self.overlay,
            text="© 2026 Aulix Inc. Todos los derechos reservados.",
            font=("Arial", 7),
            fg="#8298B5",
            bg=DARK_BLUE
        )

        copyright_label.place(
            x=35,
            y=596
        )