#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
import logging
import os
import sys
import sqlite3
from bs4 import BeautifulSoup

class StreetObj:
    def __init__(self):
        self.address=""
        self.low=""
        self.district=""
        self.houses=[]
        self.coords={}

    def print(self):
        print(self.address)
        print(self.district)
        print(self.houses)
        print(self.coords)

    def pack_houses(self):
        return "," + ','.join(self.houses) + ",";
   
    def create_insert(self):
        return "INSERT INTO streets VALUES ('" + self.address + "','" + self.low + "','" + self.district + "','" + self.pack_houses() + "'," + repr(self.coords['lon']) + "," + repr(self.coords['lat']) + ")"

soup = BeautifulSoup(open(sys.argv[1], 'r'), 'html.parser')

street = StreetObj()
ul=soup.find('ul', {"class" : "information"})
el_li=ul.li
while not el_li is None:
    if hasattr(el_li, 'b'):
        if el_li.b.string == "Адрес:":
            raw=el_li.span.string
            k=raw.rfind(', ')
            street.address=raw[k+2:]
            street.low=raw[k+2:].lower()
        elif el_li.b.string == "Район города:":
            street.district=el_li.span.string
        elif el_li.b.string == "Номера домов:":
            raw=el_li.span.string
            street.houses=raw.replace(' ', '').replace('.', '').split(',')
    el_li=el_li.find_next_sibling('li')

meta=soup.find('meta', {"name" : "og:image"})
url=meta['content']
for el in url.split('?')[1].split('&'):
    if 'll=' in el:
        parts=el.split('=')[1].split(',')
        street.coords['lat'] = float(parts[1])
        street.coords['lon'] = float(parts[0])

#street.print()

conn = sqlite3.connect(r"streets_NizhNov.db")
c = conn.cursor()

#c.execute('''CREATE TABLE streets
#             (name text, name_low text, district text, houses text, lon real, lat real)''')

#print(street.create_insert())
#c.execute(street.create_insert())

#for row in c.execute("SELECT DISTINCT district FROM streets"):
#    print(row)

conn.commit()
conn.close()
