import shutil
import requests
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import os
import assemblyai as aai
import speech_recognition as sr
from gtts import gTTS
import torch
from email_sender import *
from mutagen.mp3 import MP3
import time

#if getting corrupt mp3 output then api is out of words

with open("C:\\Users\\zombi\\OneDrive\\Desktop\\ai_call\\ai_call\\api.txt", "r") as api_file:
    lines = api_file.readlines()
    api_key = lines[0].strip()
    voice_id = lines[1].strip()
    ai_path = lines[3].strip()
    user_path = lines[4].strip()
    api_assembly = lines[5].strip()

try:
    def get_audio():
        r = sr.Recognizer()
        with sr.Microphone() as source:
            audio = r.listen(source)
            said = ""

            try:
                said = r.recognize_google(audio)
                print(said)
            except Exception as e:
                print("You didnt say anything")
                exit()

        return said

    print("speak nigga we recording\n")
    text = get_audio()
    print("\nshut up nigga we not recording")

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

    user_input = text

    input_ids = tokenizer.encode(user_input, return_tensors="pt")
    attention_mask = torch.ones(input_ids.shape, device=input_ids.device)  # Add this line to create attention mask

    with torch.no_grad():
        output = model.generate(input_ids, max_length=300, num_return_sequences=1, no_repeat_ngram_size=2, attention_mask=attention_mask)
        
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

except IndexError:
    print("No input given you didnt say anything")