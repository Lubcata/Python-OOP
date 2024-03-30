from unittest import TestCase, main

from project.mammal import Mammal


class TestMammal(TestCase):

    def setUp(self):
        self.mammal = Mammal("name", "some_type", "hey")

    def test_correct__init__(self):
        self.assertEqual("name", self.mammal.name)
        self.assertEqual("some_type", self.mammal.type)
        self.assertEqual("hey", self.mammal.sound)
        self.assertEqual("animals", self.mammal._Mammal__kingdom)

    def test_correct_sound(self):
        self.assertEqual("name makes hey", self.mammal.make_sound())

    def test_get_kingdom_return_correct_str(self):
        self.assertEqual("animals", self.mammal.get_kingdom())

    def test_info_return_correct_str(self):
        self.assertEqual("name is of type some_type", self.mammal.info())


if __name__ == "__main__":
    main()
