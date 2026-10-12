from http.server import ThreadingHTTPServer
import json
import threading
import unittest
from unittest.mock import patch
from urllib.error import HTTPError
from urllib.request import Request, urlopen

from tutor_virtual.app import Handler


class ServerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = ThreadingHTTPServer(('127.0.0.1', 0), Handler)
        cls.base = f'http://127.0.0.1:{cls.server.server_port}'
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join()

    def request(self, path, payload=None, origin=None):
        headers = {}
        body = None
        if payload is not None:
            body = json.dumps(payload).encode()
            headers = {'Content-Type': 'application/json', 'Origin': origin or self.base}
        try:
            return urlopen(Request(self.base + path, body, headers), timeout=5)
        except HTTPError as error:
            return error

    def test_assets(self):
        for path in ['/', '/style.css', '/app.js']:
            with self.request(path) as response:
                self.assertEqual(response.status, 200)
                self.assertTrue(response.read())
                self.assertIn("default-src 'self'", response.headers['Content-Security-Policy'])

    def test_private_files_not_served(self):
        for path in ['/.env', '/../.env', '/tutor.py']:
            with self.request(path) as response:
                self.assertEqual(response.code, 404)

    def test_external_origin_rejected(self):
        with patch('tutor_virtual.app.answer') as backend:
            with self.request('/api/ask', {'message': 'Hola'}, 'https://otro-sitio.example') as response:
                self.assertEqual(response.code, 403)
            backend.assert_not_called()

    def test_answer_route(self):
        with patch('tutor_virtual.app.answer', return_value='Explicación de prueba'):
            with self.request('/api/ask', {'message': 'Hola'}) as response:
                self.assertEqual(response.status, 200)
                self.assertEqual(json.load(response)['answer'], 'Explicación de prueba')


if __name__ == '__main__':
    unittest.main()
