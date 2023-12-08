import unittest
from io import StringIO
from unittest.mock import patch
from mongoengine import connect
from faker import Faker
from main_rabbit import Contact, callback


class TestMainRabbitScript(unittest.TestCase):

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
        connection = Contact._get_db().client
        connection.drop_database('test_db')


    def setUp(self):
        # Create fake contact for testing
        self.fake = Faker()
        contact = Contact(full_name=self.fake.name(), email=self.fake.email())
        contact.save()

    @patch('main_rabbit.send_email', autospec=True)
    def test_callback(self, mock_send_email):
        contact = Contact.objects().first()
        contact_id = str(contact.id)

        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            callback(None, None, None, contact_id.encode())

            # Print actual call arguments
            print("Actual call arguments:", mock_send_email.call_args_list)

            # Check if send_email was called
            mock_send_email.assert_called_once()

            # Check if the first (and only) call to send_email has the correct argument
            first_call_args, _ = mock_send_email.call_args_list[0]
            self.assertEqual(str(first_call_args[0]), contact_id)

            # Check if the message_sent field is set to True
            updated_contact = Contact.objects(id=contact.id).first()
            self.assertTrue(updated_contact.message_sent)


if __name__ == '__main__':
    unittest.main()
