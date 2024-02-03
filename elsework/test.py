import assemblyai as aai
from assemblyai.extras import MicrophoneStream
import os

# Read the API key from the file
api_key_file_path = os.path.join(os.path.dirname(__file__), 'api_key.txt')

if os.path.exists(api_key_file_path):
    with open(api_key_file_path, 'r') as file:
        api_key = file.read().strip()
    os.environ["ASSEMBLYAI_API_KEY"] = api_key
else:
    print("Error: API key file 'api_key.txt' not found.")
    exit()

def on_data(transcript: aai.RealtimeTranscript):
    if not transcript.text:
        return

    if isinstance(transcript, aai.RealtimeFinalTranscript):
        print(transcript.text, end="\r\n")
    else:
        print(transcript.text, end="\r")

def on_error(error: aai.RealtimeError):
    print("An error occurred:", error)

def on_open(session_opened: aai.RealtimeSessionOpened):
    print("Session ID:", session_opened.session_id)

def on_close():
    print("Closing Session")

transcriber = aai.RealtimeTranscriber(
    on_data=on_data,
    on_error=on_error,
    sample_rate=44_100,
    on_open=on_open,
    on_close=on_close,
)

transcriber.connect()
microphone_stream = MicrophoneStream()
transcriber.stream(microphone_stream)
transcriber.close()
