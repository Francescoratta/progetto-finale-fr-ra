League of Legends Champions Database

Un'applicazione web per esplorare e gestire i campioni di League of Legends.

Descrizione

**LoL Database** è un sito interattivo dove puoi:
- Visualizzare i campioni per ruolo (Top, Jungle, Mid, Bot, Support)
- Leggere la storia (lore) di ogni campione
- Aggiungere campioni personalizzati
- Eliminare campioni custom

L'app è costruita con Flask e utilizza un database PostgreSQL su Supabase, con API REST per l'accesso ai dati.

Tecnologie Utilizzate

- **Backend**: Flask (Python)
- **Database**: PostgreSQL (Supabase)
- **API**: Supabase REST API
- **Deploy**: Vercel
- **Frontend**: HTML, CSS, Jinja2 templates
- **Librerie Python**:
  - Flask 3.0.2
  - psycopg2-binary 2.9.9
  - requests 2.31.0
  - python-dotenv 1.0.0

Installazione Locale

Prerequisiti
- Python 3.11+
- pip
- Git

Setup

1. **Clona il repository**
```bash
git clone https://github.com/Francescoratta/progetto-finale-fr-ra.git
cd progetto-finale-fr-ra
```

2. **Crea un ambiente virtuale**
```bash
python -m venv venv
source venv/bin/activate  # su Windows: venv\Scripts\activate
```

3. **Installa le dipendenze**
```bash
pip install -r requirements.txt
```

4. **Configura le variabili d'ambiente**
Crea un file `.env.local`:
```
DATABASE_URL=postgresql://user:password@host/dbname
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key
```

5. **Popola il database (se necessario)**
```bash
python seed_supabase.py
```

6. **Avvia l'app**
```bash
python app.py
```
Visita: http://localhost:5000


Sito Pubblicato

**[LoL Database - Visita il sito](https://progetto-finale-fr-ra-ka5a.vercel.app)**

Struttura del Progetto

```
.
├── app.py                 # App Flask principale
├── seed_supabase.py       # Script per popolare il database
├── init_db.py             # Dati dei campioni
├── requirements.txt       # Dipendenze Python
├── vercel.json            # Configurazione Vercel
├── schema.sql             # Schema del database
├── templates/             # Template HTML
│   ├── base.html
│   ├── index.html
│   ├── roles.html
│   ├── champions.html
│   ├── champion_detail.html
│   └── add_champion.html
└── static/                # CSS e assets
    └── style.css
```

Rotte API

| Rotta | Metodo | Descrizione |
|-------|--------|-------------|
| `/` | GET | Pagina principale |
| `/campioni` | GET | Lista dei ruoli |
| `/campioni/<role>` | GET | Campioni per ruolo |
| `/campione/<id>` | GET | Dettagli campione |
| `/aggiungi` | GET, POST | Aggiungi campione |
| `/elimina/<id>` | POST | Elimina campione |
| `/health` | GET | Health check (debug) |
