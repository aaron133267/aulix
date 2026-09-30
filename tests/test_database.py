import unittest
from concurrent.futures import ThreadPoolExecutor
from datetime import timedelta
from tempfile import TemporaryDirectory
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from config import TIMEZONE
from datetime import datetime
from database import Base, Room, User, Store, hasher

class ReservationTests(unittest.TestCase):
    def setUp(self):
        self.directory = TemporaryDirectory()
        self.engine = create_engine('sqlite:///' + str(Path(self.directory.name) / 'test.db'))
        Base.metadata.create_all(self.engine)
        with Session(self.engine) as session, session.begin():
            session.add_all([
                User(id=1, email='docente@escuela.edu', name='Docente', password_hash=hasher.hash('test-password-123')),
                User(id=2, email='otra@escuela.edu', name='Otra', password_hash=hasher.hash('other-password-123')),
                Room(id=1, code='A', name='Salón A', location='Central', capacity=30, details='Pizarrón', status='Disponible'),
                Room(id=2, code='B', name='Salón B', location='Central', capacity=30, details='Pizarrón', status='Mantenimiento'),
            ])
        self.store = Store(self.engine)
        self.day = datetime.now(TIMEZONE).date() + timedelta(days=1)

    def tearDown(self):
        self.engine.dispose()
        self.directory.cleanup()

    def test_authentication(self):
        self.assertEqual(self.store.authenticate(' DOCENTE@ESCUELA.EDU ', 'test-password-123')['id'], 1)
        self.assertIsNone(self.store.authenticate('docente@escuela.edu', 'wrong'))
        self.assertIsNone(self.store.authenticate('missing@escuela.edu', 'wrong'))

    def test_duplicate_and_own_reservations(self):
        self.store.reserve(1, 1, self.day, '07:00')
        with self.assertRaises(ValueError):
            self.store.reserve(2, 1, self.day, '07:00')
        self.assertEqual(self.store.occupied(1, self.day), {'07:00'})
        self.assertEqual(len(self.store.reservations(1)), 1)
        self.assertEqual(len(self.store.reservations(2)), 0)
        self.store.reserve(2, 1, self.day, '08:30')
        self.store.reserve(2, 1, self.day + timedelta(days=1), '07:00')

    def test_invalid_reservations(self):
        for user, room, day, slot in [(1,2,self.day,'07:00'), (1,1,self.day,'03:00'),
            (1,1,self.day-timedelta(days=2),'07:00'), (99,1,self.day,'07:00'), (1,99,self.day,'07:00')]:
            with self.subTest(room=room, day=day, slot=slot), self.assertRaises(ValueError):
                self.store.reserve(user, room, day, slot)
        self.assertEqual(self.store.reservations(1), [])

    def test_simultaneous_confirmation(self):
        def reserve(user):
            try:
                self.store.reserve(user, 1, self.day, '10:00')
                return True
            except ValueError:
                return False
        with ThreadPoolExecutor(max_workers=2) as executor:
            results = list(executor.map(reserve, [1, 2]))
        self.assertEqual(sorted(results), [False, True])

if __name__ == '__main__':
    unittest.main()
