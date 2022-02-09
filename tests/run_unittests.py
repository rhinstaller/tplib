#!/usr/bin/python3

import unittest
import sys

if __name__ == "__main__":
    loader = unittest.TestLoader()
    tests = loader.discover(pattern="test*.py", start_dir=".")
    runner = unittest.runner.TextTestRunner(verbosity=2)
    result = runner.run(tests)
    if not result.wasSuccessful():
        sys.exit(2)
