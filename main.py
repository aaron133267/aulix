import tkinter as tk

from config import (
    WINDOW_WIDTH,
    WINDOW_HEIGHT
)

from utils import center_window

from ui.login import LoginScreen


def main():

    # ========================================================
    # CREAR VENTANA
    # ========================================================

    root = tk.Tk()

    root.title(
        "Aulix - Iniciar sesión"
    )

    root.resizable(
        False,
        False
    )

    root.configure(
        bg="white"
    )

    # ========================================================
    # CENTRAR VENTANA
    # ========================================================

    center_window(
        root,
        WINDOW_WIDTH,
        WINDOW_HEIGHT
    )

    # ========================================================
    # CREAR PANTALLA DE LOGIN
    # ========================================================

    LoginScreen(
        root
    )

    # ========================================================
    # EJECUTAR APLICACIÓN
    # ========================================================

    root.mainloop()


if __name__ == "__main__":

    main()