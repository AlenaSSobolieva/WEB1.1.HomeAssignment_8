# main_rabbit.py

import pika
from threading import Thread
import threading
from faker import Faker
from mongoengine import connect, Document, StringField, BooleanField
from bson import ObjectId

fake = Faker()

# MongoDB setup
connect(db='web-8', username='soboleva13as', password='5413034002246',
        host='mongodb+srv://soboleva13as:5413034002246@cluster0.xpt2wff.mongodb.net/web8')

# Contact model
class Contact(Document):
    full_name = StringField(required=True)
    email = StringField(required=True)
    message_sent = BooleanField(default=False)

# RabbitMQ setup
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='email_queue')

def send_email(contact_id):
    # Simulate sending email
    print(f"Sending email to contact with ID {contact_id}")

def callback(ch, method, properties, body):
    contact_id = ObjectId(body.decode())
    contact = Contact.objects(id=contact_id).first()

    if contact:
        send_email(contact_id)
        contact.message_sent = True
        contact.save()

# Set up RabbitMQ consumer in a separate thread
consume_event = threading.Event()

def consume_messages():
    channel.start_consuming()

consume_thread = Thread(target=consume_messages, daemon=True)
consume_thread.start()

print('Waiting for messages. To exit, press CTRL+C')

consume_event.set()
