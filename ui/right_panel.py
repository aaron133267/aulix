import tkinter as tk

from tkinter import messagebox

from config import (
    RIGHT_WIDTH,
    WINDOW_HEIGHT,
    BLUE,
    WHITE,
    TEXT_DARK,
    TEXT_GRAY,
    LIGHT_GRAY,
    BORDER
)

from utils import rounded_rectangle


class RightPanel:
    """
    Panel derecho que contiene el formulario de inicio de sesión.
    """

    def __init__(self, parent):

        self.parent = parent

        self.password_visible = False

        self.remember_me = tk.BooleanVar(
            value=True
        )

        self.panel = tk.Frame(
            parent,
            width=RIGHT_WIDTH,
            height=WINDOW_HEIGHT,
            bg=WHITE
        )

        self.panel.place(
            x=0,
            y=0,
            width=RIGHT_WIDTH,
            height=WINDOW_HEIGHT
        )

        self.create_panel()

    # ========================================================
    # CREAR PANEL
    # ========================================================

    def create_panel(self):

        self.create_logo()

        self.create_welcome()

        self.create_email()

        self.create_password()

        self.create_remember()

        self.create_login_button()

        self.create_terms()

    # ========================================================
    # LOGO
    # ========================================================

    def create_logo(self):

        logo_canvas = tk.Canvas(
            self.panel,
            width=24,
            height=24,
            bg=WHITE,
            highlightthickness=0
        )

        logo_canvas.place(
            x=76,
            y=55
        )

        rounded_rectangle(
            logo_canvas,
            1,
            1,
            23,
            23,
            radius=6,
            fill=BLUE,
            outline=BLUE
        )

        # Icono Aulix
        logo_canvas.create_rectangle(
            7,
            6,
            11,
            18,
            fill=WHITE,
            outline=WHITE
        )

        logo_canvas.create_rectangle(
            13,
            6,
            17,
            11,
            fill=WHITE,
            outline=WHITE
        )

        logo_canvas.create_rectangle(
            13,
            13,
            17,
            18,
            fill=WHITE,
            outline=WHITE
        )

        logo_text = tk.Label(
            self.panel,
            text="Aulix",
            font=("Arial", 16, "bold"),
            fg="#1F2C3D",
            bg=WHITE
        )

        logo_text.place(
            x=107,
            y=55
        )

    # ========================================================
    # BIENVENIDA
    # ========================================================

    def create_welcome(self):

        welcome = tk.Label(
            self.panel,
            text="Bienvenido de nuevo",
            font=("Arial", 20, "bold"),
            fg=TEXT_DARK,
            bg=WHITE
        )

        welcome.place(
            x=76,
            y=108
        )

        subtitle = tk.Label(
            self.panel,
            text="Inicia sesión en tu cuenta para gestionar recursos",
            font=("Arial", 8),
            fg=TEXT_GRAY,
            bg=WHITE
        )

        subtitle.place(
            x=77,
            y=140
        )

    # ========================================================
    # CORREO
    # ========================================================

    def create_email(self):

        label = tk.Label(
            self.panel,
            text="Correo electrónico",
            font=("Arial", 8, "bold"),
            fg=TEXT_DARK,
            bg=WHITE
        )

        label.place(
            x=76,
            y=282
        )

        self.email_entry = tk.Entry(
            self.panel,
            font=("Arial", 9),
            bg=LIGHT_GRAY,
            fg=TEXT_DARK,
            insertbackground=TEXT_DARK,
            relief="flat",
            highlightthickness=1,
            highlightbackground=BORDER,
            highlightcolor=BLUE
        )

        self.email_entry.place(
            x=76,
            y=298,
            width=307,
            height=31
        )

        self.email_entry.insert(
            0,
            "ejemplo@institucion.edu"
        )

        self.email_entry.configure(
            fg="#8B98A9"
        )

        self.email_entry.bind(
            "<FocusIn>",
            self.email_focus_in
        )

        self.email_entry.bind(
            "<FocusOut>",
            self.email_focus_out
        )

    # ========================================================
    # CONTRASEÑA
    # ========================================================

    def create_password(self):

        label = tk.Label(
            self.panel,
            text="Contraseña",
            font=("Arial", 8, "bold"),
            fg=TEXT_DARK,
            bg=WHITE
        )

        label.place(
            x=76,
            y=345
        )

        self.password_entry = tk.Entry(
            self.panel,
            font=("Arial", 9),
            bg=LIGHT_GRAY,
            fg=TEXT_DARK,
            insertbackground=TEXT_DARK,
            relief="flat",
            highlightthickness=1,
            highlightbackground=BORDER,
            highlightcolor=BLUE,
            show="•"
        )

        self.password_entry.place(
            x=76,
            y=361,
            width=307,
            height=31
        )

        self.password_entry.insert(
            0,
            "shh-top-secret"
        )

        self.password_entry.configure(
            fg="#8B98A9",
            show=""
        )

        self.password_entry.bind(
            "<FocusIn>",
            self.password_focus_in
        )

        self.password_entry.bind(
            "<FocusOut>",
            self.password_focus_out
        )

        # Botón del ojo
        self.eye_button = tk.Button(
            self.panel,
            text="◉",
            font=("Arial", 9),
            fg="#7A8A9F",
            bg=LIGHT_GRAY,
            activebackground=LIGHT_GRAY,
            activeforeground="#7A8A9F",
            relief="flat",
            borderwidth=0,
            cursor="hand2",
            command=self.toggle_password
        )

        self.eye_button.place(
            x=358,
            y=365,
            width=20,
            height=22
        )

    # ========================================================
    # RECORDARME
    # ========================================================

    def create_remember(self):

        remember = tk.Checkbutton(
            self.panel,
            text="Recordarme",
            variable=self.remember_me,
            font=("Arial", 8),
            fg=TEXT_GRAY,
            bg=WHITE,
            activebackground=WHITE,
            activeforeground=TEXT_GRAY,
            selectcolor=WHITE,
            cursor="hand2"
        )

        remember.place(
            x=74,
            y=400
        )

        forgot = tk.Label(
            self.panel,
            text="¿Olvidaste tu contraseña?",
            font=("Arial", 8, "bold"),
            fg=BLUE,
            bg=WHITE,
            cursor="hand2"
        )

        forgot.place(
            x=269,
            y=407
        )

        forgot.bind(
            "<Button-1>",
            self.forgot_password
        )

    # ========================================================
    # BOTÓN LOGIN
    # ========================================================

    def create_login_button(self):

        self.login_button = tk.Button(
            self.panel,
            text="Iniciar sesión",
            font=("Arial", 9, "bold"),
            fg=WHITE,
            bg=BLUE,
            activebackground="#2563D9",
            activeforeground=WHITE,
            relief="flat",
            borderwidth=0,
            cursor="hand2",
            command=self.login
        )

        self.login_button.place(
            x=76,
            y=432,
            width=307,
            height=33
        )

    # ========================================================
    # TÉRMINOS
    # ========================================================

    def create_terms(self):

        terms = tk.Label(
            self.panel,
            text="Al ingresar, aceptas nuestros ",
            font=("Arial", 7),
            fg="#8A98AA",
            bg=WHITE
        )

        terms.place(
            x=89,
            y=596
        )

        terms_service = tk.Label(
            self.panel,
            text="Términos de servicio",
            font=("Arial", 7),
            fg=BLUE,
            bg=WHITE,
            cursor="hand2"
        )

        terms_service.place(
            x=205,
            y=596
        )

        separator = tk.Label(
            self.panel,
            text=" y ",
            font=("Arial", 7),
            fg="#8A98AA",
            bg=WHITE
        )

        separator.place(
            x=275,
            y=596
        )

        privacy = tk.Label(
            self.panel,
            text="Política de privacidad.",
            font=("Arial", 7),
            fg=BLUE,
            bg=WHITE,
            cursor="hand2"
        )

        privacy.place(
            x=291,
            y=596
        )

    # ========================================================
    # EVENTOS DEL CORREO
    # ========================================================

    def email_focus_in(self, event):

        if self.email_entry.get() == "ejemplo@institucion.edu":

            self.email_entry.delete(
                0,
                tk.END
            )

            self.email_entry.configure(
                fg=TEXT_DARK
            )

    def email_focus_out(self, event):

        if self.email_entry.get().strip() == "":

            self.email_entry.insert(
                0,
                "ejemplo@institucion.edu"
            )

            self.email_entry.configure(
                fg="#8B98A9"
            )

    # ========================================================
    # EVENTOS DE CONTRASEÑA
    # ========================================================

    def password_focus_in(self, event):

        if self.password_entry.get() == "shh-top-secret":

            self.password_entry.delete(
                0,
                tk.END
            )

            self.password_entry.configure(
                fg=TEXT_DARK
            )

            if not self.password_visible:

                self.password_entry.configure(
                    show="•"
                )

    def password_focus_out(self, event):

        if self.password_entry.get().strip() == "":

            self.password_entry.insert(
                0,
                "shh-top-secret"
            )

            self.password_entry.configure(
                fg="#8B98A9",
                show=""
            )

    # ========================================================
    # MOSTRAR CONTRASEÑA
    # ========================================================

    def toggle_password(self):

        if self.password_entry.get() == "shh-top-secret":
            return

        self.password_visible = not self.password_visible

        if self.password_visible:

            self.password_entry.configure(
                show=""
            )

            self.eye_button.configure(
                text="○"
            )

        else:

            self.password_entry.configure(
                show="•"
            )

            self.eye_button.configure(
                text="◉"
            )

    # ========================================================
    # LOGIN
    # ========================================================

    def login(self):

        email = self.email_entry.get().strip()

        password = self.password_entry.get()

        # Validar correo vacío
        if (
            email == ""
            or email == "ejemplo@institucion.edu"
        ):

            messagebox.showerror(
                "Error",
                "Por favor, introduce tu correo electrónico."
            )

            self.email_entry.focus()

            return

        # Validar @
        if "@" not in email:

            messagebox.showerror(
                "Error",
                "Introduce un correo electrónico válido."
            )

            self.email_entry.focus()

            return

        # Validar contraseña vacía
        if (
            password == ""
            or password == "shh-top-secret"
        ):

            messagebox.showerror(
                "Error",
                "Por favor, introduce tu contraseña."
            )

            self.password_entry.focus()

            return

        # Validar longitud
        if len(password) < 8:

            messagebox.showerror(
                "Error",
                "La contraseña debe tener al menos 8 caracteres."
            )

            self.password_entry.focus()

            return

        # Aquí posteriormente se conectará
        # con el backend / API.

        messagebox.showinfo(
            "Inicio de sesión",
            "Inicio de sesión realizado correctamente."
        )

    # ========================================================
    # RECUPERAR CONTRASEÑA
    # ========================================================

    def forgot_password(self, event=None):

        messagebox.showinfo(
            "Recuperar contraseña",
            "Aquí se implementará el proceso para recuperar la contraseña."
        )