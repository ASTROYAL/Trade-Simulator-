import unittest
from src.utils.logger import Logger
from src.utils.error_handler import ErrorHandler

class TestUtils(unittest.TestCase):

    def setUp(self):
        self.logger = Logger()
        self.error_handler = ErrorHandler()

    def test_logging(self):
        self.logger.log("Test log message")
        # Verify that the log message is correctly recorded
        # This would typically involve checking the log file or output

    def test_error_handling(self):
        try:
            self.error_handler.handle_error(Exception("Test exception"))
            # Verify that the error handling works as expected
        except Exception as e:
            self.fail(f"Error handling failed with exception: {e}")

if __name__ == '__main__':
    unittest.main()