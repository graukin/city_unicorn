#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
import sqlite3

#import sys
#reload(sys)  # Reload does the trick!
#sys.setdefaultencoding('UTF8')

class DBHelper:
    def __init__(self, dbname="info_extractor/streets_Vologda.db"):
        self.dbname = dbname
        self.conn = sqlite3.connect(dbname)

    def setup(self):
        stmt = "CREATE TABLE IF NOT EXISTS streets (name text, district text, houses text, lon real, lat real)"
        self.conn.execute(stmt)
        self.conn.commit()

    def get_names(self, part):
        stmt = "SELECT name FROM streets WHERE name_low LIKE '%" + self.query2low(part) + "%'"
        print(stmt)
        return '\n'.join([x[0] for x in self.conn.execute(stmt)])

    def get_exact_name(self, part):
        stmt = "SELECT name, district, lon, lat FROM streets WHERE name_low LIKE '%" + self.query2low(part) + "%' LIMIT 1"
        print(stmt)
        return '\n'.join([x[0]+","+x[1]+", ( "+repr(x[2]) +" "+repr(x[3]) + " )" for x in self.conn.execute(stmt)])

    def get_zone(self, bounds):
        stmt = "SELECT name FROM streets WHERE lon <= " + repr(bounds['maxLon']) + " AND lon >= " + repr(bounds['minLon']) + " AND lat <= " + repr(bounds['maxLat']) + " AND lat >= " + repr(bounds['minLat'])
        print(stmt)
        return '\n'.join([x[0] for x in self.conn.execute(stmt)])

    def query2low(self, query):
        return query.lower().replace(' ', '.').replace('-','.')
