import shutil
import requests
from transformers import BertTokenizer, BertForCausalLM
import os
import assemblyai as aai
import speech_recognition as sr
from gtts import gTTS
import torch
from email_sender import *
from mutagen.mp3 import MP3
import time

# Load BERT model and tokenizer
model_name = "bert-base-uncased"
model = BertForCausalLM.from_pretrained(model_name)
tokenizer = BertTokenizer.from_pretrained(model_name)

# Load API and paths from file
with open("C:\\Users\\zombi\\OneDrive\\Desktop\\ai_call\\ai_call\\api.txt", "r") as api_file:
    lines = api_file.readlines()
    api_key = lines[0].strip()
    voice_id = lines[1].strip()
    ai_path = lines[3].strip()
    user_path = lines[4].strip()
    api_assembly = lines[5].strip()

def get_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        said = ""

        try:
            said = r.recognize_google(audio)
            print(said)
        except Exception as e:
            print("Exception: " + str(e))

    return said

print("Speak, we are recording\n")
text = get_audio()
print("\nStop recording, processing...")

# Tokenize and encode input for BERT
user_input = text
input_ids = tokenizer.encode(user_input, return_tensors="pt", max_length=300, truncation=True)

# Model inference
output = model.generate(input_ids, max_length=300, num_return_sequences=1)
generated_text = tokenizer.decode(output[0], skip_special_tokens=True)


data = {
    "text": generated_text,
    "model_id": "eleven_monolingual_v1",
    "voice_settings": {
        "stability": 0.75,
        "similarity_boost": 0.86
    }
}

response = requests.post(url, json=data, headers=headers)

with open('ai_output.mp3', 'wb') as f:
    f.write(response.content)

shutil.move('ai_output.mp3', ai_path)
os.system("start "+ai_path+"\\ai_output.mp3")

send_email(sender_email="galacticoderr@gmail.com",
           sender_password="jlnw esrt tjlu bnfp",
           recipient_email='someonedmta@gmail.com',
           subject="Ai Output",
           message='ai output',
           attachment_path=ai_path+"\\ai_output.mp3"
)

audio = MP3(ai_path+"\\ai_output.mp3")
a_l = audio.info.length

time.sleep(a_l)
os.remove(ai_path+"\\ai_output.mp3")
