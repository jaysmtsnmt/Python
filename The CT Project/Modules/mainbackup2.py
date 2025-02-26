print("[PYTHON] CT-02 Starting... \n")

import cv2
import time
import dlib
import sys
import turtle
import serial #custom serial library is not needed (see class: serial)
import pygame
import pvporcupine
import threading as th
import lib_tta_3D as action
from colorama import Fore
import lib_spotify as spotify
from pvrecorder import PvRecorder
from lib_stt import recognizer as SST

arduino = serial.Serial(port='COM5', baudrate=9600, timeout=.1)

#Variables
state = "sleep"
speech = None
WAKEWORDPATH1 = r'C:\Users\delay\OneDrive\Documents\Code & Programs\Visual Studio Code\Python\The CT Project\Wakewords\Datafiles\Hey-Cee-Tee_en_windows_v3_0_0.ppn'
WAKEWORDPATH2 = r"C:\Users\delay\OneDrive\Documents\Code & Programs\Visual Studio Code\Python\The CT Project\Wakewords\Datafiles\yo-cee-tee_en_windows_v3_0_0.ppn"
MIC_ID = 1

#Face Tracking
WIDTH = 1280
HEIGHT = 720
VISION_Y = 480
truecentre = WIDTH/2
movement_pix_sens = 64
detector = dlib.get_frontal_face_detector()
serial_comm_limit = 0.2

#Reminder
REMINDERSPATH = r'C:\Users\delay\OneDrive\Documents\Code & Programs\Visual Studio Code\Python\The CT Project\Modules\Reminder\data.txt'

#Serial
class Serial:
    global state
    
    def serialUpdate():
        global state
        while True:
            recieved = str(arduino.readline().decode("utf-8"))
            #recieved = recieved.strip() #stripping data with \r\n characters (it doesnt work rn)
            dataToPython = recieved.split("=")
            if dataToPython[0] != recieved: #if data is indeed split and seperated (pos 0 will not be the same as recieved)
                #print(f'[PYDEBUG] {dataToPython}')
                if dataToPython[0] == "[STATE]":
                    state = dataToPython[1].strip() #when read, the end of the data is actually read as \r\n
                    print(f"[STATE] PYSTATE changed to: {state}")
                
            if recieved != "":
                print(recieved, end = "")
            #return recieved
        
    def write(x):
        arduino.write(bytes((x+'\n'), 'utf-8'))
        time.sleep(0.05)

    def getwriteInput():
        while True:
            writeinput = turtle.Screen()
            writeinput.setup(400, 500)
            print("[PYTHON] Getting Input")
            datawrite = turtle.textinput("Python -> C++ Input", "Dataline")
            print(datawrite)
            
            if datawrite != "":
                Serial.write(datawrite)   
                
            print("[PYTHON] Done")     
            
    def deepSleepInput():
        global state
        writeinput = turtle.Screen()
        writeinput.setup(100, 100)
        
        while True:
            datawrite = turtle.textinput("Python -> C++ Input", "Dataline")
            print(f"[PYTHON] Command Recieved: {datawrite}")
            
            if datawrite == "wake":
                state = "sleep"
                print(f"[PYTHON] Starting Up CT-02...")
                pygame.init()
                display = pygame.display.set_mode((300, 300))
                Serial.write("00/sleep")
                
                writeinput.clear()
                writeinput.reset()
                writeinput.bye()
                break
                
            elif datawrite != "":
                Serial.write(datawrite)

#Functions
def wakeword():
    keyword_dictionary = {"1": ["Hey CT", WAKEWORDPATH1], 
                   "2": ["Yo CT", WAKEWORDPATH2]}
    access_key = '5XYibmnYr83z6EscaHDRMx7ERgAnRBf1T71w007c+xADuXcb3PhsOg=='
    keyword_paths = []
    
    # for i, device in enumerate(PvRecorder.get_available_devices()):
    #     print('Device %d: %s' % (i, device))
    #     #Device 0: Microphone (Realtek(R) Audio)
        
    for keyword in keyword_dictionary: 
        keyword_paths.append(keyword_dictionary[keyword][1])
        #print(f'Keywords paths {keyword_paths}')
        
    #creating the porcupine object
    porcupine = pvporcupine.create(
        access_key=access_key,
        keyword_paths=keyword_paths,
        sensitivities=[0.5, 0.5])

    #recording audio
    recorder = PvRecorder(frame_length=porcupine.frame_length, device_index=MIC_ID)
    recorder.start()
    print('[AUDIO] Command Armed... ')

    try:
        while True:
            pcm = recorder.read()
            result = porcupine.process(pcm)
            
            if result >= 0:
                print(f'[PYTHON] Detected Keyword: {keyword_dictionary[str(result+1)][0]}')
                wakeEvent.set()
                
    except KeyboardInterrupt:
        print('[STATE] Forcing Deep Sleep...')
        
    finally:
        recorder.delete()
        porcupine.delete()
        print("[AUDIO] Audio Engine shutdown")

def sleep():
    global state
    #print(f"[PYDEBUG] EVENT {wakeEvent.is_set()}")
    if wakeEvent.is_set() == True:
        #print("[EVENT] wakeEvent Detected")
        Serial.write("00/awake")
        wakeEvent.clear()
        SST.stopRecording.clear()
        state = "awake"
        
def deepsleep():
    global state
    getInput_Thread = th.Thread(target=Serial.deepSleepInput) #special input prompt such that if wake is passed, robot goes into sleep
    getInput_Thread.daemon = True
    
    if getInput_Thread.is_alive() == False and state == "deepsleep": #so that it doesnt keep starting this thread over and over again until the program closes (leaves deep sleep)
        #print("[PYTHON] Deep Sleep threading started")
        getInput_Thread.run()

def listen():
    global speech
    print("[PYSST] Listening")
    SST.stopRecording.clear()
    speech_detected.clear()
    speech = SST.recognize()
    
    if speech != None:
        #print(f"[PYSST] {speech}")
        SST.stopRecording.clear()
        speech = speech.lower()
        speech_detected.set() 
        #to do: need to clear speech as a global variable and also clear Speech detected
    
    # else: #I genuinely don't know why i keep repeating it
    #     SST.stopRecording.clear()

def textToAction():
    global speech
    global state
    
    if speech != None and len(speech) > 1:
        category, sentence, identifiers, neutral_terms = action.process(speech)
        #if it is a request, category != None
        
        if category == "reminder":
            print(Fore.GREEN + f"[TTA] Reminder: {sentence}" + Fore.RESET)
            for identifier in identifiers:
                if identifier == "what" or identifier == "view":
                    with open(REMINDERSPATH, "r") as rfile:
                        reminders = rfile.readlines()
                        if reminders[0] != None:
                            n_reminders = 0
                            print(Fore.GREEN + "Reminders: " + Fore.RESET)
                            for reminder in reminders:
                                n_reminders += 1
                                print(f"{n_reminders}: {reminder}")
                    
                    rfile.close()
                
                elif identifier == "add" or identifier == "remind":
                    with open(REMINDERSPATH, "a") as rfile:
                        print(Fore.GREEN + f"New Reminder Added: {' '.join(neutral_terms)}" + Fore.RESET)
                        rfile.write((" ".join(neutral_terms) + "\n"))
                    
                    rfile.close()
                
                elif identifier == "delete" or identifier == "complete" or identifier == "mark" or identifier == "remove": #not working yet
                    reminders_dictionary = {}
                    with open(REMINDERSPATH, "w+") as rfile:
                        reminders = rfile.readlines()
                        if reminders[0] != None:
                            n_reminders = 0
                            print(Fore.GREEN + "Reminders: " + Fore.RESET)
                            for reminder in reminders:
                                n_reminders += 1
                                reminders_dictionary[n_reminders] = reminder
                    
                    rfile.close()
        
        elif category == "room":
            print(Fore.GREEN + f"[TTA] Room: {sentence}" + Fore.RESET)
        
        elif category == "music":
            print(Fore.GREEN + f"[TTA] Music: {sentence}" + Fore.RESET)
            for identifier in identifiers:
                if identifier == "turn" or identifier == "play" or identifier == "pause": #toggle
                    if identifier == "play" or (identifier == "turn" and sentence.find("on") > -1):
                        #check neutral_terms
                        if len(neutral_terms) > 0: #if there are some neutral words
                            x = 0
                            song_name = ""
                            
                            for term in neutral_terms:
                                if len(term.split()) > x:
                                    x = len(term.split())
                                    song_name = term
                            try: 
                                index = neutral_terms.index("by") + 1
                                spotify.play(song=song_name, song_artist=neutral_terms[index])
                                
                            except ValueError:
                                spotify.play(song=song_name)
                            
                        else:       
                            spotify.play()
                            break
                            
                    elif identifier == "pause" or (identifier == "turn" and sentence.find("off") > -1):
                        spotify.pause()
                        break             
                    
                elif identifier == "skip":
                    spotify.skip()
                    break       
                    
                elif identifier == "rewind":
                    spotify.rewind()
                    break       
                
                elif identifier == "add" or "queue":
                    if len(neutral_terms) > 0: #if there are some neutral words
                        x = 0
                        song_name = ""
                        
                        for term in neutral_terms:
                            if len(term.split()) > x:
                                x = len(term.split())
                                song_name = term
                        
                        try: 
                            index = neutral_terms.index("by") + 1
                            spotify.addtoQueue(song=song_name, song_artist=neutral_terms[index])
                            
                        except ValueError:
                            spotify.addtoQueue(song=song_name)
                
                else:
                    print(spotify.currentlyPlaying())
                    break
                        
        elif category == "alarm":            
            print(Fore.GREEN + f"[TTA] Alarm: {sentence}" + Fore.RESET)
        
        elif category == "timer":
            print(Fore.GREEN + f"[TTA] Timer: {sentence}" + Fore.RESET)

        elif category == "calendar":
            print(Fore.GREEN + f"[TTA] Calendar: {sentence}" + Fore.RESET)
        
        elif category == "log":
            print(Fore.GREEN + f"[TTA] Log: {sentence}" + Fore.RESET)

        elif category == "command":
            print(Fore.GREEN + f"[TTA] Command: {sentence}" + Fore.RESET)
            for identifier in identifiers:
                if identifier == "eject" or identifier == "phone":
                    Serial.write("05/eject")
                    break
                    
                elif identifier == "sleep":
                    state = "sleep"
                    Serial.write("03/sw/98/10")
                    Serial.write("00/sleep")
                    break
                    
                elif identifier == "hibernate" or identifier == "hibernation":
                    state = "deepsleep"
                    Serial.write("00/deepsleep")
                    break
        
        else: #so far, it is deactivated 
            print(Fore.RED + f"[TTA] Error! NoneType Category (Not a request)" + Fore.RESET)
            if sentence.find("sleep") != -1:
                state="sleep"
                Serial.write("03/sw/98/10")
                Serial.write("00/sleep")
                
            elif sentence.find("hibernate") != -1:
                state="deepsleep"
        
        speech = None #reset speech to None

#Threading
serialUpdate_thread = th.Thread(target=Serial.serialUpdate)
serialUpdate_thread.daemon = True #when error surfaces or program exits serial stops updating
serialUpdate_thread.start()

wakeword_thread = th.Thread(target=wakeword)
wakeword_thread.daemon = True
wakeword_thread.start()
wakeEvent = th.Event() #if wakeword is called... 

speech_detected = th.Event()

#Main
def main():
    global speech
    global state
    
    #Clearing of the wakeword event if state is not sleep (change if needed later)
    if wakeEvent.is_set() == True and state != "sleep":
        wakeEvent.clear()
    
    if state == "idle":
        SST.stopRecording.clear()
        #print("[SST] RECOGNIZE")
        speech = SST.recognize()
        
        if speech != None:
            print(f"[PYSST] {speech}")
            SST.stopRecording.clear()
            
            speech = speech.lower()
            
            #i just want to do this for fun
            if speech.find("play") >= 0:
                spotify.play()
            
            elif speech.find("pause") >= 0:
                spotify.pause()
        else:
            SST.stopRecording.clear()
    
    if state == "awake":
        count = 0
        prev_frame_time = 0
        new_frame_time = 0
        prev_face_x = 0
        face_x = 0
        face_y = 0
        
        vid = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        vid.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
        vid.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)
        
        #start recording (one thread)
        listening_thread = th.Thread(target=listen)
        listening_thread.daemon = True
        listening_thread.start()
        
        while state == "awake": #while loop for repeat
            #see if listening thread had detected speech
            if speech_detected.is_set() == True:
                speech_detected.clear()
                
                textToAction_thread = th.Thread(target=textToAction)
                textToAction_thread.daemon = True
                textToAction_thread.start()
                
            elif (listening_thread.is_alive() == False) and (speech_detected.is_set()) == False:
                listening_thread = th.Thread(target=listen)
                listening_thread.daemon = True
                listening_thread.start()
            
            ret, frame = vid.read()
            if not ret:
                break
            
            frame = frame[int((HEIGHT/2)-(VISION_Y/2)):int((HEIGHT/2)+(VISION_Y/2)), 0:WIDTH] #FULL WIDTH, HALF HEIGHT
            faces = detector(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            cv2.circle(frame, (int(WIDTH/2), int(VISION_Y/2)), 20, (0,0,0), 3)
            
            for face in faces:
                count += 1
                x1 = face.left()
                y1 = face.top()
                x2 = face.right()
                y2 = face.bottom()
                
                centrex = (x1 + x2)/2
                centrey = (y1 + y2)/2
                #boxarea = (x2 - x1) * (y2 - y1)
                
                cv2.circle(frame, (int(round(centrex)), int(round(centrey))), 10, (0,0,255), 3)
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 3)
                
                face_x = round(centrex)
                face_y = round(centrey)
        
            new_frame_time = time.time() 
            fps = 1/(new_frame_time-prev_frame_time)     
            if (new_frame_time-prev_frame_time) >= serial_comm_limit:
                prev_frame_time = new_frame_time 
                fps = int(fps) 
                
                if (face_x != 0) or (face_y != 0):
                    if (abs(face_x - prev_face_x) > movement_pix_sens):
                        Serial.write(f"09/{face_x}")
                        print(f"\n[PYTHON] Sent: 09/{face_x} | FPS: {fps}")

                        prev_face_x = face_x
                        
            #cv2.imshow('frame', frame)
            key = cv2.waitKey(1) & 0xFF

            if key == ord("q") or key == ord("Q"):
                break  
            
            face_x = 0
            face_y = 0
    
        print("Quitting...")
        vid.release() 
        cv2.destroyAllWindows() 
        time.sleep(0.5)
        
    elif state == "sleep":
        #print("SLEEP")
        sleep()
        
    elif state == "deepsleep":
        speech = None
        deepsleep()

pygame.init()
display = pygame.display.set_mode((300, 300))

print("\n[PYTHON] CT-02 Online")
while __name__ == "__main__":
    main()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            Serial.write("00/sleep")
            sys.exit()
         
        # checking if keydown event happened or not
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                print("[PYTHON] ESC Forcing Hibernation...")
                Serial.write("00/deepsleep")
                state = "deepsleep"
       