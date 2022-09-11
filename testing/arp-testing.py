import unittest
import arp_v as tool


class MyTestCase(unittest.TestCase):
    def test_ping_success(self):
        output = tool.run_command("ping 127.0.0.1")
        success = "(0% loss"
        self.assertIn(success, output)


    def test_ping_fail(self):
        output = tool.run_command("this should fail")
        success = "00% loss"
        self.assertIn(success, output)


if __name__ == '__main__':
    unittest.main()
