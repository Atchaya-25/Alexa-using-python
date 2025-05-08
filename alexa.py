import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import requests

#sReplace with your actual SerpAPI key
SERP_API_KEY = "3bc6d56ea1322e8c2a5daf332b7b70056a441c0aeca3e9d28b042a6609916ded"

# Initialize speech recognizer and text-to-speech engine
listener = sr.Recognizer()
engine = pyttsx3.init()
voice = engine.getProperty('voices')
engine.setProperty('voice', voice[1].id)

def talk(text):
    """Speaks the given text."""
    engine.say(text)
    engine.runAndWait()

def take_command():
    """Listens to the user's voice command and returns the text."""
    command = ""
    try:
        with sr.Microphone() as source:
            print("Listening.....")
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            command = command.lower()
            if 'alexa' in command:
                command = command.replace('alexa', '').strip()
                print("User Command:", command)
    except:
        pass
    return command

def search_google(query):
    """Fetches a detailed answer from Google Search API and reads it aloud."""
    try:
        url = f"https://serpapi.com/search.json?q={query}&api_key={SERP_API_KEY}"
        response = requests.get(url)
        data = response.json()

        # Check for Answer Box (Direct Answer)
        if "answer_box" in data and "snippet" in data["answer_box"]:
            answer = data["answer_box"]["snippet"]
        elif "organic_results" in data and len(data["organic_results"]) > 0:
            # Fetch multiple results to get more lines
            answers = [result["snippet"] for result in data["organic_results"][:3] if "snippet" in result]
            answer = " ".join(answers)  # Combine multiple snippets
        else:
            answer = "Sorry, I couldn't find a detailed answer."

        # Ensure at least 15 lines by repeating important content
        if len(answer.split('. ')) < 10:
            answer = answer + " " + answer  

        print("Answer:", answer)
        talk(answer)
        return answer

    except Exception as e:
        print("Error fetching search results:", e)
        talk("I couldn't get an answer from Google.")
        return "Error"

def run_alexa():
    command = take_command()
    print("Command Received:", command)

    if 'play' in command:
        song = command.replace('play', '').strip()
        talk('Playing ' + song)
        pywhatkit.playonyt(song)

    elif 'time' in command:
        time = datetime.datetime.now().strftime("%I:%M %p")
        talk('Current time is ' + time)
        print("Current Time:", time)

    # Check for question-based keywords and search Google
    elif command.startswith(('who is', 'tell me about', 'what', 'how', 'which', 'where', 'name', 'number of', 'when')):
        search_google(command)

    else:
        talk("I didn't catch that. Can you repeat?")

# Run Alexa

run_alexa()
