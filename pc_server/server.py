"""SS OIL read-only LAN API. SQL Server 2005; requires pyodbc and an ODBC driver.
No SQL modifications; credentials are read from environment variables.
"""
import json
import os
from decimal import Decimal
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import unquote

try:
    import pyodbc
except ImportError:
    raise SystemExit('Install pyodbc and an SQL Server-compatible ODBC driver')

HOST = os.getenv('SSOIL_HOST', '0.0.0.0')
PORT = int(os.getenv('SSOIL_PORT', '8765'))
TOKEN = os.environ['SSOIL_API_TOKEN']
ODBC = os.environ['SSOIL_ODBC_CONNECTION']

# The sales table's quantities are aggregated once per product, as requested.
# Confirm that SmP_S contains only the sales NOT already reflected in ART.Kolicina.
PRODUCT_SQL = '''SELECT Art_ID, Naziv, PCena, Kolicina FROM dbo.ART'''
BARCODE_SQL = '''SELECT Art_ID, BKod_ID FROM dbo.ART_BK'''
SALE_SQL = '''SELECT Art_ID, SUM(Kolicina) FROM dbo.SmP_S GROUP BY Art_ID'''
ONE_SQL = '''SELECT Art_ID, PCena, Kolicina FROM dbo.ART WHERE Art_ID = ?'''
ONE_SALES_SQL = '''SELECT COALESCE(SUM(Kolicina), 0) FROM dbo.SmP_S WHERE Art_ID = ?'''


def conn():
    # Explicit read-only connection intent. The SQL login MUST also have SELECT-only grants.
    return pyodbc.connect(ODBC, autocommit=True, timeout=10)


def val(value):
    if isinstance(value, Decimal):
        return str(value)
    return value


def snapshot():
    with conn() as db:
        cur = db.cursor()
        rows = cur.execute(PRODUCT_SQL).fetchall()
        products = {str(r[0]): {'id': str(r[0]), 'name': str(r[1] or ''),
                   'price': str(r[2] or 0), 'stock': str(r[3] or 0), 'barcodes': []}
                   for r in rows}
        for art_id, barcode in cur.execute(BARCODE_SQL).fetchall():
            if str(art_id) in products and barcode is not None:
                b = str(barcode).strip()
                if b and b not in products[str(art_id)]['barcodes']:
                    products[str(art_id)]['barcodes'].append(b)
    return {'products': list(products.values())}


def product(art_id):
    with conn() as db:
        cur = db.cursor()
        row = cur.execute(ONE_SQL, (art_id,)).fetchone()
        if row is None:
            return None
        sold = cur.execute(ONE_SALES_SQL, (art_id,)).fetchone()[0] or 0
        net = Decimal(str(row[3] or 0)) - Decimal(str(sold))
        return {'id': str(row[0]), 'price': str(row[1] or 0),
                'stock': str(net), 'art_stock': str(row[3] or 0), 'sales': str(sold)}


class Handler(BaseHTTPRequestHandler):
    def respond(self, status, data):
        payload = json.dumps(data, ensure_ascii=False, default=val).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(payload)))
        self.send_header('Cache-Control', 'no-store')
        self.end_headers()
        self.wfile.write(payload)

    def do_GET(self):
        if self.headers.get('X-SSOIL-Token', '') != TOKEN:
            return self.respond(401, {'error': 'unauthorized'})
        try:
            if self.path == '/snapshot':
                return self.respond(200, snapshot())
            if self.path.startswith('/product/'):
                art_id = unquote(self.path[len('/product/'):])
                if not art_id.isdigit():
                    return self.respond(400, {'error': 'invalid product id'})
                result = product(art_id)
                return self.respond(200, result) if result else self.respond(404, {'error': 'not found'})
            return self.respond(404, {'error': 'not found'})
        except Exception:
            self.log_error('Database query failed')
            return self.respond(503, {'error': 'database unavailable or schema mismatch'})

    def do_POST(self):
        return self.respond(405, {'error': 'read only'})


if __name__ == '__main__':
    ThreadingHTTPServer((HOST, PORT), Handler).serve_forever()
