from dotenv import load_dotenv
import os 
import logging
import sys 

load_dotenv()

logging.disable(sys.maxsize)
CLIENT_ID = os.environ.get('FLOCKFYSH_CLIENT_ID', None)