# search_quotes.py

from mongoengine import connect
from main import Quote, Author
from pymongo import MongoClient

def main():
    connection_string = 'mongodb+srv://soboleva13as:5413034002246@cluster0.xpt2wff.mongodb.net/web8'

    # Check the connection using pymongo
    try:
        pymongo_client = MongoClient(connection_string)
        pymongo_client.admin.command('ping')
        print("Pinged MongoDB using pymongo. Connection successful!")
    except Exception as e:
        print("Error connecting to MongoDB using pymongo:", e)

    # Connect using mongoengine
    connect(db='web-8', username='soboleva13as', password='5413034002246',
            host='mongodb+srv://soboleva13as:5413034002246@cluster0.xpt2wff.mongodb.net/web8')
    while True:
        user_input = input("Enter command (name:<author>, tag:<tag>, tags:<tag1,tag2>, exit): ").split(':')

        if user_input[0] == 'exit':
            break
        elif user_input[0] == 'name':
            author_name = user_input[1].strip()
            # Find the author separately
            author = Author.objects(fullname=author_name).first()
            if not author:
                print(f"No author found with name: {author_name}")
                continue
            # Query quotes using the found author
            quotes = Quote.objects(author=author)
        elif user_input[0] == 'tag':
            tag = user_input[1].strip()
            quotes = Quote.objects(tags=tag)
        elif user_input[0] == 'tags':
            tags = [t.strip() for t in user_input[1].split(',')]
            quotes = Quote.objects(tags__in=tags)
        else:
            print("Invalid command. Please try again.")
            continue

        for quote in quotes:
            print(f"{quote.author.fullname}: {quote.quote}")

    print("Script execution ended.")

if __name__ == "__main__":
    main()
