"""Persistencia MySQL; crear tablas y cuentas es una operación explícita."""
import os
import ssl
from datetime import date, datetime
from functools import lru_cache
from argon2 import PasswordHasher
from argon2.exceptions import VerificationError, InvalidHashError
from sqlalchemy import Date, ForeignKey, String, UniqueConstraint, create_engine, select
from sqlalchemy.engine import URL
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column
from config import ROOT, SLOTS, TIMEZONE

hasher = PasswordHasher()
DUMMY_HASH = hasher.hash('unused-timing-placeholder')

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(254), unique=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    name: Mapped[str] = mapped_column(String(120))
    role: Mapped[str] = mapped_column(String(30), default='docente')

class Room(Base):
    __tablename__ = 'rooms'
    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(String(30), unique=True)
    name: Mapped[str] = mapped_column(String(100))
    location: Mapped[str] = mapped_column(String(160))
    capacity: Mapped[int]
    details: Mapped[str] = mapped_column(String(255))
    status: Mapped[str] = mapped_column(String(30), default='Disponible')

class Reservation(Base):
    __tablename__ = 'reservations'
    __table_args__ = (UniqueConstraint('room_id', 'day', 'slot', name='uq_room_day_slot'),)
    id: Mapped[int] = mapped_column(primary_key=True)
    room_id: Mapped[int] = mapped_column(ForeignKey('rooms.id'))
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    day: Mapped[date] = mapped_column(Date)
    slot: Mapped[str] = mapped_column(String(5))

@lru_cache
def get_engine():
    required = ['MYSQL_HOST', 'MYSQL_PORT', 'MYSQL_DATABASE', 'MYSQL_USER', 'MYSQL_PASSWORD', 'MYSQL_SSL_CA']
    if any(not os.getenv(key) for key in required):
        raise ValueError('Configura la conexión a Aiven en .env siguiendo .env.example.')
    context = ssl.create_default_context(cafile=str(ROOT / os.environ['MYSQL_SSL_CA']))
    url = URL.create('mysql+pymysql', username=os.environ['MYSQL_USER'],
                     password=os.environ['MYSQL_PASSWORD'], host=os.environ['MYSQL_HOST'],
                     port=int(os.environ['MYSQL_PORT']), database=os.environ['MYSQL_DATABASE'],
                     query={'charset': 'utf8mb4'})
    return create_engine(url, connect_args={'ssl': context, 'connect_timeout': 8,
                         'read_timeout': 10, 'write_timeout': 10}, pool_size=5,
                         max_overflow=0, pool_pre_ping=True, pool_recycle=300)

class Store:
    def __init__(self, engine):
        self.engine = engine

    def authenticate(self, email, password):
        with Session(self.engine) as session:
            user = session.scalar(select(User).where(User.email == email.strip().lower()))
            try:
                hasher.verify(user.password_hash if user else DUMMY_HASH, password)
            except (VerificationError, InvalidHashError):
                return None
            return {'id': user.id, 'name': user.name, 'role': user.role} if user else None

    def rooms(self):
        with Session(self.engine) as session:
            return list(session.scalars(select(Room).order_by(Room.name)))

    def occupied(self, room_id, day):
        with Session(self.engine) as session:
            return set(session.scalars(select(Reservation.slot).where(
                Reservation.room_id == room_id, Reservation.day == day)))

    def reserve(self, user_id, room_id, day, slot):
        if slot not in SLOTS or not isinstance(day, date):
            raise ValueError('Selecciona una fecha y un horario válidos.')
        start = datetime.combine(day, datetime.strptime(slot, '%H:%M').time(), TIMEZONE)
        if start <= datetime.now(TIMEZONE):
            raise ValueError('No puedes reservar un horario que ya pasó.')
        try:
            with Session(self.engine) as session, session.begin():
                room = session.get(Room, room_id)
                if not room or room.status != 'Disponible':
                    raise ValueError('Este salón no está disponible para reservar.')
                if not session.get(User, user_id):
                    raise ValueError('Inicia sesión de nuevo.')
                reservation = Reservation(user_id=user_id, room_id=room_id, day=day, slot=slot)
                session.add(reservation)
                session.flush()
                reservation_id = reservation.id
            return reservation_id
        except IntegrityError as error:
            raise ValueError('Ese horario acaba de ser reservado. Elige otro horario.') from error

    def reservations(self, user_id):
        with Session(self.engine) as session:
            return list(session.execute(select(Reservation, Room).join(Room).where(
                Reservation.user_id == user_id).order_by(Reservation.day.desc(), Reservation.slot)))
