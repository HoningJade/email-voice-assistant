import os
import sys
import json
import speech_recognition as sr
from gtts import gTTS
from pydub import AudioSegment


def get_keywords() -> set():

    with open("keywords.txt") as keywords_file:
        keywords = set(line.strip() for line in keywords_file.readlines())
    return keywords

def audio2text(audio_file : str, verbose : bool = False) -> str:

    r = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio_text = r.listen(source)
        try:
            text = r.recognize_google(audio_text)
            if verbose:
                print('Converting audio transcripts into text ...')
                print(text)
        except:
            print('Sorry.. run again...')
    return text

def text2query(text : str, keywords : set) -> dict:
    
    def preprocess(word : str) -> str:
        return word.lower()
    
    query = dict()
    for word in text.split(' '): # FIXME:
        word = preprocess(word)
        if word in keywords:
            query[word] = query.get(word, 0) + 1

    return query

def text2audio(text : str, save_file : str, language="en", slow=False):
    
    audio_obj = gTTS(text=text, lang=language, slow=slow)
    ext = os.path.splitext(save_file)[-1]
    if ext.lower() == ".mp3":
        audio_obj.save(save_file)
    elif ext.lower() == ".wav":
        audio_obj.save("/tmp/tmp.mp3")
        sound = AudioSegment.from_mp3("/tmp/tmp.mp3")
        sound.export(save_file, format="wav")
    else:
        print("Unsupported format, available formats are mp3 and wav", file=sys.stderr)
        raise NotImplementedError

if __name__ == '__main__':

    # keywords = get_keywords()
    # for root, dirs, files in os.walk("input_audio"):
    #     for file in files:
    #         realpath = os.path.join(root, file)
    #         basename = os.path.splitext(file)[0]
    #         print("* Processing input audio file "+realpath)
    #         transcript = audio2text(realpath, True)
    #         query = text2query(transcript, keywords)
    #         with open(os.path.join("output_query", basename+".json"), 'w') as input_query_file:
    #             json.dump(query, input_query_file, indent=4)

    text = "Your PhD advisor is asking whether you have any updates this week."
    text2audio(text, os.path.join("output_audio", "summary.wav"))

