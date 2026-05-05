"""
presence.py  –  sledování přihlášených uživatelů
Použití: import presence; presence.init(); presence.sidebar_widget()
"""

import sqlite3
import time
from datetime import datetime
from pathlib import Path

import streamlit as st

DB_PATH   = Path("presence.db")
HEARTBEAT = 15   # sekund – jak často se aktualizuje timestamp
TIMEOUT   = 30   # sekund – po kolika sekundách bez heartbeatu se uživatel odhlásí

# Mapování indexu záložky na název
TAB_NAMES = {
    0: "🔍 Extrakce",
    1: "🌐 Překlad",
    2: "🧬 Validace",
    3: "💬 Chat",
    4: "🧹 Čištění dat",
    5: "✍️ Stylistika",
    6: "⚙️ Workflow",
    7: "📜 Historie",
    8: "❓ Nápověda",
}


# ── DB ────────────────────────────────────────────────────────────────────────

def _conn():
    return sqlite3.connect(str(DB_PATH), check_same_thread=False, timeout=5)

def _init_db():
    with _conn() as c:
        c.execute("""
            CREATE TABLE IF NOT EXISTS presence (
                session_id TEXT PRIMARY KEY,
                name       TEXT,
                tab        TEXT,
                tab_idx    INTEGER DEFAULT 0,
                last_seen  REAL,
                task_start REAL
            )
        """)
        c.execute("""
            CREATE TABLE IF NOT EXISTS queue (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT,
                name       TEXT,
                created_at REAL,
                started_at REAL,
                status     TEXT DEFAULT 'waiting'
            )
        """)

def _now():
    return time.time()

def _active_users():
    cutoff = _now() - TIMEOUT
    with _conn() as c:
        return c.execute(
            "SELECT session_id, name, tab, tab_idx, last_seen "
            "FROM presence WHERE last_seen > ? ORDER BY last_seen",
            (cutoff,)
        ).fetchall()

def _heartbeat(session_id, name, tab, tab_idx):
    with _conn() as c:
        c.execute("""
            INSERT INTO presence (session_id, name, tab, tab_idx, last_seen, task_start)
            VALUES (?,?,?,?,?,?)
            ON CONFLICT(session_id) DO UPDATE SET
                name=excluded.name,
                tab=excluded.tab,
                tab_idx=excluded.tab_idx,
                last_seen=excluded.last_seen
        """, (session_id, name, tab, tab_idx, _now(), _now()))

def _remove_user(session_id):
    with _conn() as c:
        c.execute("DELETE FROM presence WHERE session_id=?", (session_id,))
        c.execute("DELETE FROM queue WHERE session_id=? AND status='waiting'", (session_id,))


# ── Fronta LLM ────────────────────────────────────────────────────────────────

def queue_add(session_id: str, name: str) -> int:
    """Přidá úlohu do fronty. Vrátí ID úlohy."""
    with _conn() as c:
        cur = c.execute(
            "INSERT INTO queue (session_id, name, created_at, status) VALUES (?,?,?,'waiting')",
            (session_id, name, _now())
        )
        return cur.lastrowid

def queue_start(job_id: int):
    with _conn() as c:
        c.execute("UPDATE queue SET status='processing', started_at=? WHERE id=?",
                  (_now(), job_id))

def queue_done(job_id: int):
    with _conn() as c:
        c.execute("UPDATE queue SET status='done' WHERE id=?", (job_id,))

def queue_position(job_id: int) -> tuple:
    """Vrátí (pořadí_v_čekání, počet_celkem_čekajících)."""
    with _conn() as c:
        waiting = c.execute(
            "SELECT id FROM queue WHERE status='waiting' ORDER BY created_at"
        ).fetchall()
        ids = [r[0] for r in waiting]
        if job_id in ids:
            return ids.index(job_id) + 1, len(ids)
        return 0, len(ids)

def queue_current_user() -> str:
    """Vrátí jméno uživatele, jehož úloha se právě zpracovává."""
    with _conn() as c:
        row = c.execute(
            "SELECT name FROM queue WHERE status='processing' ORDER BY started_at DESC LIMIT 1"
        ).fetchone()
        return row[0] if row else ""


# ── Streamlit API ─────────────────────────────────────────────────────────────

def init():
    """Zavolej jednou na začátku app.py (po st.set_page_config)."""
    _init_db()

    # Unikátní ID session (přežije rerun, né restart prohlížeče)
    if "presence_session_id" not in st.session_state:
        import uuid
        st.session_state["presence_session_id"] = str(uuid.uuid4())

    if "presence_name" not in st.session_state:
        st.session_state["presence_name"] = ""

    if "presence_tab_idx" not in st.session_state:
        st.session_state["presence_tab_idx"] = 0


def login_dialog():
    """
    Zobrazí dialog pro zadání jména — jednou za session.
    Zobrazí se jen pokud není přihlášen A uživatel klikl na 'Zadat nové jméno'.
    Pokud je presence_name již nastaveno (z tlačítek), rovnou pokračuje.
    """
    if st.session_state.get("presence_name"):
        return  # už přihlášen

    # Přihlášení tlačítkem proběhlo — presence_name je nastaveno, přeskočíme dialog
    if st.session_state.get("_preseed_username") and not st.session_state.get("_show_login_dialog"):
        # Jméno bylo vybráno tlačítkem, přihlásíme rovnou
        st.session_state["presence_name"] = st.session_state["_preseed_username"]
        st.rerun()
        return

    # Zobrazíme dialog jen pokud uživatel klikl na 'Zadat nové jméno'
    if not st.session_state.get("_show_login_dialog"):
        st.stop()  # čekáme na výběr jména nebo klik na tlačítko
        return

    # ── Formulář pro zadání nového jména ────────────────────────────────────
    _prefill = st.session_state.get("_preseed_username", "")
    st.markdown("---")
    st.markdown("### 👤 Kdo jsi?")
    col1, col2 = st.columns([3, 1])
    with col1:
        name = st.text_input("Tvoje jméno", key="presence_name_input",
                             value=_prefill,
                             placeholder="např. Martin",
                             label_visibility="collapsed")
    with col2:
        if st.button("▶ Vstoupit", type="primary", use_container_width=True):
            if name.strip():
                st.session_state["presence_name"] = name.strip()
                st.session_state.pop("_show_login_dialog", None)
                # Uložíme jméno do known_users přes callback (pokud existuje)
                _save_cb = st.session_state.get("_presence_save_user_cb")
                if callable(_save_cb):
                    _save_cb(name.strip())
                st.rerun()
            else:
                st.warning("Zadej jméno.")
    st.stop()


def heartbeat(tab_idx: int = 0):
    """
    Volej na začátku každého rerunu (nebo alespoň jednou za HEARTBEAT sekund).
    tab_idx = index aktuálně aktivní záložky (0–8).
    """
    name = st.session_state.get("presence_name", "")
    if not name:
        return
    sid  = st.session_state["presence_session_id"]
    tab  = TAB_NAMES.get(tab_idx, "?")
    st.session_state["presence_tab_idx"] = tab_idx
    _heartbeat(sid, name, tab, tab_idx)


def sidebar_widget():
    """
    Zobrazí widget 'Kdo je online' a frontu LLM v sidebaru.
    Volej uvnitř `with st.sidebar:` bloku.
    """
    name = st.session_state.get("presence_name", "")
    if not name:
        return

    sid   = st.session_state["presence_session_id"]
    users = _active_users()

    st.divider()
    st.markdown(f"**👥 Online ({len(users)})**")

    my_tab_idx = st.session_state.get("presence_tab_idx", 0)
    for row in users:
        u_sid, u_name, u_tab, u_tab_idx, u_last = row
        age = int(_now() - u_last)
        icon = "🟢" if age < 10 else "🟡"
        me   = " *(já)*" if u_sid == sid else ""
        st.caption(f"{icon} **{u_name}**{me}  \n↳ {u_tab}")

    # Fronta
    with _conn() as c:
        waiting = c.execute(
            "SELECT name FROM queue WHERE status='waiting' ORDER BY created_at"
        ).fetchall()
        processing = c.execute(
            "SELECT name FROM queue WHERE status='processing' ORDER BY started_at DESC LIMIT 1"
        ).fetchone()

    if processing or waiting:
        st.markdown("**📋 Fronta LLM**")
        if processing:
            st.caption(f"⚙️ zpracovává: **{processing[0]}**")
        for i, (w_name,) in enumerate(waiting):
            me = " *(já)*" if w_name == name else ""
            st.caption(f"{i+1}. {w_name}{me}")

    # Odhlášení
    if st.button("🚪 Odhlásit se", key="presence_logout", use_container_width=True):
        _remove_user(sid)
        st.session_state["presence_name"] = ""
        st.session_state["_current_user"] = ""
        st.session_state.pop("_preseed_username", None)
        st.session_state.pop("_show_login_dialog", None)
        st.rerun()


def my_queue_status() -> str:
    """
    Vrátí čitelný string o pozici ve frontě, nebo "".
    Volej kdekoliv v UI po spuštění LLM úlohy.
    """
    job_id = st.session_state.get("presence_job_id")
    if not job_id:
        return ""
    pos, total = queue_position(job_id)
    if pos == 0:
        current = queue_current_user()
        if current:
            return f"⚙️ Zpracovává se… (fronta prázdná, běží pro {current})"
        return ""
    return f"⏳ Tvoje úloha je **{pos}.** v pořadí (čeká {total} úloh)"


def llm_start() -> int:
    """
    Zavolej PŘED voláním LLM.
    Vrátí job_id — předej do llm_done().
    """
    name   = st.session_state.get("presence_name", "neznámý")
    sid    = st.session_state["presence_session_id"]
    job_id = queue_add(sid, name)
    queue_start(job_id)
    st.session_state["presence_job_id"] = job_id
    return job_id


def llm_done(job_id: int = None):
    """Zavolej PO dokončení LLM volání."""
    if job_id is None:
        job_id = st.session_state.get("presence_job_id")
    if job_id:
        queue_done(job_id)
        st.session_state.pop("presence_job_id", None)
