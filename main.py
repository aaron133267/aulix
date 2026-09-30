<<<<<<< HEAD
import asyncio
from datetime import datetime
from time import monotonic

from shiny import App, reactive, render, ui, req
from config import ROOT, SLOTS, TIMEZONE
from database import Store, get_engine
from ui.screens import badge, booking, catalog, heading, login_screen, shell

def today():
    return datetime.now(TIMEZONE).date()

def room_click(room_id):
    return f"Shiny.setInputValue('selected_room', {room_id}, {{priority: 'event'}})"

def alert(message, success=False):
    return ui.div(message, class_='message success' if success else 'message', role='status')

app_ui = ui.page_fluid(ui.tags.link(rel='stylesheet', href='styles.css'),
                       ui.output_ui('root'), title='Aulix · Reserva de salones', lang='es')

def server(input, output, session):
    user = reactive.value(None)
    current_page = reactive.value('rooms')
    rooms = reactive.value([])
    selected = reactive.value(None)
    revision = reactive.value(0)
    login_error = reactive.value('')
    booking_feedback = reactive.value(None)
    last_attempt = [0.0]

    def store():
        return Store(get_engine())

    @render.ui
    def root():
        return shell(user()) if user() else login_screen()

    @render.ui
    def login_message():
        return alert(login_error()) if login_error() else None

    @reactive.effect
    @reactive.event(input.login)
    async def login():
        if monotonic() - last_attempt[0] < 2:
            login_error.set('Espera un momento antes de volver a intentarlo.')
            return
        last_attempt[0] = monotonic()
        email, password = input.email().strip(), input.password()
        if '@' not in email or not password or len(email) > 254 or len(password) > 128:
            login_error.set('Introduce un correo válido y tu contraseña.')
            return
        try:
            db = store()
            account = await asyncio.to_thread(db.authenticate, email, password)
            if not account:
                login_error.set('Correo o contraseña incorrectos.')
                return
            available_rooms = await asyncio.to_thread(db.rooms)
            rooms.set(available_rooms)
            selected.set(available_rooms[0].id if available_rooms else None)
            current_page.set('rooms')
            login_error.set('')
            user.set(account)
        except Exception:
            login_error.set('No se pudo conectar. Revisa la configuración de Aiven, el certificado y la inicialización de las tablas.')

    @reactive.effect
    @reactive.event(input.logout)
    def logout():
        user.set(None)
        rooms.set([])
        selected.set(None)
        booking_feedback.set(None)

    @reactive.effect
    @reactive.event(input.nav_rooms)
    def nav_rooms():
        if user():
            current_page.set('rooms')

    @reactive.effect
    @reactive.event(input.nav_reservations)
    def nav_reservations():
        if user():
            current_page.set('reservations')

    @reactive.effect
    @reactive.event(input.selected_room)
    def select_room():
        if user() and input.selected_room() in [r.id for r in rooms()]:
            selected.set(input.selected_room())

    @reactive.effect
    @reactive.event(input.reserve_room)
    def open_booking():
        if user() and selected():
            booking_feedback.set(None)
            current_page.set('booking')

    @render.ui
    def page():
        req(user())
        if current_page() == 'booking':
            return booking(rooms(), selected(), today())
        if current_page() == 'reservations':
            return ui.div(heading('Mis reservas', 'Tus espacios y horarios confirmados.', 'Mis reservas'),
                          ui.output_ui('my_reservations'))
        return catalog()

    @render.ui
    def room_cards():
        req(user())
        req(current_page() == 'rooms')
        query = input.search().strip().casefold()
        filtered = [r for r in rooms() if query in f'{r.name} {r.code} {r.location}'.casefold()
                    and (input.status() == 'Todos' or r.status == input.status())]
        if input.order() == 'capacity':
            filtered.sort(key=lambda r: r.capacity, reverse=True)
        return ui.div(ui.p(f'Mostrando {len(filtered)} de {len(rooms())} salones', class_='muted count'),
            ui.div(*[ui.tags.button(
                ui.div(ui.span('⌂', class_='room-icon'), ui.span('Salón', class_='type-label'), class_='card-top'),
                ui.h3(r.name), ui.p('⌖ ' + r.location), ui.p(f'{r.capacity} estudiantes'),
                ui.div(badge(r.status), ui.tags.small('Seleccionado' if selected() == r.id else 'Ver detalles'), class_='card-bottom'),
                type='button', onclick=room_click(r.id),
                class_='room-card selected' if selected() == r.id else 'room-card',
                **{'aria-pressed': str(selected() == r.id).lower()}) for r in filtered], class_='room-grid')
            if filtered else ui.div('No hay salones que coincidan con tu búsqueda.', class_='panel'))

    @render.ui
    async def room_detail():
        req(user())
        req(current_page() == 'rooms')
        revision()
        room = next((r for r in rooms() if r.id == selected()), None)
        if not room:
            return ui.div('Selecciona un salón para ver los detalles.', class_='panel')
        try:
            occupied = await asyncio.to_thread(store().occupied, room.id, today())
        except Exception:
            return alert('No se pudo consultar la disponibilidad. Vuelve a seleccionar el salón.')
        return ui.tags.section(ui.div(badge(room.status), ui.tags.small(room.code), class_='card-top'),
            ui.h2(room.name), ui.p('UBICACIÓN', class_='detail-label'), ui.p(room.location),
            ui.p('CAPACIDAD / DETALLES', class_='detail-label'), ui.p(f'{room.capacity} estudiantes · {room.details}'),
            ui.hr(), ui.h3('Horarios para hoy'), ui.p(today().strftime('%d/%m/%Y'), class_='muted'),
            *[ui.div(ui.span('◷  ' + label), ui.tags.small('Ocupado' if key in occupied else
                ('No disponible' if room.status != 'Disponible' else 'Libre')),
                class_='slot-row ' + ('busy' if key in occupied or room.status != 'Disponible' else 'free')) for key, label in SLOTS.items()],
            ui.input_action_button('reserve_room', '✓ Reservar este salón', class_='btn-primary full', disabled=room.status != 'Disponible'),
            class_='panel detail-panel')

    @reactive.calc
    def chosen_room():
        req(user())
        req(current_page() == 'booking')
        return next((r for r in rooms() if str(r.id) == input.booking_room()), None)

    @render.ui
    def booking_detail():
        room = chosen_room()
        return ui.div(ui.h3(room.name), ui.p(f'{room.location} · {room.capacity} estudiantes'), badge(room.status), class_='room-summary') if room else None

    @render.ui
    async def booking_slots():
        revision()
        room, day = chosen_room(), input.booking_date()
        if not room or not day:
            return alert('Selecciona un salón y una fecha.')
        try:
            occupied = await asyncio.to_thread(store().occupied, room.id, day)
        except Exception:
            return alert('No se pudieron cargar los horarios. Cambia la fecha para reintentar.')
        now = datetime.now(TIMEZONE)
        choices = {key: label for key, label in SLOTS.items() if key not in occupied
                   and room.status == 'Disponible'
                   and datetime.combine(day, datetime.strptime(key, '%H:%M').time(), TIMEZONE) > now}
        return ui.div(ui.p('Disponibilidad para ' + day.strftime('%d/%m/%Y'), class_='muted'),
            *[ui.div(label, ui.tags.small('Ocupado' if key in occupied else 'No disponible'), class_='slot-row busy')
              for key, label in SLOTS.items() if key not in choices],
            ui.input_radio_buttons('slot', 'Horarios libres', choices, selected=next(iter(choices)))
            if choices else alert('No hay horarios disponibles para esta fecha.'))

    @render.ui
    def booking_summary():
        room = chosen_room()
        day = input.booking_date()
        slot = input.slot() if 'slot' in input else None
        return ui.div(ui.h3('✓ Resumen de tu reserva'), ui.tags.strong(room.name if room else 'Selecciona un salón'),
            ui.p(day.strftime('%d/%m/%Y') if day else 'Selecciona una fecha'),
            ui.p(SLOTS.get(slot, 'Selecciona un horario')), class_='reservation-summary')

    @reactive.effect
    @reactive.event(input.booking_room, input.booking_date)
    def clear_feedback():
        booking_feedback.set(None)
        ui.update_action_button('confirm', disabled=False)

    @reactive.effect
    @reactive.event(input.confirm)
    async def confirm():
        req(user())
        req(current_page() == 'booking')
        if booking_feedback() and booking_feedback()[1]:
            return
        room = chosen_room()
        if not room:
            return
        try:
            slot = input.slot() if 'slot' in input else None
            number = await asyncio.to_thread(store().reserve, user()['id'], room.id, input.booking_date(), slot)
            booking_feedback.set((f'Reserva #{number} confirmada. Puedes consultarla en Mis reservas.', True))
            ui.update_action_button('confirm', disabled=True)
            revision.set(revision() + 1)
        except ValueError as error:
            booking_feedback.set((str(error), False))
            revision.set(revision() + 1)
        except Exception:
            booking_feedback.set(('No se pudo verificar el resultado. Consulta Mis reservas antes de reintentar.', False))

    @render.ui
    def booking_message():
        result = booking_feedback()
        return alert(*result) if result else None

    @render.ui
    async def my_reservations():
        req(user())
        req(current_page() == 'reservations')
        revision()
        try:
            reservations = await asyncio.to_thread(store().reservations, user()['id'])
        except Exception:
            return alert('No se pudieron cargar tus reservas. Vuelve a entrar en esta sección.')
        if not reservations:
            return ui.tags.section(ui.h2('Tu próxima clase empieza aquí'), ui.p('Todavía no tienes reservas. Selecciona un salón para comenzar.'), class_='panel empty-state')
        return ui.div(*[ui.tags.section(ui.div(ui.h3(room.name), ui.span('✓ Confirmada', class_='badge-status available'), class_='card-top'),
            ui.p(room.location), ui.tags.strong(f'{reservation.day:%d/%m/%Y} · {SLOTS[reservation.slot]}'),
            ui.p(f'Reserva #{reservation.id}', class_='muted'), class_='panel') for reservation, room in reservations], class_='reservation-grid')

app = App(app_ui, server, static_assets=ROOT / 'www')

if __name__ == '__main__':
    app.run()
=======
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
>>>>>>> 6bf3e3849a767736c47c0980fc08951d3a1dba9f
