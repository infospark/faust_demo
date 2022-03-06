import unittest
from py import scraper
import undetected_chromedriver as uc
from py.order import Order
import jsonpickle


class TestJSONPickle(unittest.TestCase):

    order1 = Order('UK', 100)
    order2 = Order('FR', 150)

    def test_round_trip(self):
        frozen = jsonpickle.encode(self.order1)
        print('json pickled Order', frozen)
        thawed = jsonpickle.decode(frozen)
        print(thawed)
        assert(thawed == self.order1)