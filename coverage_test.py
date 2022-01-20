import unittest

def helloworld(a):
    msg = f"Hello World! {a}"
    print(msg)
    return msg

class MainTest(unittest.TestCase):
    def test_helloworld(self):
        ret = helloworld("Test")
        self.assertEqual(ret, "Hello World! Test")

if __name__ == "__main__":
    unittest.main()