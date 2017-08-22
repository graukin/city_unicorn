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
ul=soup.find('ul', class_="information")
el_li=ul.li
while not el_li is None:
    if hasattr(el_li, 'b'):
        if el_li.b.string == u"Адрес:":
            raw=el_li.span.string
            k=raw.rfind(', ')
            address=raw[k+2:]
        if el_li.b.string == u"Район города:":
            district=el_li.span.string
        if el_li.b.string == u"Номера домов:":
            raw=el_li.span.string
            houses=raw.replace(' ', '').replace('.', '').split(',')
    el_li=el_li.find_next_sibling('li')

print address,"\n",district,"\n",houses

for div in soup.find_all('div', class_="content-block"):
    if hasattr(div, 'h2') and hasattr(div, 'p'):
        print div.p
