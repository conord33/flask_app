from unittest import TestLoader, TextTestRunner, TestSuite

from tests.test_data import DataTestCase

if __name__ == "__main__":

	# Create test suite
    loader = TestLoader()
    suite = TestSuite((
        loader.loadTestsFromTestCase(DataTestCase)
    ))

    runner = TextTestRunner(verbosity = 2)
    runner.run(suite)