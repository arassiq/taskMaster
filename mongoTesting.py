import os
from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

class MongoConnect:

    def __init__(self):
        load_dotenv()
        self.mongoPassword = os.getenv("MONGODBPASSWORD")
        self.uri = f"mongodb+srv://amrassiq:{self.mongoPassword}@testing.dth0i.mongodb.net/?retryWrites=true&w=majority&appName=Testing"

        # Create a new client and connect to the server
        self.client = MongoClient(self.uri, server_api=ServerApi('1'), tlsAllowInvalidCertificates=True)

    # Send a ping to confirm a successful connection
    def connect(self):
        try:
            self.client.admin.command('ping')
            print("Pinged your deployment. You successfully connected to MongoDB!")
        except Exception as e:
            print(e)

def main():
    mongoClient = MongoConnect()
    mongoClient.connect()

    db = mongoClient.client["testing"]
    collection = db["userChatLog"]

    data = {"user": "testUser", "chatHistory": "hai"}
    #collection.insert_one(data)

# Run this block only if the script is executed directly
if __name__ == "__main__":
    main()