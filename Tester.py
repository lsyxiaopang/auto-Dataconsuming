#该文件用于对DataConsumer进行测试
from DataConsumer import *
import unittest
class CheckRange(unittest.TestCase):
    def test_rangeout(self):
        s=RangeNumber(3,0.01)
        self.assertEqual(str(s),"$(3.00)^{0.01}_{0.01}$")

unittest.main()