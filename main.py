from ast import arguments
import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import webbrowser
import os
import time
import subprocess
from ecapture import ecapture as ec
import wolframalpha
import json
import sys
import requests
import tkinter
from tkinter import messagebox



engine=pyttsx3.init('sapi5')
voices=engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
root = tkinter.Tk()
root.withdraw()





# Interaction fonctions

def speak(text):
    print(f"[i] {text}\n")
    engine.say(text)
    engine.runAndWait()

def ask(text):
    speak(text)
    return takeCommand()

def wishMe():
    strTime=datetime.datetime.now().strftime("%H:%M:%S")
    speak(f"Bonjour, je suis votre assistant personnel, il est {strTime}")

def takeCommand(say = None):
    if say:
        speak(say)
    r = sr.Recognizer()
    microphone = sr.Microphone()
    with microphone as source:
        print("Je vous écoute ...\n")
        r.pause_threshold = 1
        audio = r.listen(source)
        try:
            r.adjust_for_ambient_noise(source)
            statement=r.recognize_google(audio, language='fr-FR')
            print(f"[i] Vous avez dit : {statement}\n")

        except Exception as e:
            # speak("Pardonnez-moi")
            return "None"

        return statement

# Configuration fonctions

def get_config():
    try:
        with open('config.json') as f:
            data = json.load(f)
            return data
    except:
        return None

def setup_config():
    config = get_config()
    if config:
        return config
    else:
        config = {
            "start_keyword" : None
        }
        with open('config.json', 'w') as f:
            json.dump(config, f)
        return config
    
def configure_keyword():
    config = setup_config()
    if config['start_keyword']:
        return config['start_keyword']
    else:
        config['start_keyword'] = ask("Quel est le mot clé pour démarrer votre assistant personnel ?").lower()
        with open('config.json', 'w') as f:
            json.dump(config, f)
        return config['start_keyword']

def config(key):
    config = setup_config()
    return config[key]


if __name__=='__main__':

    args = sys.argv
    
    configure_keyword()

    if len(args) > 1:
        if "--no-intro" not in args:
            speak("Chargement de votre assistant personnel...")
            wishMe()
            speak(f"Le mot clé est {config('start_keyword')}")

    speak("Dites-moi comment puis-je vous aider ?")

    while True:

        try:

            statement = takeCommand().lower()
            print(statement.startswith(config('start_keyword')), statement, config('start_keyword'))
            if statement.startswith(config('start_keyword')):
                statement = statement.replace(config('start_keyword'), '')

                if statement==0:
                    continue

                if "good bye" in statement or "ok bye" in statement or "stop" in statement:
                    speak("Au revoir, à bientôt")
                    break

                if 'wikipedia' in statement:
                    speak("Recherche de wikipedia...")
                    statement=statement.replace("wikipedia", "")
                    result=wikipedia.summary(statement, sentences=2)
                    speak("Voici le résultat de votre recherche : ")
                    speak(result)

                elif "none" == statement:
                    pass

                elif 'youtube' in statement:
                    speak("Recherche de youtube...")
                    statement=statement.replace("youtube", "")
                    webbrowser.open("https://www.youtube.com/results?search_query="+statement)
                    # time.sleep(5)

                elif 'google' in statement:
                    speak("Recherche de google...")
                    statement=statement.replace("google", "")
                    webbrowser.open("https://www.google.com/search?q="+statement)
                    # time.sleep(5)

                elif 'ouvre gmail' in statement:
                    speak("Ouverture de gmail...")
                    webbrowser.open("https://mail.google.com/mail/u/0/#inbox")
                    # time.sleep(5)

                elif "météo" in statement:
                    api_key="8ef61edcf1c576d65d836254e11ea420"
                    base_url="https://api.openweathermap.org/data/2.5/weather?"
                    speak("Recherche de la météo...")
                    city_name = takeCommand("Quel est votre ville ?")
                    complete_url=base_url+"appid="+api_key+"&q="+city_name
                    response = requests.get(complete_url)
                    x=response.json()
                    if x["cod"]!="404":
                        y=x["main"]
                        current_temperature = y["temp"]
                        current_humidiy = y["humidity"]
                        z = x["weather"]
                        weather_description = z[0]["description"]
                        speak("Temperature : " + str(current_temperature) + "°C")
                        speak("Humidité : " + str(current_humidiy) + "%")
                        speak("Description : " + str(weather_description))
                    else:
                        speak("Ville non trouvée.")



                elif 'heure' in statement:
                    strTime=datetime.datetime.now().strftime("%H:%M:%S")
                    speak(f"Il est {strTime}")

                elif "stackoverflow" in statement:
                    speak("Recherche de stackoverflow...")
                    statement=statement.replace("stackoverflow", "")
                    webbrowser.open("https://stackoverflow.com/search?q="+statement)
                    # time.sleep(5)

                elif 'recherche' in statement:
                    statement = statement.replace("search", "")
                    # webbrowser.open_new_tab(statement)
                    webbrowser.open("https://www.google.com/search?q="+statement)
                    # time.sleep(5)

                elif 'ask' in statement:
                    speak('I can answer to computational and geographical questions and what question do you want to ask now')
                    question=takeCommand()
                    app_id="R2K75H-7ELALHR35X"
                    client = wolframalpha.Client('R2K75H-7ELALHR35X')
                    res = client.query(question)
                    answer = next(res.results).text
                    speak(answer)


                elif "éteins" in statement or "déconnexion" in statement:
                    speak("Ok , your pc will log off in 10 sec make sure you exit from all applications")
                    subprocess.call(["shutdown", "/l"])

                elif "visual studio" in statement:
                    subprocess.call(["C:\\Users\\Asus\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"])

                else:
                    ask = messagebox.askyesno("Que faire ?", "Souhaitez-vous rechercher " + statement + " sur google ?")
                    if ask:
                        webbrowser.open("https://www.google.com/search?q=" + statement)

        except Exception as e:
            speak("Une erreur est survenue")
            print(f"[x] {e}")

# time.sleep(3)











