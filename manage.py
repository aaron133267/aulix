import argparse
from getpass import getpass
from sqlalchemy import select
from sqlalchemy.orm import Session
from database import Base, Room, User, get_engine, hasher

def main():
    parser = argparse.ArgumentParser(description='Configuración inicial de Aulix')
    parser.add_argument('command', choices=['init-db', 'create-user'])
    args = parser.parse_args()
    engine = get_engine()
    if args.command == 'init-db':
        Base.metadata.create_all(engine)
        with Session(engine) as session, session.begin():
            for i, (name, location, capacity, status) in enumerate([
                ('Salón 201-A', 'Edificio Central, planta 1', 32, 'Disponible'),
                ('Salón 202-A', 'Edificio Central, planta 1', 28, 'Disponible'),
                ('Salón 301-B', 'Edificio B, planta 2', 40, 'Disponible'),
                ('Salón 302-B', 'Edificio B, planta 2', 35, 'Mantenimiento'),
                ('Salón 101-C', 'Edificio C, planta baja', 24, 'Disponible'),
                ('Salón 102-C', 'Edificio C, planta baja', 30, 'Mantenimiento'),
            ], start=1):
                code = f'SAL-{i:03}'
                if not session.scalar(select(Room).where(Room.code == code)):
                    session.add(Room(code=code, name=name, location=location,
                                     capacity=capacity, status=status,
                                     details='Pizarrón, mesas y sillas para estudiantes'))
        print('Tablas creadas y salones de ejemplo cargados sin duplicar existentes.')
    else:
        email = input('Correo: ').strip().lower()
        name = input('Nombre: ').strip()
        role = input('Rol (docente/administrador) [docente]: ').strip() or 'docente'
        password = getpass('Contraseña (12 a 128 caracteres): ')
        if '@' not in email or len(email) > 254 or not name or len(name) > 120:
            raise SystemExit('Correo o nombre inválido.')
        if role not in ('docente', 'administrador') or not 12 <= len(password) <= 128:
            raise SystemExit('Rol o longitud de contraseña inválidos.')
        if password != getpass('Repite la contraseña: '):
            raise SystemExit('Las contraseñas no coinciden.')
        with Session(engine) as session, session.begin():
            if session.scalar(select(User).where(User.email == email)):
                raise SystemExit('Ya existe una cuenta con ese correo.')
            session.add(User(email=email, name=name, role=role, password_hash=hasher.hash(password)))
        print('Cuenta creada.')

if __name__ == '__main__':
    main()
