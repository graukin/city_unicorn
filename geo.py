#!/usr/bin/python3.6
# -*- coding: utf-8 -*-

import math

class GeoPoint:
    def __init__(self, lon, lat):
        self.lon = lon
        self.lat = lat

    def printl(self):
        print("P: lon=" + repr(self.lon) + ", lat=" + repr(self.lat))

    def radian(self):
        return GeoPoint(self.lon*math.pi/180., self.lat*math.pi/180.)

class GeoWrapper:
    def __init__(self):
        pass

    def distance(self, point1, point2):
        radius = 6372795
        rP1 = point1.radian()
        rP2 = point2.radian()

        cl1 = math.cos(rP1.lat)
        cl2 = math.cos(rP2.lat)
        sl1 = math.sin(rP1.lat)
        sl2 = math.sin(rP2.lat)
        delta = rP2.lon - rP1.lon
        cdelta = math.cos(delta)
        sdelta = math.sin(delta)
 
        y = math.sqrt(math.pow(cl2*sdelta,2)+math.pow(cl1*sl2-sl1*cl2*cdelta,2))
        x = sl1*sl2+cl1*cl2*cdelta
        ad = math.atan2(y,x)
        dist = ad*radius
        return dist

