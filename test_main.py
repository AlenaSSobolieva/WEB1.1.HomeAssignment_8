import unittest
from mongoengine import connect
from main import Author, Quote

class TestMainScript(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Connect to the test database
        connect(
            db='test_db',
            alias='default',  # Explicitly specify the alias for the default connection
            username='soboleva13as',
            password='5413034002246',
            host='mongodb+srv://soboleva13as:5413034002246@cluster0.xpt2wff.mongodb.net/web8'
        )

    @classmethod
    def tearDownClass(cls):
        # Drop the test database after all tests have run
        connection = Author._get_db().client
        connection.drop_database('test_db')

    def test_author_creation(self):
        # Test if the Author object is created and saved successfully
        author_data = {
            'fullname': 'Test Author',
            'born_date': 'January 1, 2000',
            'born_location': 'Test City',
            'description': 'Test Description'
        }
        author = Author(**author_data)
        author.save()

        saved_author = Author.objects(fullname=author_data['fullname']).first()
        self.assertIsNotNone(saved_author)
        self.assertEqual(saved_author.born_date, author_data['born_date'])

    def test_quote_creation(self):
        # Test if the Quote object is created and saved successfully
        author_data = {
            'fullname': 'Test Author',
            'born_date': 'January 1, 2000',
            'born_location': 'Test City',
            'description': 'Test Description'
        }
        test_author = Author(**author_data)
        test_author.save()

        quote_data = {
            'tags': ['tag1', 'tag2'],
            'author': test_author,
            'quote': 'Test Quote'
        }
        quote = Quote(**quote_data)
        quote.save()

        saved_quote = Quote.objects(quote=quote_data['quote']).first()
        self.assertIsNotNone(saved_quote)
        self.assertEqual(saved_quote.tags, quote_data['tags'])
        self.assertEqual(saved_quote.author, test_author)
        self.assertEqual(saved_quote.quote, quote_data['quote'])

if __name__ == '__main__':
    unittest.main()
