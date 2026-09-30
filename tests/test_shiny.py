"""Exercise real Shiny websocket outputs using an isolated test database."""
import json
import socket
import threading
import time
import unittest
from unittest.mock import patch

import uvicorn
from websockets.sync.client import connect

import main
import test_database


class ShinyFlowTests(unittest.TestCase):
    def test_login_catalog_booking_and_logout(self):
        fixture = test_database.ReservationTests()
        fixture.setUp()
        listener = socket.socket()
        listener.bind(('127.0.0.1', 0))
        port = listener.getsockname()[1]
        server = uvicorn.Server(uvicorn.Config(main.app, log_level='error'))
        worker = threading.Thread(target=server.run, kwargs={'sockets': [listener]}, daemon=True)
        try:
            with patch.object(main, 'get_engine', return_value=fixture.engine):
                worker.start()
                deadline = time.monotonic() + 10
                while not server.started and time.monotonic() < deadline:
                    time.sleep(.05)
                self.assertTrue(server.started)
                with connect(f'ws://127.0.0.1:{port}/websocket/', proxy=None) as ws:
                    def update(data, method='update'):
                        actions = {'login', 'logout', 'nav_rooms', 'nav_reservations', 'reserve_room', 'confirm'}
                        data = {(key + ':shiny.action' if key in actions else key): value for key, value in data.items()}
                        ws.send(json.dumps({'method': method, 'data': data}))

                    def expect(output, text):
                        deadline = time.monotonic() + 8
                        seen = []
                        while time.monotonic() < deadline:
                            try:
                                message = json.loads(ws.recv(timeout=8))
                            except TimeoutError:
                                self.fail(f'Missing {output}: {seen}')
                            errors = {k: v for k, v in message.get('errors', {}).items() if v.get('message')}
                            self.assertFalse(errors, errors)
                            seen.append(message)
                            value = message.get('values', {}).get(output)
                            if value is not None and text in str(value):
                                return
                        self.fail(f'No output {output}: {seen}')

                    outputs = ['root', 'page', 'login_message', 'room_cards', 'room_detail',
                               'booking_detail', 'booking_slots', 'booking_summary', 'booking_message', 'my_reservations']
                    data = {f'.clientdata_output_{name}_hidden': False for name in outputs}
                    data.update({'email': '', 'password': '', 'login': 0, 'logout': 0,
                                 'nav_rooms': 0, 'nav_reservations': 0, 'reserve_room': 0,
                                 'confirm': 0, 'search': '', 'status': 'Todos', 'order': 'az'})
                    update(data, 'init')
                    expect('root', 'Bienvenido de nuevo')
                    update({'email': 'docente@escuela.edu', 'password': 'test-password-123', 'login': 1})
                    expect('root', 'Mis reservas')
                    update({'search': 'Salón A'})
                    expect('room_cards', 'Salón A')
                    update({'reserve_room': 1})
                    expect('page', 'Crear reserva')
                    update({'booking_room': '1', 'booking_date:shiny.date': fixture.day.isoformat()})
                    expect('booking_slots', '07:00')
                    update({'slot': '07:00'})
                    expect('booking_summary', '07:00')
                    update({'confirm': 1})
                    expect('booking_message', 'confirmada')
                    update({'nav_reservations': 1})
                    expect('my_reservations', 'Salón A')
                    update({'logout': 1})
                    expect('root', 'Bienvenido de nuevo')
                    self.assertEqual(len(fixture.store.reservations(1)), 1)
        finally:
            server.should_exit = True
            worker.join(timeout=10)
            listener.close()
            fixture.tearDown()
