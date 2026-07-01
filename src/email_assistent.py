import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY')

headers = {
  'Content-Type': 'application/json',
  'Authorization': f'Bearer {OPENROUTER_API_KEY}'
}

data = {
  'model': 'openrouter/free',
  'messages': [
    {
      'role': 'user',
      'content': 'How many r\'s are in the word \'strawberry\'?'
    }
  ]
}

response = requests.post('https://openrouter.ai/api/v1/chat/completions', headers=headers, json=data)
response_json = response.json()

print(f'Role: {response_json['choices'][0]['message']['role']}: {response_json['choices'][0]['message']['content']}')