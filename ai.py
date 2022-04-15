from neuralintents import GenericAssistant
import speech_recognition
import pyttsx3 as tts
import sys
import requests
import json


recognizer = speech_recognition.Recognizer()

speaker = tts.init()

speaker.setProperty("rate", 100)

todo_list = ["Making Coffee", 'Drinking Coffee', 'Learn Some new', 'Listen music']

def create_note():
    global recognizer

    speaker.say("What do you want to write onto your note Sir")
    speaker.runAndWait()

    done = False

    while not done:
        try:

            with speech_recognition.Microphone() as mic:

                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audio = recognizer.listen(mic)

                note = recognizer.recognize_google(audio)
                note = note.lower()

                speaker.say("Please tell me the file name Sir")
                speaker.runAndWait()

                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audio = recognizer.listen(mic)

                filename = recognizer.recognize_google(audio)
                filename = filename.lower()

            with open(filename, 'w') as f:
                f.write(note)
                done = True
                speaker.say(f"I'm been created {filename} Sir")
                speaker.runAndWait()

        except speech_recognition.UnknownValueError:
            recognizer = speech_recognition.Recognizer()
            speaker.say("I don't understand Sir")
            speaker.runAndWait()

def add_todo():

    global recognizer

    speaker.say("What do you want to add?, Sir")
    speaker.runAndWait()

    done = False

    while not done:

        try:

            with speech_recognition.Microphone() as mic:

                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audio = recognizer.listen(mic)

                item = recognizer.recognize_google(audio)
                item = item.lower()

                todo_list.append(item)

                done = True

                speaker.say(f"I added {item} to the to do list")
                speaker.runAndWait()
        except speech_recognition.UnknownValueError:
            recognizer = speech_recognition.Recognizer()
            speaker.say("I don't understand.")
            speaker.runAndWait()

def show_todos():

    speaker.say("Your items are")
    for item in todo_list:
        speaker.say(item)
    speaker.runAndWait()

def hello():
    speaker.say("Hi Sir, How can I help you.")
    speaker.runAndWait()

def quit():
    r = requests.get('https://api.lyrics.ovh/v1/imagine dragons/demon')
    i = json.loads(r.text)
    speaker.say(str(i["lyrics"]))
    speaker.runAndWait()

mappings = {
    "greeting": hello,
    "create_note": create_note,
    "add_todo": add_todo,
    "show_todos": show_todos,
    "exit": quit
}


assistant = GenericAssistant('ai.json', intent_methods=mappings)
assistant.train_model()

while True:

    try:

        with speech_recognition.Microphone() as mic:

            recognizer.adjust_for_ambient_noise(mic, duration=0.2)
            audio = recognizer.listen(mic)

            message = recognizer.recognize_google(audio)
            message = message.lower()

        assistant.request(message)

    except speech_recognition.UnknownValueError:
        recognizer = speech_recognition.Recognizer()








