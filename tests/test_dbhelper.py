#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
import unittest

from dbhelper import DBHelper

class TestMain(unittest.TestCase):
    def test_grep_single(self):
        db = DBHelper()

        text = u"улица Генерала Зимина"

        self.assertEqual(text, db.get_names("Зимин"))
        self.assertEqual(text, db.get_names("зимин"))
        self.assertEqual(text, db.get_names("ЗимИН"))

    def test_grep_list(self):
        db = DBHelper()

        text = u"улица Генерала Зимина\nулица Генерала Штеменко\nулица Им Генерала Клюева\nулица имени Генерала Ивлиева И.Д."

        self.assertEqual(text, db.get_names("Генерал"))
        self.assertEqual(text, db.get_names("генерал"))
        self.assertEqual(text, db.get_names("гЕНЕРАЛ"))

        text = u"Оранжерейный тупик\nТупиковый 1-й переулок\nТупиковый 2-й переулок\nТупиковый 3-й переулок"
        self.assertEqual(text, db.get_names("тупик"))

if __name__ == '__main__':
    unittest.main()
