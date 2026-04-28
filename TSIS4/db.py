"""
db.py — PostgreSQL database layer using psycopg2.

All functions return Python values; callers need not know SQL.
If the database is unavailable the functions degrade gracefully
(print a warning and return safe defaults) so the game still runs
without a running Postgres instance.
"""

import datetime

try:
    import psycopg2
    import psycopg2.extras
    PSYCOPG2_AVAILABLE = True
except ImportError:
    PSYCOPG2_AVAILABLE = False
    print("[DB] psycopg2 not found — database features disabled.")

import config

# ---------- connection helper ----------

def _connect():
    """Open and return a new psycopg2 connection, or None on failure."""
    if not PSYCOPG2_AVAILABLE:
        return None
    try:
        conn = psycopg2.connect(
            host=config.DB_HOST,
            port=config.DB_PORT,
            dbname=config.DB_NAME,
            user=config.DB_USER,
            password=config.DB_PASSWORD,
            connect_timeout=3,
        )
        return conn
    except Exception as e:
        print(f"[DB] Connection failed: {e}")
        return None


# ---------- schema initialisation ----------

CREATE_PLAYERS = """
CREATE TABLE IF NOT EXISTS players (
    id       SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL
);
"""

CREATE_SESSIONS = """
CREATE TABLE IF NOT EXISTS game_sessions (
    id            SERIAL PRIMARY KEY,
    player_id     INTEGER REFERENCES players(id),
    score         INTEGER   NOT NULL,
    level_reached INTEGER   NOT NULL,
    played_at     TIMESTAMP DEFAULT NOW()
);
"""

def init_db():
    """Create tables if they do not exist yet."""
    conn = _connect()
    if conn is None:
        return
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute(CREATE_PLAYERS)
                cur.execute(CREATE_SESSIONS)
        print("[DB] Schema ready.")
    except Exception as e:
        print(f"[DB] init_db error: {e}")
    finally:
        conn.close()


# ---------- player ----------

def get_or_create_player(username: str) -> int | None:
    """
    Return the player_id for *username*, creating the row if absent.
    Returns None on database error.
    """
    conn = _connect()
    if conn is None:
        return None
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO players (username) VALUES (%s) "
                    "ON CONFLICT (username) DO NOTHING;",
                    (username,)
                )
                cur.execute("SELECT id FROM players WHERE username = %s;", (username,))
                row = cur.fetchone()
                return row[0] if row else None
    except Exception as e:
        print(f"[DB] get_or_create_player error: {e}")
        return None
    finally:
        conn.close()


# ---------- sessions ----------

def save_session(player_id: int, score: int, level_reached: int) -> bool:
    """Insert a completed game session.  Returns True on success."""
    conn = _connect()
    if conn is None:
        return False
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO game_sessions (player_id, score, level_reached) "
                    "VALUES (%s, %s, %s);",
                    (player_id, score, level_reached)
                )
        return True
    except Exception as e:
        print(f"[DB] save_session error: {e}")
        return False
    finally:
        conn.close()


def get_personal_best(player_id: int) -> int:
    """Return the player's all-time highest score, or 0 on failure."""
    conn = _connect()
    if conn is None:
        return 0
    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT COALESCE(MAX(score), 0) FROM game_sessions "
                "WHERE player_id = %s;",
                (player_id,)
            )
            row = cur.fetchone()
            return row[0] if row else 0
    except Exception as e:
        print(f"[DB] get_personal_best error: {e}")
        return 0
    finally:
        conn.close()


def get_leaderboard(limit: int = 10) -> list[dict]:
    """
    Return the top *limit* scores across all players.
    Each entry is a dict with keys:
        rank, username, score, level_reached, played_at
    """
    conn = _connect()
    if conn is None:
        return []
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(
                """
                SELECT
                    ROW_NUMBER() OVER (ORDER BY gs.score DESC) AS rank,
                    p.username,
                    gs.score,
                    gs.level_reached,
                    gs.played_at
                FROM game_sessions gs
                JOIN players p ON p.id = gs.player_id
                ORDER BY gs.score DESC
                LIMIT %s;
                """,
                (limit,)
            )
            rows = cur.fetchall()
            return [dict(r) for r in rows]
    except Exception as e:
        print(f"[DB] get_leaderboard error: {e}")
        return []
    finally:
        conn.close()