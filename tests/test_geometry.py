import uuid
from unittest import TestCase
from src.geometry import Node, Line


class GeometryTestCase(TestCase):

    def test_line_definition_by_id(self):
        a = Node(0, 0)
        k = Node(1, 0)

        line = Line(a.id, k.id)

        self.assertTrue(type(line.id),uuid.UUID)

