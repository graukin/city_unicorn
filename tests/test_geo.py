#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
import unittest

from geo import GeoPoint, GeoWrapper

class TestMain(unittest.TestCase):
    def test_basic(self):
        point = GeoPoint(1.1234, 45.983)
        radPoint = point.degree2radian()
        self.assertAlmostEqual(radPoint.lon, 0.0196070288, places=4, msg=None, delta=None)
        self.assertAlmostEqual(radPoint.lat, 0.80255475, places=4, msg=None, delta=None)

        degPoint = radPoint.radian2degree()
        self.assertAlmostEqual(degPoint.lon, point.lon, places=4, msg=None, delta=None)
        self.assertAlmostEqual(degPoint.lat, point.lat, places=4, msg=None, delta=None)

    def test_distance(self):
        wrapper = GeoWrapper()

        self.assertAlmostEqual(wrapper.distance(GeoPoint(-139.398,77.1539), GeoPoint(-139.55,-77.1804))/100., 171660.29, places=2, msg=None, delta=None)
        self.assertAlmostEqual(wrapper.distance(GeoPoint(120.398,77.1539), GeoPoint(129.55,77.1804))/100., 2258.83, places=2, msg=None, delta=None)
        self.assertAlmostEqual(wrapper.distance(GeoPoint(-120.398,77.1539), GeoPoint(129.55,77.1804))/100., 23326.69, places=2, msg=None, delta=None)

    def test_central(self):
        wrapper = GeoWrapper()
        p1 = GeoPoint(43.978471,56.319519)
        p2 = GeoPoint(43.977447,56.319724)
        c = wrapper.central(p1, p2)
        self.assertAlmostEqual(wrapper.distance(p1, c)/100., wrapper.distance(p2, c)/100., places=2, msg=None, delta=None)

        bounds=wrapper.bounds(c, 30)
        print(wrapper.distance(c, GeoPoint(c.lon, bounds['minLat'])))
        print(wrapper.distance(c, GeoPoint(c.lon, bounds['maxLat'])))
        print(wrapper.distance(c, GeoPoint(bounds['minLon'], c.lat)))
        print(wrapper.distance(c, GeoPoint(bounds['maxLon'], c.lat)))

if __name__ == '__main__':
    unittest.main()

