# For accessing environment variables frm .env file:
import os
from dotenv import load_dotenv   

## Constants: ##
load_dotenv()

# our OpenAI key:
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

# TODO: Generate tree from taxonomy spreadsheet
# TODO: run graph
# TODO: handle output
