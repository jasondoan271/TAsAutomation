import sqlite3
import hashlib

DB_NAME = "threats.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    # Fang's wet dream rn ifykyk
    # content_hash to check for duplicates based on RAW content

    c.execute("""
        CREATE TABLE IF NOT EXISTS threats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source TEXT,
            title TEXT,
            link TEXT,
            published TEXT,
            summary TEXT,
            clean_content TEXT,
            categories TEXT,
            cves TEXT,
            content_hash TEXT UNIQUE,
            processed INTEGER DEFAULT 0
        )
    """)
    c.execute("CREATE INDEX IF NOT EXISTS idx_processed ON threats(processed)") # indexing is WAY faster than comparing all rows (this only looks at processed column then maps to rows (pick 3 VS search until 3 r found))
    conn.commit()
    conn.close()

def compute_hash(raw_text):
    """Hash ONLY the raw content for deduplication."""
    if raw_text is None:
        raw_text = ""
    return hashlib.sha256(raw_text.encode("utf-8", "ignore")).hexdigest()

def insert_threat(threat):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    # Hash the RAW content
    content_hash = compute_hash(threat["raw_content"])

    try:
        c.execute("""
            INSERT INTO threats
            (source, title, link, published, summary, clean_content, categories, cves, content_hash)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            threat["source"],
            threat["title"],
            threat["link"],
            threat["published"],
            threat["summary"],
            threat["clean_content"],   # sanitized content ONlY to be inserted in db
            ",".join(threat["categories"]),
            ",".join(threat["cves"]),
            content_hash
        ))
        conn.commit()
    except sqlite3.IntegrityError:
        # ^^^ exception finds dupe based on hash, ignores it n continues
        pass
    finally:
        conn.close()

def get_unprocessed_per_source(limit_per_source):
    """
    Fetch a limited (defined) number of unprocessed articles for each source and
    returns a list of rows.
    """
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    # First, get distinct sources cause its boring otherwise (one source could be the only one for newsletter)
    c.execute("SELECT DISTINCT source FROM threats")
    sources = [row[0] for row in c.fetchall()] 

    rows = []
    for src in sources:
        c.execute("""
            SELECT id, source, title, summary, clean_content, cves, link
            FROM threats
            WHERE processed = 0 AND source = ?
            ORDER BY published DESC
            LIMIT ?
        """, (src, limit_per_source))
        rows.extend(c.fetchall()) # fetches all of the columns from the command above and continuously appends to rows, list of tuples (ts took me too long even w GPT)

    conn.close()
    return rows

def mark_processed(ids):
    """Mark items as processed after sending it to the LLM/newsletter."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.executemany(
        "UPDATE threats SET processed = 1 WHERE id = ?",
        [(i,) for i in ids]
    )
    conn.commit() # remember to commit changes
    conn.close()

