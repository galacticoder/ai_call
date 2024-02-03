import assemblyai as aai
from transformers import GPT2LMHeadModel, GPT2Tokenizer

try:
    model_name = "gpt2-xL"
    tokenizer = GPT2Tokenizer.from_pretrained(model_name)
    model = GPT2LMHeadModel.from_pretrained(model_name)

    with open('params.txt', 'r') as file:
        lines = file.readlines()
        api_key = lines[0].strip()
        audio_path = lines[1].strip()

    aai.settings.api_key = api_key
    transcriber = aai.Transcriber()

    transcript = transcriber.transcribe(audio_path)

    user_input = transcript.text  # Extract text from the transcript object

    print(transcript.text)

    def generate_response(prompt, max_length=100, temperature=0.7):
        input_ids = tokenizer.encode(prompt, return_tensors="pt")
        
        output = model.generate(
            input_ids,
            max_length=max_length,
            temperature=temperature,
            num_beams=5,
            no_repeat_ngram_size=2,
            top_k=50,
            top_p=0.95,
            early_stopping=True
        )

        response = tokenizer.decode(output[0], skip_special_tokens=True)
        return response

    response = generate_response(user_input)
    print("AI Response:", response)

except FileNotFoundError:
    print("Error finding file path of audio")
