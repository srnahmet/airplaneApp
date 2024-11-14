from django.test import TestCase
from .models import Airplane

# Create your tests here.
class AirplaneModelTest(TestCase):
    def setUp(self):
        Airplane.objects.create(name="TB2")
        
    def test_car_name(self):
        car = Airplane.objects.get(name="TB2")
        self.assertEqual(car.name, "TB2")