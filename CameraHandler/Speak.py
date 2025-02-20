from gtts import gTTS
import os

def text_to_speech(text, language='en', filename='output.mp3', play=True):
    tts = gTTS(text=text, lang=language, slow=False)
    tts.save(filename)
    if play:
        os.system("mpg321 output.mp3")
    # os.remove(filename)  

if __name__ == "__main__":
    text_to_speech("Hello, how are you?")