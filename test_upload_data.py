import unittest
from mongoengine import connect
from unittest.mock import patch
from io import StringIO
from main import Author, Quote
from upload_data import main

class TestUploadData(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Connect to the test database
        connect(
            db='test_db',
            alias='default',
            username='soboleva13as',
            password='5413034002246',
            host='mongodb+srv://soboleva13as:5413034002246@cluster0.xpt2wff.mongodb.net/web8'
        )

    @classmethod
    def tearDownClass(cls):
        # Drop the test database after all tests have run
        connection = Author._get_db().client
        connection.drop_database('test_db')

    def test_upload_data(self):
        connection_string = 'mongodb+srv://soboleva13as:5413034002246@cluster0.xpt2wff.mongodb.net/web8'

        with patch('builtins.input', return_value=connection_string):
            with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                main()

                output = mock_stdout.getvalue()
                self.assertIn("Pinged MongoDB using pymongo. Connection successful!", output)

                albert_einstein = Author.objects(fullname="Albert Einstein").first()
                self.assertIsNotNone(albert_einstein)

                steve_martin = Author.objects(fullname="Steve Martin").first()
                self.assertIsNotNone(steve_martin)

                quote1 = Quote.objects(
                    quote="“The world as we have created it is a process of our thinking. It cannot be changed without changing our thinking.”").first()
                self.assertIsNotNone(quote1)

                quote2 = Quote.objects(
                    quote="“There are only two ways to live your life. One is as though nothing is a miracle. The other is as though everything is a miracle.”").first()
                self.assertIsNotNone(quote2)

                quote3 = Quote.objects(
                    quote="“Try not to become a man of success. Rather become a man of value.”").first()
                self.assertIsNotNone(quote3)

                quote4 = Quote.objects(quote="“A day without sunshine is like, you know, night.”").first()
                self.assertIsNotNone(quote4)

if __name__ == '__main__':
    unittest.main()
