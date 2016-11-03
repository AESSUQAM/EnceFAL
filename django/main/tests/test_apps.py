# -*- encoding: utf-8 -*-

from django.test import TestCase
from main.apps import *

class FormsTest(TestCase):
    def setUp(self):
        self.main_app = MainConfig()

    def appNamesCorrect(self):
        assertEqual(main_app, "main")
