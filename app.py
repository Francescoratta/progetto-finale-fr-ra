from flask import Flask, render_template, request, redirect, url_for, jsonify
import os
import psycopg2
from psycopg2.extras import DictCursor  # Sostituisce sqlite3.Row per leggere i dati come dizionari
import requests
from dotenv import load_dotenv

# Carica variabili d'ambiente da .env.local (solo sviluppo locale)
load_dotenv('.env.local')

SUPABASE_URL = os.environ.get('SUPABASE_URL')
SUPABASE_KEY = os.environ.get('SUPABASE_SERVICE_ROLE_KEY') or os.environ.get('SUPABASE_API_KEY')

# Configurazione per Vercel: diciamo a Flask che i template e i file statici sono nella cartella corrente
app = Flask(__name__, template_folder='templates', static_folder='static')

def supabase_request(method, path, params=None, json_data=None):
    if not SUPABASE_URL or not SUPABASE_KEY:
        raise ValueError('SUPABASE_URL o SUPABASE_SERVICE_ROLE_KEY non configurati.')

    headers = {
        'apikey': SUPABASE_KEY,
        'Authorization': f'Bearer {SUPABASE_KEY}',
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    url = f"{SUPABASE_URL}/rest/v1/{path}"
    try:
        response = requests.request(method, url, headers=headers, params=params, json=json_data, timeout=20)
    except requests.RequestException as e:
        raise RuntimeError(f"Supabase network error: {e}") from e

    if not response.ok:
        raise RuntimeError(f"Supabase request failed: {response.status_code} {response.text}")
    return response


def get_db_connection():
    # Fallback: direct DB connection only if SUPABASE REST vars non configurati
    db_url = os.environ.get("DATABASE_URL")
    if not db_url:
        raise ValueError("DATABASE_URL non configurata. Controlla il file .env.local")
    try:
        from urllib.parse import urlparse, unquote
        import socket

        parsed = urlparse(db_url)
        username = unquote(parsed.username) if parsed.username else None
        password = unquote(parsed.password) if parsed.password else None
        host = parsed.hostname
        port = parsed.port or 5432
        dbname = parsed.path.lstrip('/') if parsed.path else None

        connect_host = host
        try:
            infos = socket.getaddrinfo(host, port, family=socket.AF_UNSPEC, type=socket.SOCK_STREAM)
            ipv4_addr = None
            ipv6_addr = None
            for info in infos:
                family, _, _, _, sockaddr = info
                if family == socket.AF_INET and not ipv4_addr:
                    ipv4_addr = sockaddr[0]
                if family == socket.AF_INET6 and not ipv6_addr:
                    ipv6_addr = sockaddr[0]
            if ipv4_addr:
                connect_host = ipv4_addr
            elif ipv6_addr:
                connect_host = ipv6_addr
        except Exception:
            connect_host = host

        conn = psycopg2.connect(
            host=connect_host,
            port=port,
            dbname=dbname,
            user=username,
            password=password,
            cursor_factory=DictCursor,
            sslmode='require'
        )
        return conn
    except Exception as e:
        import sys
        print(f"Errore connessione DB: {e}", file=sys.stderr)
        raise


def use_supabase_rest():
    return bool(SUPABASE_URL and SUPABASE_KEY)

@app.route('/health')
def health():
    """Health check: returns whether Supabase env vars are configured."""
    db_url = os.environ.get("DATABASE_URL")
    supabase_url = os.environ.get('SUPABASE_URL')
    supabase_key_set = bool(os.environ.get('SUPABASE_SERVICE_ROLE_KEY') or os.environ.get('SUPABASE_API_KEY'))

    return jsonify({
        'app': 'ok',
        'database_url_set': bool(db_url),
        'database_host': None,
        'supabase_url_set': bool(supabase_url),
        'supabase_key_set': supabase_key_set,
        'use_supabase_rest': bool(supabase_url and supabase_key_set),
        'supabase_url': supabase_url
    })

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/campioni')
def roles():
    return render_template('roles.html')

@app.route('/campioni/<role>')
def champions_by_role(role):
    try:
        if use_supabase_rest():
            params = {
                'select': '*',
                'role': f'eq.{role}'
            }
            response = supabase_request('GET', 'champions', params=params)
            champions = response.json()
        else:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute('SELECT * FROM champions WHERE role = %s', (role,))
            champions = cur.fetchall()
            cur.close()
            conn.close()

        return render_template('champions.html', champions=champions, role=role)
    except Exception as e:
        import traceback
        return jsonify(
            error=str(e),
            traceback=traceback.format_exc()
        ), 500

@app.route('/campione/<int:id>')
def champion_detail(id):
    try:
        if use_supabase_rest():
            params = {
                'select': '*',
                'id': f'eq.{id}'
            }
            response = supabase_request('GET', 'champions', params=params)
            results = response.json()
            champion = results[0] if results else None
        else:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute('SELECT * FROM champions WHERE id = %s', (id,))
            champion = cur.fetchone()
            cur.close()
            conn.close()

        return render_template('champion_detail.html', champion=champion)
    except Exception as e:
        import traceback
        return jsonify(
            error=str(e),
            traceback=traceback.format_exc()
        ), 500

@app.route('/aggiungi', methods=('GET', 'POST'))
def add_champion():
    if request.method == 'POST':
        name = request.form['name']
        role = request.form['role']
        lore = request.form['lore']
        difficulty = request.form['difficulty']
        image_vertical = request.form['image_vertical']
        image_horizontal = request.form['image_horizontal']

        if use_supabase_rest():
            data = {
                'name': name,
                'role': role,
                'lore': lore,
                'difficulty': difficulty,
                'image_vertical': image_vertical,
                'image_horizontal': image_horizontal,
                'is_custom': True
            }
            supabase_request('POST', 'champions', json_data=data)
        else:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute(
                'INSERT INTO champions (name, role, lore, difficulty, image_vertical, image_horizontal, is_custom) VALUES (%s, %s, %s, %s, %s, %s, 1)',
                (name, role, lore, difficulty, image_vertical, image_horizontal)
            )
            conn.commit()
            cur.close()
            conn.close()

        return redirect(url_for('champions_by_role', role=role)) 

    return render_template('add_champion.html')


@app.route('/elimina/<int:id>', methods=('POST',))
def delete_champion(id):
    if use_supabase_rest():
        # Fetch role first so we can redirect back to the correct lane
        params = {
            'select': 'role',
            'id': f'eq.{id}'
        }
        response = supabase_request('GET', 'champions', params=params)
        results = response.json()
        role = results[0]['role'] if results else None

        supabase_request('DELETE', 'champions', params={'id': f'eq.{id}'})
        if role:
            return redirect(url_for('champions_by_role', role=role))
        return redirect(url_for('roles'))

    conn = get_db_connection()
    cur = conn.cursor()
    
    # Cambiato ? con %s
    cur.execute('SELECT role FROM champions WHERE id = %s', (id,))
    champion = cur.fetchone()
    
    if champion:
        role = champion['role']
        # Cambiato ? con %s
        cur.execute('DELETE FROM champions WHERE id = %s', (id,))
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for('champions_by_role', role=role))
    
    cur.close()
    conn.close()
    return redirect(url_for('roles'))

# Vercel non richiede app.run(), ma lo lasciamo per i tuoi test locali se imposti la variabile d'ambiente sul PC
if __name__ == '__main__':
    app.run(debug=True)