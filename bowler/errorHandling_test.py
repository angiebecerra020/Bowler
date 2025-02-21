import unittest
from unittest.mock import patch
from your_module import process_file, FilenameMatcherError  
import logging

# Set up logging to capture log outputs
log = logging.getLogger()
log.setLevel(logging.DEBUG)

class TestFilenameMatcherErrorHandling(unittest.TestCase):
    @patch('your_module.filename_matcher')  # Mocking filename_matcher
    @patch('time.sleep')  # Mock sleep to avoid actual delays in tests
    def test_retry_on_permission_error(self, mock_sleep, mock_filename_matcher):
        # Simulate PermissionError on the first two attempts
        mock_filename_matcher.side_effect = [PermissionError("Permission denied"), 
                                             PermissionError("Permission denied"), 
                                             True]

        # Call the function to test
        process_file("test_file.txt")

        # Check that filename_matcher was called 3 times
        self.assertEqual(mock_filename_matcher.call_count, 3)
        mock_sleep.assert_called_with(1)

    @patch('your_module.filename_matcher')
    @patch('time.sleep')
    def test_file_not_found(self, mock_sleep, mock_filename_matcher):
        # Simulate FileNotFoundError
        mock_filename_matcher.side_effect = FileNotFoundError("File not found")

        with self.assertRaises(FilenameMatcherError):
            process_file("non_existent_file.txt")

    @patch('your_module.filename_matcher')
    @patch('time.sleep')
    def test_generic_error_handling(self, mock_sleep, mock_filename_matcher):
        # Simulate a generic exception
        mock_filename_matcher.side_effect = Exception("Generic error")

        # Call the function and check it retries
        process_file("error_file.txt")

        self.assertEqual(mock_filename_matcher.call_count, 3)
        mock_sleep.assert_called_with(1)

if __name__ == '__main__':
    unittest.main()

