# Covexa
# 
# By Team Covexa

import pyttsx3
import webbrowser
import speech_recognition as speech
import wikipedia
import pygame as pg
from time import sleep

# Initializing Covexa
class Covexa():
    def __init__(self):
        # Initializing speech output
        self.engine = pyttsx3.init()
        
        # Initializing pygame window size
        self.width = 550
        self.height = 540
        self.size = (self.width, self.height)
        
        # Variable that controls if the main loop is running or not
        self.running = True
        
        # Registering chrome
        self.chrome_path = "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"
        webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(self.chrome_path))
        
        # Dialogues list
        self.dialogues = {"a": "It is a new virus, tramsmitted to humans by bats.",
                          "b": "Quarantine yourself if having symptoms or if you are in a city with any reported cases.",
                          "c": 'Covid-19 transmits through mucous droplets that are sprayed into the air while sneezing or coughing.',
                          'd': "Coronavirus originated in Wuhan, Hubei Province, China.",
                          'e': "Symptoms of Coronavirus include cough, fever, chills, headache, tiredness, and trouble breathing.",
                          'f': "Use alcohol-based hand sanitizer and rub thoroughly after coming in contact with any object which could be contaminated.",
                          'g': "For regular updates on Covid-19 from the World Health Organization, Send 'hi' to + 4 1, 7 9 8, 9 3 1, 8 9 2 on WhatsApp.",
                          'h': "Use N-95 masks, if possible. Surgical masks and hankercheifs are not very useful against the Coronavirus.",
                          'i': "Wash your hands with soap",
                          'j': "Starting Coronavirus test. Please answer the questions honestly as yes or no.", 
                          'web': "Opening website.",
                          'z': "Hope you are well. Goodbye"}
        
        # Coronavirus test questions
        self.questions = ["Do you have cough?",
                          "Do you have a cold?",
                          "Are you suffering from diarrhea?",
                          "Do you have a sore throat?",
                          "Are you experiencing body aches?",
                          "Do you have a headache?",
                          "Do you have a body temperature over 37.8 degrees Celsius?",
                          "Are you having difficulty breathing?",
                          "Are you experiencing fatigue?",
                          "Have you travelled anywhere in the past 2 weeks?",
                          "Have you travelled to a COVID-19 affected Area?",
                          "Have you come into contact with or do you take care of a Coronavirus patient?"]
        
        # Score/question
        self.weight = [1, 1, 1, 1, 1, 1, 1, 2, 2, 3, 3, 3]
        
        # Initializing stuff
        self.speech_init()
        pg.init()
        pg.mixer.quit()
        
        # Opening pygame window
        self.screen = pg.display.set_mode(self.size)
        pg.display.set_caption('Covexa')
        
    def speech_init(self):
        # Initializing speech output
        # Speed
        self.engine.setProperty('rate', 175)
        # Volume
        self.engine.setProperty('volume' , 2)
        # Accent and Gender
        voices = self.engine.getPropertyvoices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[0].id)
        
    def speech_output(self, x):
        self.engine.say(x)
        self.engine.runAndWait()
    
    def change_screen(self, image):
        # Changes background of the Pygame window.
        # Graphics are shown as screens set to background, instead of sprites.
        bg = pg.image.load(image + ".png").convert_alpha()
        self.screen.blit(bg,(0,0))
            
    def start_listening(self):
        # Voice recognition
        global command
        try:
            r = speech.Recognizer() 
            with speech.Microphone() as source:
                    r.adjust_for_ambient_noise(source, 0.2)
                    self.speech_output("Say something")
                    audio = r.listen(source)
            command = r.recognize_google(audio)
            self.speech_output("You said: " + command)
        # Dealing with incoherent input
        except speech.UnknownValueError:
            self.speech_output("Sorry, I didn't get that. Try again.")
            self.start_listening()
        return str(command)
    
    def test(self):
        self.score = 0
        for x in range(0, 12):
            self.speech_output(self.questions[x])
            userinp = self.start_listening()
            w = self.weight[x]
            if userinp == "yes":
                self.score = self.score + w  
            elif userinp == "no":
                self.score = self.score + 0
        
        self.speech_output("Your score is " + str(self.score))
        
        if self.score==0:
            print("You're fine. Congatulations!")
            
        elif self.score == 2 or self.score == 1:  
            print("This very likely is just an allergy or stress. Observe your symptoms for a few days, but don't worry too much.")
            
        elif self.score <= 5 and self.score >= 3:
            print("Drink lots of water and wash your hands often. Watch your symptoms and be careful.")
            
        elif self.score <= 6 and self.score >= 12:
            print ("Consult a doctor when possible. Quarantine yourself.")
            
        elif self.score < 12 and self.score >24:
            print("You are at risk of COVID-19. Quarratine yourself." '''Call 0 2. 8. 6 5 1. 7 8 0 0.''')
            
        elif self.score == 24:
            print("You are at a very high risk of COVID-19. Quarratine yourself immediately. Call 0 2. 8. 6 5 1. 7 8 0 0.")
            
        elif self.score > 24:
            print("bup")        
    
    def run(self):
        # Startup
        # Setting screen
        self.change_screen('bg1')
        sleep(2)
        # Opening dialogue
        x = "I am covexa, your coronavirus help bot"
        self.speech_output(x)
        x = "Ask me any questions you have related to Coronavirus."
        self.speech_output(x)
        x = "If you want to exit, say 'bye'."
        self.speech_output(x)
        self.userinp = self.start_listening()
        while self.running:
            self.take_input(self.userinp)
        
    def take_input(self, userinp):
        
        if "coronavirus" in userinp:
            self.change_screen('bg4')
            y = wikipedia.summary(userinp, sentences = 2)
            try: 
                self.speech_output(y)
                userinp = self.start_listening()
            except wikipedia.DisambiguationError:
                pass
        
        if "prevention" in userinp:
            x = self.dialogues['b']
            self.speech_output(x)
            a = "https://www.who.int/emergencies/diseases/novel-coronavirus-2019/advice-for-public"
            x = self.dialogues['web']
            self.speech_output(x)        
            self.open_website(a)
            userinp = self.start_listening()
            
        if "mask" in userinp:
            x = self.dialogues['h']
            self.speech_output(x)
            userinp = self.start_listening()
        
        if "transmission" in userinp:
            x = self.dialogues['c']
            self.speech_output(x)
            userinp = self.start_listening()
        
        if "origin" in userinp:
            self.change_screen('bg5')
            x = self.dialogues['d']
            self.speech_output(x)
            userinp = self.start_listening()
            
        if "symptoms" in userinp:
            self.change_screen('bg3')
            x = self.dialogues['e']
            self.speech_output(x)
            userinp = self.start_listening()
            
        if "updates" in userinp:
            self.change_screen('bg7')
            x = self.dialogues['g']
            self.speech_output(x)
            b = "https://www.arcgis.com/apps/opsdashboard/index.html#/bda7594740fd40299423467b48e9ecf6"
            x = self.dialogues['web']
            self.speech_output(x)        
            self.open_website(b)
            userinp = self.start_listening()
        
        if "sanitizer" in userinp:
            x = self.dialogues['f']
            self.speech_output(x) 
            userinp = self.start_listening()
            
        if "test" in userinp:
            x = self.dialogues['j']
            self.test()
            
        if "bye" in userinp:
            pg.quit()
            self.running = False
        else:
            x = "I don't know the answer to that question"
            self.speech_output(x)
            userinp = self.start_listening()
    
#
# Main loop
#

Cov = Covexa()

while Cov.running:
    Cov.run()
