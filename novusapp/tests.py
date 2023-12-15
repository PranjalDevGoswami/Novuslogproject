from django.test import TestCase

# Create your tests here.



def add_two_numbers(a, b):
    return a + b

class TestExample(TestCase):

    def test_add_two_numbers(self):
        self.assertEqual(add_two_numbers(2, 2), 4)