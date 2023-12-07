# upload_data.py

import json
from mongoengine import connect
from pymongo import MongoClient  # Add this import
from main import Author, Quote

def main():
    # Replace 'your_connection_string' with your actual MongoDB Atlas connection string
    connection_string = 'mongodb+srv://soboleva13as:5413034002246@cluster0.xpt2wff.mongodb.net/web8'

    # Check the connection using pymongo
    try:
        pymongo_client = MongoClient(connection_string)
        pymongo_client.admin.command('ping')
        print("Pinged MongoDB using pymongo. Connection successful!")
    except Exception as e:
        print("Error connecting to MongoDB using pymongo:", e)

    # Now, connect using mongoengine
    connect(db='web-8', username='soboleva13as', password='5413034002246',
            host='mongodb+srv://soboleva13as:5413034002246@cluster0.xpt2wff.mongodb.net/web8')

    # Load data from JSON files
    with open(r'C:\GIT_HUB\WEB1.1.HomeAssignment_8\authors.json', 'r', encoding='utf-8') as file:
        authors_data = json.load(file)

    with open(r'C:\GIT_HUB\WEB1.1.HomeAssignment_8\qoutes.json', 'r', encoding='utf-8') as file:
        quotes_data = json.load(file)

    # Store data in MongoDB
    for author_data in authors_data:
        # Update the date format and convert the born_date string to a string
        born_date_str = author_data.get('born_date')
        if born_date_str:
            author_data['born_date'] = born_date_str  # Keep it as a string for StringField

        author = Author(**author_data)
        author.save()

    for quote_data in quotes_data:
        author = Author.objects(fullname=quote_data['author']).first()
        if 'author' in quote_data:
            del quote_data['author']  # Remove 'author' key if present
        quote = Quote(author=author, **quote_data)
        quote.save()

if __name__ == '__main__':
    main()
