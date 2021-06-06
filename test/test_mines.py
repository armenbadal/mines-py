import unittest
import mines


class TestGameEngine(unittest.TestCase):

    def test_create(self):
        gf = mines.Field(5, 5)
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
