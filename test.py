import unittest
import os
import csv
import tempfile
from unittest.mock import patch, mock_open
from util import processcsv, forcecopy
from adopt import csv_file_path as adopt_csv_file_path
from deploy import csv_file_path as deploy_csv_file_path

class TestProject(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.csv_content = "local_path,dest_path\nfile1.txt,~/file1.txt\nfile2.txt,~/file2.txt"
        self.csv_file = os.path.join(self.temp_dir, "test.csv")
        with open(self.csv_file, "w") as f:
            f.write(self.csv_content)

    def tearDown(self):
        os.remove(self.csv_file)
        os.rmdir(self.temp_dir)

    def test_loaddeploycsv(self):
        # Test with existing file
        self.assertEqual(processcsv(self.csv_file), self.csv_file)

        # Test with non-existing file
        with self.assertRaises(FileNotFoundError):
            processcsv("non_existing_file.csv")

    @patch('util.shutil.copy1')
    def test_ccp(self, mock_copy):
        origin = "origin.txt"
        destination = "destination.txt"

        # Test successful copy
        with patch('os.path.exists', return_value=True):
            forcecopy(origin, destination)
            mock_copy.assert_called_once_with(destination, origin)

        # Test FileNotFoundError
        with patch('os.path.exists', return_value=False):
            with self.assertRaises(FileNotFoundError):
                forcecopy(origin, destination)

    @patch('builtins.open', new_callable=mock_open, read_data=csv_content)
    @patch('util.ccp')
    def test_adopt(self, mock_ccp, mock_file):
        with patch('sys.argv', ['adopt.py', self.csv_file]):
            import adopt
            mock_ccp.assert_called()

    @patch('builtins.open', new_callable=mock_open, read_data=csv_content)
    @patch('util.ccp')
    def test_deploy(self, mock_ccp, mock_file):
        with patch('sys.argv', ['deploy.py', self.csv_file]):
            import deploy
            mock_ccp.assert_called()

    def test_csv_file_path(self):
        # Test default CSV file path
        with patch('sys.argv', ['script.py']):
            self.assertEqual(adopt_csv_file_path, 'deploy-destinations.csv')
            self.assertEqual(deploy_csv_file_path, 'deploy-destinations.csv')

        # Test custom CSV file path
        custom_path = 'custom.csv'
        with patch('sys.argv', ['script.py', custom_path]):
            from adopt import csv_file_path as adopt_custom_path
            from deploy import csv_file_path as deploy_custom_path
            self.assertEqual(adopt_custom_path, custom_path)
            self.assertEqual(deploy_custom_path, custom_path)

if __name__ == '__main__':
    unittest.main()
