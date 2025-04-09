from dotenv import find_dotenv, load_dotenv, dotenv_values
import os

# Load the .env file first
env_path = find_dotenv()
print(f"Found .env file at: {env_path}")
load_dotenv(env_path, override=True)

# Now get environment variables
print("MET_CLIENT_ID:", os.getenv("MET_CLIENT_ID"))
print("MET_CLIENT_SECRET:", os.getenv("MET_CLIENT_SECRET"))

# Optional: show raw values from the file
config = dotenv_values(env_path)
print("=== Variables loaded from .env ===")
for key, value in config.items():
    print(f"{key} = {value}")
