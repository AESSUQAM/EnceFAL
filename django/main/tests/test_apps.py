# -*- encoding: utf-8 -*-

from django.test import TestCase
from main.apps import *
import os

class FormsTest(TestCase):
    def setUp(self):
        class temp:
            __path__ = "."
        self.a = temp()
        self.main_app = MainConfig("main", self.a)

    def test_appNamesCorrect(self):
        self.assertEqual(self.main_app.name, "main")
