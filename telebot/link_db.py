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

    def all_links(self):
        sql = 'SELECT * FROM links'
        return [{'id': row[0], 'uid': row[1], 'link': row[2].encode('utf-8')} for row in self.conn.execute(sql)]

    def total_stat(self):
        sql = 'SELECT * FROM links'
        users = set()
        links_num = 0
        for row in self.conn.execute(sql):
            links_num += 1
            users.add(row[1])
        return {'users': len(users), 'links': links_num}

    def total_users(self):
        sql = 'SELECT * FROM links'
        return len([row for row in self.conn.execute(sql)])

    def store(self, uid, link):
        sql = 'INSERT INTO links (uid, link) VALUES (?, ?);'
        self.conn.execute(sql, (uid, link))
        self.conn.commit()

    def remove(self, link_id, uid):
        sql = 'DELETE FROM links WHERE id = ? AND uid = ?;'
        self.conn.execute(sql, (link_id, uid))
        self.conn.commit()
