import shutil
import requests
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import os

with open("C:\\Users\\zombi\\OneDrive\\Desktop\\ai_call\\ai_call\\api.txt", "r") as api_file:
    lines = api_file.readlines()
    api_key = lines[0].strip()
    voice_id = lines[1].strip()
    path = lines[3].strip()
    api_text = lines[4].strip()

model_name = "gpt2-xL"
model = GPT2LMHeadModel.from_pretrained(model_name)
tokenizer = GPT2Tokenizer.from_pretrained(model_name)

CHUNK_SIZE = 1024
url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"

headers = {
    "Accept": "audio/mpeg",
    "Content-Type": "application/json",
    "xi-api-key": api_key
}

user_input = input("User: ")
input_ids = tokenizer.encode(user_input, return_tensors="pt")
output = model.generate(input_ids, max_length=50, num_return_sequences=1, no_repeat_ngram_size=2)
generated_text = tokenizer.decode(output[0], skip_special_tokens=True)

data = {
    "text": generated_text,
    "model_id": "eleven_monolingual_v1",
    "voice_settings": {
        "stability": 0.65,
        "similarity_boost": 0.86
    }
}

response = requests.post(url, json=data, headers=headers)

with open('ai_output.mp3', 'wb') as f:
    for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
        if chunk:
            f.write(chunk)
            
shutil.move('ai_output.mp3', path)
os.system("start "+path+"\\ai_output.mp3")
