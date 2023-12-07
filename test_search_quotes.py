import unittest
import json
from io import StringIO
from unittest.mock import patch
from mongoengine import connect, disconnect
from main import Author, Quote
import search_quotes  # Import your search_quotes module

class TestSearchQuotes(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Connect to the main application database
        connect(
            db='test_db',
            alias='default',  # Explicitly specify the alias for the default connection
            username='soboleva13as',
            password='5413034002246',
            host='mongodb+srv://soboleva13as:5413034002246@cluster0.xpt2wff.mongodb.net/web8'
        )

    @classmethod
    def tearDownClass(cls):
        # Disconnect explicitly from the main application database
        disconnect(alias='default')

    def setUp(self):
        # Load data from JSON files
        with open(r'C:\GIT_HUB\WEB1.1.HomeAssignment_8\authors.json', 'r', encoding='utf-8') as file:
            authors_data = json.load(file)

        with open(r'C:\GIT_HUB\WEB1.1.HomeAssignment_8\qoutes.json', 'r', encoding='utf-8') as file:
            quotes_data = json.load(file)

        # Store data in MongoDB
        for author_data in authors_data:
            author = Author(**author_data)
            author.save()

        for quote_data in quotes_data:
            author = Author.objects(fullname=quote_data['author']).first()
            if 'author' in quote_data:
                del quote_data['author']  # Remove 'author' key if present
            quote = Quote(author=author, **quote_data)
            quote.save()

    def tearDown(self):
        # Clear the data in the test database after each test
        connection = Author._get_db().client
        connection.drop_database('test_db')

    @patch('builtins.input', side_effect=['name:Albert Einstein', 'exit'])
    def test_search_by_name(self, mock_input):
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            search_quotes.main()
            output = mock_stdout.getvalue()
            self.assertIn("Albert Einstein:", output)
            self.assertIn("The world as we have created it is a process of our thinking.", output)

    @patch('builtins.input', side_effect=['tag:change', 'exit'])
    def test_search_by_tag(self, mock_input):
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            search_quotes.main()
            output = mock_stdout.getvalue()
            self.assertIn("Albert Einstein:", output)
            self.assertIn("The world as we have created it is a process of our thinking.", output)

if __name__ == '__main__':
    unittest.main()
