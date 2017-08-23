#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
import logging
import os
import sys
from bs4 import BeautifulSoup

soup = BeautifulSoup(open('example.html', 'r'), 'html.parser')
address=""
district=""
houses=[]
coords={}
ul=soup.find('ul', {"class" : "information"})
el_li=ul.li
while not el_li is None:
    if hasattr(el_li, 'b'):
        if el_li.b.string == "Адрес:":
            raw=el_li.span.string
            k=raw.rfind(', ')
            address=raw[k+2:]
        elif el_li.b.string == "Район города:":
            district=el_li.span.string
        elif el_li.b.string == "Номера домов:":
            raw=el_li.span.string
            houses=raw.replace(' ', '').replace('.', '').split(',')
    el_li=el_li.find_next_sibling('li')

meta=soup.find('meta', {"name" : "og:image"})
url=meta['content']
for el in url.split('?')[1].split('&'):
    if 'll=' in el:
        parts=el.split('=')[1].split(',')
        coords['n'] = float(parts[1])
        coords['e'] = float(parts[0])

print(address, '\n', district, '\n', houses, '\n', coords)
