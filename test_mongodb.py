# This code is copied from Mongodb Atlas cluster that I have created for this project
# click on the cluster -> connect-> drivers -> view full code sample
# for password do this: Quickstart -> choose username and password -> Create user. then copy the uri to .env file

# NOTE: ping does not work on codespace. otherwise, install ping for testing mongo db
#  sudo apt update && sudo apt install iputils-ping -y

# whitelist your ip, otherwise ssl handshake will fail!
# get the ip: 20.61.126.213
# copy it to Mongodb Atlas -> network access -> add ip address or click on allow access from anywhere



from pymongo.mongo_client import MongoClient
import os

uri = os.getenv("MONGO_DB_URL")

# Create a new client and connect to the server
client = MongoClient(uri)

# Send a ping to confirm a successful connection
try:
    databases = client.admin.command('ping')
    print("Successfully connected to MongoDB! Available databases:", databases)
except Exception as e:
    print(e)