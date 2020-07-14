import time
import sys
import Adafruit_DHT
import speech_recognition as sr
from gtts import gTTS
import os

sensor = Adafruit_DHT.DHT11
pin = 4
r=sr.Recognizer()
    
def ReadData():
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
    if humidity is None or temperature is None:
        print('Failed to get reading. Try again!')
        sys.exit(1)
    print("Humidity:",humidity,"Temperature:",temperature)
    return humidity,temperature

with sr.Microphone() as source:
    print("Please wait.Calibrating microphone...")
    r.adjust_for_ambient_noise(source,duration=1)
    print("Say Command!")
    audio=r.listen(source)
    
print("Google Speech Recognition thinks you said:")
ass = r.recognize_google(audio)
print(ass)
h,t = ReadData()
#print(str(h)+str(t))
lines = "The temperature is " + str(t)+ " and humidty is " +str(h)
print(lines)
tts = gTTS(text=lines,lang='en')
tts.save('str.mp3')
os.system('omxplayer str.mp3')
