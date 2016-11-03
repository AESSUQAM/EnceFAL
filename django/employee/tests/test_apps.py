# -*- encoding: utf-8 -*-

from django.test import TestCase
from employee.apps import *

class FormsTest(TestCase):
    def setUp(self):
        self.main_app = EmployeeConfig()

    def appNamesCorrect(self):
        assertEqual(main_app, "employee")
