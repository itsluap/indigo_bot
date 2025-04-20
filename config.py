import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Bot Configuration
BOT_TOKEN = os.getenv('DISCORD_TOKEN')
BOT_PREFIX = '!'  # Default prefix for commands

# Debug Configuration
DEBUG = False  # Set to True to enable debug mode

# Role IDs (to be filled in)
ADMIN_ROLE_ID = None
MODERATOR_ROLE_ID = None

# Channel IDs (to be filled in)
WELCOME_CHANNEL_ID = None
LOGS_CHANNEL_ID = None

# FiveM Server Configuration
FIVEM_SERVER_IP = os.getenv('FIVEM_SERVER_IP', '')
FIVEM_SERVER_PORT = os.getenv('FIVEM_SERVER_PORT', '30120') 