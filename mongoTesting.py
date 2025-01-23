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
    jsonFormat= {
        "username" : "test",
        "chatLog": {

            "1" : "n/a",
            "2" : "n/a",
            "3" : "n/a",
            "4" : "n/a",
            "5" : "n/a"


        }

    }
    data = jsonFormat
    collection.insert_one(data)
    '''
    try:
        # Query the document with the matching username
        user_data = collection.find_one({"username": "test"})
        
        if user_data and "chatLog" in user_data:
            print(user_data["chatLog"])
        else:
            print(f"No chat log found for username: {"test"}")
            return None
    except Exception as e:
        print(f"Error retrieving chat log: {e}")
        return None

    #print(jsonFormat["chatLog"]["1"]) #returns hey (1 contents)
'''

# Example usage

# Run this block only if the script is executed directly
if __name__ == "__main__":
    main()