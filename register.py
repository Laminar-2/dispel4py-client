from client import d4pClient
import os

client = d4pClient()
user_name = os.getenv('LAMINAR_USERNAME')
user_password  = os.getenv('LAMINAR_PASSWORD')
if user_name is not None and user_password is not None:
    client.register(user_name, user_password)
else:
    print("Failed to register user")
