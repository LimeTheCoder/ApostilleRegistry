from django.test import TestCase
from .models import Organ

# Create your tests here.


class OrganModelTest(TestCase):

    def test_string_representation(self):
        organ = Organ(name='Judge')
        self.assertEqual(str(organ), organ.name)
