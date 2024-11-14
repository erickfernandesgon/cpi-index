import os
from dotenv import load_dotenv

# Load the .env file
load_dotenv()

# Retrieve the API key
api_key = os.getenv("BLS_API_KEY")  # Use the variable name, not the actual API key

print("Loaded API key:", api_key)
