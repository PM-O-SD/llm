"""Servidor local y punto de entrada: python -m tutor_virtual.app."""
import argparse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
from urllib.parse import urlparse

from .tutor import TutorError, answer

ROOT = Path(__file__).resolve().parent
FILES = {'/': ('index.html', 'text/html'), '/app.js': ('app.js', 'text/javascript'), '/style.css': ('style.css', 'text/css')}


class Handler(BaseHTTPRequestHandler):
    def send(self, status, body, content_type='application/json'):
        data = body if isinstance(body, bytes) else json.dumps(body, ensure_ascii=False).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', content_type + '; charset=utf-8')
        self.send_header('Content-Length', str(len(data)))
        self.send_header('Cache-Control', 'no-store')
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.send_header('Content-Security-Policy', "default-src 'self'; script-src 'self'; style-src 'self'; connect-src 'self'; object-src 'none'; frame-ancestors 'none'")
        self.end_headers()
        self.wfile.write(data)

    def allowed_host(self):
        return self.headers.get('Host') in (f'127.0.0.1:{self.server.server_port}', f'localhost:{self.server.server_port}')

    def do_GET(self):
        if not self.allowed_host():
            self.send(403, {'error': 'Acceso local requerido.'})
            return
        resource = FILES.get(urlparse(self.path).path)
        if not resource:
            self.send(404, {'error': 'Página no encontrada.'})
            return
        filename, mime = resource
        self.send(200, (ROOT / 'static' / filename).read_bytes(), mime)

    def do_POST(self):
        if not self.allowed_host() or self.headers.get('Origin') not in (
            f'http://127.0.0.1:{self.server.server_port}', f'http://localhost:{self.server.server_port}',
        ):
            self.send(403, {'error': 'Envía la consulta desde la página del tutor.'})
            return
        if self.path != '/api/ask':
            self.send(404, {'error': 'Ruta no encontrada.'})
            return
        if self.headers.get_content_type() != 'application/json':
            self.send(415, {'error': 'Formato de consulta inválido.'})
            return
        try:
            length = int(self.headers.get('Content-Length', '0'))
            if length <= 0 or length > 150000:
                self.send(413, {'error': 'La consulta excede el tamaño permitido.'})
                return
            payload = json.loads(self.rfile.read(length))
        except (ValueError, UnicodeError):
            self.send(400, {'error': 'No se pudo leer la consulta.'})
            return
        try:
            text = answer(payload)
        except TutorError as exc:
            self.send(400, {'error': str(exc)})
            return
        self.send(200, {'answer': text})

    def log_message(self, format, *args):
        # No se registran conversaciones ni credenciales.
        return


def main():
    from dotenv import load_dotenv
    load_dotenv(ROOT.parent / '.env')
    parser = argparse.ArgumentParser(description='Tutor virtual de IA')
    parser.add_argument('--port', type=int, default=8000)
    args = parser.parse_args()
    try:
        server = ThreadingHTTPServer(('127.0.0.1', args.port), Handler)
    except OSError:
        parser.exit(1, 'No se pudo abrir el puerto. Prueba --port 8001.\n')
    print(f'Abre http://127.0.0.1:{server.server_port} en tu navegador. Ctrl+C para cerrar.', flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == '__main__':
    main()
