# -*- encoding: utf-8 -*-

from django.test import TestCase
from employee.apps import *
import os

class FormsTest(TestCase):
    def setUp(self):
        class temp:
            __path__ = "."
        self.a = temp()
        self.main_app = EmployeeConfig("employee", self.a)

    def test_appNamesCorrect(self):
        self.assertEqual(self.main_app.name, "employee")
