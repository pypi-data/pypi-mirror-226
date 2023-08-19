from unittest import TestCase

from cnvrg_endpoint_binary import EndpointBinary

__author__ = "Craig Smith"
__copyright__ = "Craig Smith"
__license__ = "MIT"


class TestInit(TestCase):
    def test_init_good_no_endpoint(self):
        test_eb = EndpointBinary(binary_name="./main", endpoint="dummy")
        self.assertEqual(test_eb.binary_name, "./main")
