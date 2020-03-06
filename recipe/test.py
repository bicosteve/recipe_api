
from django.test import TestCase


from recipe.calc import add, subtract

class CalcTest(TestCase):


    def test_add_numbers(self):
        '''Test that two numbers are added together'''
        self.assertEqual(add(2,1),3)


    def test_substract_numbers(self):
        '''test that values are subtracted and return'''
        self.assertEqual(subtract(11,5),6)

