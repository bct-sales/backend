import sqlite3
import logging
import sys
import os


script = '''
CREATE TABLE sale_events (
    sale_event_id INTEGER PRIMARY KEY,
    date TEXT NOT NULL,
    description TEXT NOT NULL
);

CREATE TABLE users (
    user_id INTEGER PRIMARY KEY,
    email_address STRING NOT NULL UNIQUE,
    password_hash STRING NOT NULL
);

CREATE TABLE items (
    item_id INTEGER PRIMARY KEY,
    description TEXT NOT NULL,
    price_in_cents INTEGER NOT NULL,
    sale_event_id INTEGER,
    owner_id INTEGER,
    recipient_id INTEGER,
    FOREIGN KEY (sale_event_id)
        REFERENCES sale_events (sale_event_id)
        ON DELETE CASCADE,
    FOREIGN KEY (owner_id)
        REFERENCES users (user_id)
        ON DELETE CASCADE,
    FOREIGN KEY (recipient_id)
        REFERENCES users (user_id)
        ON DELETE CASCADE
);
'''


DB_FILENAME = os.getenv('BCT_DATABASE')

if DB_FILENAME is None:
    logging.error('No BCT_DB_FILENAME environment variable set')
    DB_FILENAME = 'bct.db'
    # sys.exit(-1)

db = sqlite3.connect(DB_FILENAME)

db.executescript(script)
