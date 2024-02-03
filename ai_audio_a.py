import os
import subprocess
import shutil
import requests
from transformers import GPT2LMHeadModel, GPT2Tokenizer

# Read the API key and voice ID from the api.txt file
with open("api.txt", "r") as api_file:
    lines = api_file.readlines()
    api_key = lines[0].strip()
    voice_id = lines[1].strip()  # Read the voice ID from the second line

# Load GPT-2 model and tokenizer
model_name = "gpt2-xL"
model = GPT2LMHeadModel.from_pretrained(model_name)
tokenizer = GPT2Tokenizer.from_pretrained(model_name)

# Set up Eleven Labs API
CHUNK_SIZE = 1024
url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"

headers = {
    "Accept": "audio/mpeg",
    "Content-Type": "application/json",
    "xi-api-key": api_key
}

# Get user input and generate response using GPT-2
user_input = input("User: ")
input_ids = tokenizer.encode(user_input, return_tensors="pt")
output = model.generate(input_ids, max_length=50, num_return_sequences=1, no_repeat_ngram_size=2)
generated_text = tokenizer.decode(output[0], skip_special_tokens=True)

# Set up Eleven Labs TTS data
data = {
    "text": generated_text,
    "model_id": "eleven_monolingual_v1",
    "voice_settings": {
        "stability": 0.65,
        "similarity_boost": 0.86
    }
}

# Make TTS request and save audio
response = requests.post(url, json=data, headers=headers)
with open('output.mp3', 'wb') as f:
    for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
        if chunk:
            f.write(chunk)

# Play the audio using the mpv command-line player
subprocess.run(["mpv", "output.mp3"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# Move the MP3 file to the destination directory
destination_directory = os.path.expanduser("C:\\Users\\zombi\\OneDrive\\Desktop\\ai_call\\audios\\user_inputs")
os.makedirs(destination_directory, exist_ok=True)

base_filename = "output.mp3"
destination_path = os.path.join(destination_directory, base_filename)
counter = 1

while os.path.exists(destination_path):
    filename, ext = os.path.splitext(base_filename)
    destination_path = os.path.join(destination_directory, f"{filename}_{counter}{ext}")
    counter += 1

shutil.move("output.mp3", destination_path)
