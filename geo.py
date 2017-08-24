#!/usr/bin/python3.6
# -*- coding: utf-8 -*-

import math

class Cortesian:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

class GeoPoint:
    def __init__(self, lon, lat):
        self.lon = lon
        self.lat = lat

    def printl(self):
        print("P: lon=" + repr(self.lon) + ", lat=" + repr(self.lat))

    def degree2radian(self):
        return GeoPoint(self.lon*math.pi/180., self.lat*math.pi/180.)
 
    def radian2degree(self):
        return GeoPoint(self.lon*180./math.pi, self.lat*180./math.pi)

    def cortesian(self):
        rad = self.degree2radian()
        X = math.cos(rad.lat) * math.cos(rad.lon)
        Y = math.cos(rad.lat) * math.sin(rad.lon)
        Z = math.sin(rad.lat)
        return Cortesian(X, Y, Z)

class GeoZone:
    def __init__(self, point1, point2, offset):
        wrapper = GeoWrapper()
        self.central = wrapper.central(point1, point2)
        self.radius = wrapper.distance(point1, self.central) + offset
        self.bounds = wrapper.bounds(self.central, self.radius)

class GeoWrapper:
    def __init__(self):
        pass

    def distance(self, point1, point2):
        radius = 6372795
        rP1 = point1.degree2radian()
        rP2 = point2.degree2radian()

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

    def central(self, point1, point2):
        cort1 = point1.cortesian()
        cort2 = point2.cortesian()

        x = cort1.x + cort2.x
        y = cort1.y + cort2.y
        z = cort1.z + cort2.z
        Lon = math.atan2(y, x)
        Hyp = math.sqrt(x * x + y * y)
        Lat = math.atan2(z, Hyp)

        return GeoPoint(Lon, Lat).radian2degree()

    def bounds(self, central, distance):
        kmInLongitudeDegree = 111.320 * math.cos( central.lat / 180. * math.pi)
        deltaLat = distance / (1000.*111.1)
        deltaLong = distance / (1000.*kmInLongitudeDegree)

        bounds={}
        bounds['minLat'] = central.lat - deltaLat
        bounds['maxLat'] = central.lat + deltaLat
        bounds['minLon'] = central.lon - deltaLong
        bounds['maxLon'] = central.lon + deltaLong
        return bounds

