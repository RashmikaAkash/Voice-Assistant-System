import speech_recognition as sr
import subprocess
import pywhatkit
import pyttsx3
import webbrowser
import logging
import os
import datetime
import requests

# Basic logging configuration
logging.basicConfig(level=logging.ERROR)

# Initialize text-to-speech engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

# Initialize recognizer
recognizer = sr.Recognizer()

# Get OpenWeatherMap API key from environment variables
api_key = os.getenv('OPENWEATHER_API_KEY')

def speak(text):
    engine.say(text)
    engine.runAndWait()

def get_weather(city):
    if not api_key:
        return "API key is missing. Please set up your OpenWeatherMap API key."
    
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    try:
        response = requests.get(url).json()
        if response['cod'] == 200:
            main = response['main']
            temp = main['temp']
            weather = response['weather'][0]['description']
            return f"The current temperature in {city} is {temp}°C with {weather}."
        else:
            return "Sorry, I couldn't get the weather data. Please check the city name."
    except Exception as e:
        return "There was an error fetching the weather data."

def get_answer(question):
    # Basic responses to frequently asked questions
    answers = {
        "your name": "I am your personal assistant created by Akash.",
        "creator": "I was created by Akash.",
        "how are you": "I'm doing great, thank you for asking!",
    }
    return answers.get(question.lower(), "Sorry, I don't know that one.")

def cmd():
    print("Voice Assistant is running. Say 'exit' or 'stop' to terminate.")
    while True:
        with sr.Microphone() as source:
            try:
                print('Clearing background noises... Please wait.')
                recognizer.adjust_for_ambient_noise(source, duration=0.5)
                print('Listening...')
                recorded_audio = recognizer.listen(source)

                # Recognize the audio
                print("Recognizing...")
                command = recognizer.recognize_google(recorded_audio).lower()
                print(f'You said: {command}')

                # Respond to commands
                if 'chrome' in command or 'open chrome' in command:
                    response = 'Opening Chrome now.'
                    speak(response)
                    program = r"C:/Program Files/Google/Chrome/Application/chrome.exe"
                    subprocess.Popen([program])

                elif 'youtube' in command or 'open youtube' in command:
                    response = 'Opening YouTube now.'
                    speak(response)
                    webbrowser.open("https://www.youtube.com")

                elif 'facebook' in command or 'open facebook' in command:
                    response = 'Opening Facebook now.'
                    speak(response)
                    webbrowser.open("https://www.facebook.com")

                elif 'my computer' in command or 'open my computer' in command:
                    response = 'Opening File Explorer now.'
                    speak(response)
                    os.startfile('explorer')

                elif 'time' in command:
                    now = datetime.datetime.now()
                    time = now.strftime("%H:%M")
                    response = f"The current time is {time}."
                    speak(response)

                elif 'weather' in command:
                    city = command.split('in')[-1].strip()
                    if city:
                        response = get_weather(city)
                    else:
                        response = "Please specify the city."
                    speak(response)

                elif 'play' in command and 'music' in command:
                    response = 'Playing some relaxing music for you.'
                    speak(response)
                    pywhatkit.playonyt("relaxing music")

                elif 'send a whatsapp' in command:
                    try:
                        command = command.split('send a whatsapp')[-1].strip()
                        number, message = command.split('to')[0].strip(), command.split('to')[-1].strip()
                        pywhatkit.sendwhatmsg_instantly(f"+{number}", message)
                        response = f"Sending message to {number}."
                    except Exception as e:
                        response = "Sorry, I couldn't send the WhatsApp message."
                    speak(response)

                elif 'shutdown' in command or 'exit' in command or 'stop' in command:
                    response = 'Shutting down the assistant. Goodbye!'
                    speak(response)
                    break

                elif 'who are you' in command or 'your name' in command:
                    response = get_answer("your name")
                    speak(response)

                elif 'how are you' in command:
                    response = get_answer("how are you")
                    speak(response)

                else:
                    response = "Sorry, I didn't understand that command."
                    speak(response)

            except sr.UnknownValueError:
                print("Sorry, I could not understand the audio.")
                speak("Sorry, I could not understand what you said. Please try again.")

            except sr.RequestError as e:
                print(f"Could not request results; {e}")
                speak("There seems to be a network issue. Please check your connection.")

            except Exception as ex:
                print(f"An error occurred: {ex}")
                speak("An error occurred. Please try again.")

# Run the function
cmd()
