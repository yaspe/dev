import sqlite3

"""
table creation: CREATE TABLE links(id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, uid INT NOT NULL, link TEXT NOT NULL);
"""


class TLinkDb(object):
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)

    def links(self, uid, limit=None):
        if limit is None:
            limit = 100
        sql = 'SELECT * FROM links WHERE uid = ? ORDER BY id DESC limit ?'

        return [{'id': row[0], 'link': row[2].encode('utf-8')} for row in self.conn.execute(sql, (uid, limit))]

    def store(self, uid, link):
        sql = 'INSERT INTO links (uid, link) VALUES (?, ?);'
        self.conn.execute(sql, (uid, link))
        self.conn.commit()

    def remove(self, link_id, uid):
        sql = 'DELETE FROM links WHERE id = ? AND uid = ?;'
        self.conn.execute(sql, (link_id, uid))
        self.conn.commit()
