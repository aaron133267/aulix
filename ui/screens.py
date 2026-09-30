from shiny import ui

def logo():
    return ui.div(ui.span(ui.tags.i(), ui.tags.i(), ui.tags.i(), class_='logo-icon'), 'Aulix', class_='brand')

def badge(status):
    return ui.span('● ' + status, class_='badge-status ' + ('available' if status == 'Disponible' else 'maintenance'))

def login_screen():
    return ui.div(
        ui.tags.section(
            ui.p('✦  GESTIÓN EDUCATIVA INTELIGENTE', class_='eyebrow'),
            ui.div(ui.h1('El espacio para tus próximas ideas.'),
                   ui.p('Consulta y reserva los salones de tu institución en un solo lugar. Fácil, organizado y a tu tiempo.'), class_='hero-copy'),
            ui.div(ui.div(ui.tags.strong('01'), ui.span('Encuentra tu salón')),
                   ui.div(ui.tags.strong('02'), ui.span('Elige un horario')),
                   ui.div(ui.tags.strong('03'), ui.span('Confirma tu reserva')), class_='hero-steps'),
            ui.tags.small('Aulix · Espacios que hacen posible aprender'), class_='login-hero'),
        ui.tags.section(logo(), ui.div(ui.h2('Bienvenido de nuevo'),
            ui.p('Inicia sesión para gestionar tus reservas.', class_='muted'),
            ui.input_text('email', 'Correo electrónico', placeholder='nombre@institucion.edu'),
            ui.input_password('password', 'Contraseña'),
            ui.input_action_button('login', 'Iniciar sesión →', class_='btn-primary full'),
            ui.output_ui('login_message'), class_='login-form'),
            ui.tags.small('¿Necesitas una cuenta? Contacta al administrador de tu institución.', class_='muted'),
            class_='login-side'), class_='login-layout')

def shell(user):
    return ui.div(
        ui.tags.header(logo(), ui.div(
            ui.input_action_button('nav_rooms', 'Salones', class_='nav-button'),
            ui.input_action_button('nav_reservations', 'Mis reservas', class_='nav-button'), class_='nav-links'),
            ui.div(ui.div(ui.tags.strong(user['name']), ui.tags.small(user['role'].capitalize())),
                   ui.input_action_button('logout', 'Salir', class_='nav-button'), class_='profile'), class_='topbar'),
        ui.tags.main(ui.output_ui('page'), class_='workspace'))

def heading(title, subtitle, crumb):
    return ui.div(ui.p('Inicio  ›  ' + crumb, class_='breadcrumb-text'),
                  ui.h1(title), ui.p(subtitle, class_='muted'), class_='page-heading')

def catalog():
    return ui.div(heading('Consultar salones', 'Encuentra el espacio ideal para tu próxima clase.', 'Salones'),
        ui.div(ui.input_text('search', None, placeholder='Buscar por nombre, código o ubicación…'),
               ui.input_select('status', 'Estado', {'Todos': 'Todos', 'Disponible': 'Disponible', 'Mantenimiento': 'Mantenimiento'}),
               ui.input_select('order', 'Ordenar', {'az': 'Nombre A–Z', 'capacity': 'Mayor capacidad'}), class_='filter-bar'),
        ui.div(ui.tags.section(ui.output_ui('room_cards')), ui.tags.aside(ui.output_ui('room_detail')), class_='catalog-layout'))

def booking(rooms, selected, today):
    return ui.div(heading('Crear reserva', 'Selecciona un salón, una fecha y un horario para tu reserva.', 'Reservas  ›  Crear reserva'),
        ui.div(ui.div(
            ui.tags.section(ui.h3(ui.span('1', class_='step'), 'Seleccionar salón'),
                ui.input_select('booking_room', 'Salón o espacio académico', {str(r.id): r.name for r in rooms}, selected=str(selected)),
                ui.output_ui('booking_detail'), class_='panel'),
            ui.tags.section(ui.h3(ui.span('2', class_='step'), 'Seleccionar fecha'),
                ui.input_date('booking_date', 'Fecha de la reserva', value=today, min=today, language='es', weekstart=1),
                ui.p('Horarios escolares de 07:00 a 16:00, en bloques de 90 minutos.', class_='muted'), class_='panel'),
            ), ui.div(
                ui.tags.section(ui.h3(ui.span('3', class_='step'), 'Seleccionar horario'), ui.output_ui('booking_slots'), class_='panel'),
                ui.tags.section(ui.output_ui('booking_summary'),
                    ui.input_action_button('confirm', '✓ Confirmar reserva', class_='btn-primary full'),
                    ui.output_ui('booking_message'),
                    ui.p('Tu reserva se confirma directamente al guardarse.', class_='footnote'), class_='panel'),
            ), class_='booking-layout'))
