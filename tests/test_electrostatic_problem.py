import unittest

from examples.electrostatics.capacitance import planar_capacitor

class TestFemmElectrostaticProblem(unittest.TestCase):
    # integration test ignored from the unittest list
    def test_electrostatic_problem(self):

        planar_capacitor.planar_capacitor_problem(0.2, 0.005, 0.01)
