import tkinter as tk


def center_window(window, width, height):
    """
    Centra una ventana en la pantalla.
    """

    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x = int((screen_width - width) / 2)
    y = int((screen_height - height) / 2)

    window.geometry(
        f"{width}x{height}+{x}+{y}"
    )


def rounded_rectangle(
    canvas,
    x1,
    y1,
    x2,
    y2,
    radius=10,
    fill=None,
    outline=None
):
    """
    Crea un rectángulo con bordes redondeados
    dentro de un Canvas.
    """

    points = [
        x1 + radius, y1,
        x2 - radius, y1,
        x2, y1,
        x2, y1 + radius,
        x2, y2 - radius,
        x2, y2,
        x2 - radius, y2,
        x1 + radius, y2,
        x1, y2,
        x1, y2 - radius,
        x1, y1 + radius,
        x1, y1
    ]

    return canvas.create_polygon(
        points,
        smooth=True,
        fill=fill,
        outline=outline
    )