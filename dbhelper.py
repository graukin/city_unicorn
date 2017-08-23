import sqlite3


class DBHelper:
    def __init__(self, dbname="info_extractor/streets_NizhNov.db"):
        self.dbname = dbname
        self.conn = sqlite3.connect(dbname)

    def setup(self):
        stmt = "CREATE TABLE IF NOT EXISTS streets (name text, district text, houses text, lon real, lat real)"
        self.conn.execute(stmt)
        self.conn.commit()

    def get_names(self, part):
        stmt = "SELECT name FROM streets WHERE name LIKE '%" + part + "%'"
        return ','.join([x[0] for x in self.conn.execute(stmt)])
