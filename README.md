# Text-to-Speech AI with GPT-2

This Python script utilizes the GPT-2 language model for text-to-speech conversion. It captures audio input, converts it into text using Google Speech Recognition, generates extended text with GPT-2, and then converts the generated text into an AI voice using an external API. The generated audio is saved as an MP3 file, emailed as an attachment, and played locally.

## Prerequisites

Before running the script, make sure to have the following dependencies installed:

- `shutil`
- `requests`
- `transformers`
- `os`
- `speech_recognition`
- `torch`
- `email_sender` (please make sure this module is available)
- `mutagen`

## Usage

1. Ensure the required dependencies are installed by running:

   ```bash
   pip install -r requirements.txt
   ```
   If that doesn't work, you can install manually by running:
   ```bash
   pip install shutil requests transformers torch email_sender mutagen SpeechRecognition
   
2. Create the `api.txt` file:

   An API key, voice ID, and file path configurations should be provided in the `api.txt` file in this order:
   **line 1**  | **Your [eleven labs](https://elevenlabs.io/) api key**
   ------------- | -------------
   **line 2** | **Your voice id from eleven labs**
   **line 3**  | **Your path to the `ai_call/audios/ai_audio`**

Run the script and Speak into the microphone when prompted, and the script will generate AI audio output based on your speech.

## Configuration

Adjust the following parameters in the script according to your preferences(not nesessary):

- `model_name`: The GPT-2 model name.
- `max_length`: Maximum length of the generated text.
- `num_return_sequences`: Number of generated sequences.
- `stability` and `similarity_boost`: Adjust voice settings in the data dictionary.
- `sender_email`, `sender_password`, and `recipient_email`: Configure email details for sending the AI output.

**Note:** Make sure to not show anyone else sensitive information like API keys.

## Important Notes

- If the generated MP3 output is corrupted, it may indicate that the API is out of words.
- If no input is given during the speech recognition stage, the script will print a corresponding message and exit.

Feel free to customize and integrate this script into your projects for enhanced text-to-speech capabilities using GPT-2.

Updates to the ai model in the future will be coming using better models
