import sqlite3 as sl
con = sl.connect('Logs.db')
with con:
    con.execute("""
        CREATE TABLE CLIENTS (
            id_client INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            gmt INTEGER,
            type TEXT
        );
    """)
    con.commit()
    con.execute("""
        CREATE TABLE DEVICES (
            id_device INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            id_client INTEGER REFERENCES CLIENTS (id_client),
            name TEXT,
            username TEXT,
            version INTEGER
        );
    """)
    con.commit()
    con.execute("""
        CREATE TABLE LOG (
            id_log INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            id_device INTEGER REFERENCES DEVICES (id_device),
            date DATE,
            time TIME,
            depth INTEGER,
            power INTEGER
        );
    """)
    con.commit()