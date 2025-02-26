import pickle
import math
from googlesearch import search
from googlesearch import SearchResult
from colorama import Fore
import lib_spotify as spotify
#from tta_1D import vectCalcZ as vectCalcZ

#Dictionaries 
#Z Axis Dictionaries 
request_dictionary = {}
conversational_dictionary = {}
request_final = {}
conversational_final = {}

#X & Y Axis Dictionaries #Will base training off 30 examples
n_xytrain_sentences = 40
reminder_dictionary = {}
room_dictionary = {}
music_dictionary = {}
alarm_dictionary = {} #Only for alarm setting
timer_dictionary = {} #
calendar_dictionary = {}
log_dictionary = {}
command_dictionary = {} #CT-02 Specific Commands
listofcats = ["reminder", "room", "music", "alarm", "timer", "calendar", "log", "command"]
listofdicts = [reminder_dictionary, room_dictionary, music_dictionary, alarm_dictionary, timer_dictionary, calendar_dictionary, log_dictionary, command_dictionary]

'''
Wake me up at 4.22 p.m.
Wake me up at 6.15 a.m.
'''

common_words = {}
deletion_repetition = 1 #Delete trained word if only repeated once
repeat_allowance = 3 #words are only allowed to be found in a maximum of 3 dictionaries

#Paths
T_NEUTRAL = r"C:\Users\delay\OneDrive\Documents\Code & Programs\Visual Studio Code\Python\The CT Project\Modules\Text to Action\train_neutral.txt"
T_REQUEST = r"C:\Users\delay\OneDrive\Documents\Code & Programs\Visual Studio Code\Python\The CT Project\Modules\Text to Action\train_requests.txt"
T_TEST_NEUTRAL = r"C:\Users\delay\OneDrive\Documents\Code & Programs\Visual Studio Code\Python\The CT Project\Modules\Text to Action\test_neutral.txt"
T_TEST_REQUEST = r"C:\Users\delay\OneDrive\Documents\Code & Programs\Visual Studio Code\Python\The CT Project\Modules\Text to Action\test_requests.txt"
T_XY_TRAINING = r"C:\Users\delay\OneDrive\Documents\Code & Programs\Visual Studio Code\Python\The CT Project\Modules\Text to Action\XY_training.txt"

def train(loops = 1, cutoff_score = 6): #Number of training loops
    loopnumber = 1
    dictionary_number = -1 #Everytime a header is seen, dictionary_number +1
    n_dictionaries = len(listofdicts)
    
    while loopnumber <= loops:
        loopnumber += 1
        
        #Commence Training for requests
        training_file = open(T_XY_TRAINING, "r", encoding="UTF-8")
        
        #Reading the training file
        for sentence in training_file:
            sentence = sentence.lower()
            
            if sentence.find("///") != -1: #if this is a header line
                sentence = sentence.replace("///", "")
                print(Fore.YELLOW + f"[TTA] Dictionary Training: {sentence}" + Fore.RESET)
                dictionary_number += 1
                
            else:
                if dictionary_number != -1 and dictionary_number < n_dictionaries: #do not allow training to start if start header was not read or if dictionary number exceeds range
                    sentence = sentence.split()
                    
                    for word in sentence:
                        #remove ' from training data and replace with is
                        if word.find("’s") >= 0:
                            if listofdicts[dictionary_number].get("is") != None:
                                listofdicts[dictionary_number]["is"] = listofdicts[dictionary_number]["is"] + 1
                                
                            else:
                                listofdicts[dictionary_number]["is"] = 0
                        
                            word = word.replace("’s", "")

                        if word != "a.m." and word != "p.m.":
                            #remove any punctuation from training data and replace with ""
                            for letter in word:
                                if not (ord(letter) >= 97 and ord(letter) <= 122): 
                                    word = word.replace(letter, "")
                        
                        #writing to dictionary
                        if listofdicts[dictionary_number].get(word) != None: #if it is found in the dictionary!
                            listofdicts[dictionary_number][word] = listofdicts[dictionary_number][word] + 1
                            
                        else: #if it is not, create a new value for it
                            listofdicts[dictionary_number][word] = 0                        
                    
        training_file.close()
        
        for dictionary in listofdicts: #Repeat for all dictionaries
            temp_dict = dict(dictionary)
            print(Fore.LIGHTRED_EX + f"[TTA] Filtering Data..." + Fore.RESET)
            for item in temp_dict:
                if temp_dict.get(item) <= deletion_repetition:
                    dictionary.pop(item)
                    
        for dictionary in listofdicts: #Repeat for all dictionaries
            print(Fore.YELLOW + "[TTA] Scaling Data..." + Fore.RESET)
            for item in dictionary:
                dictionary[item] = dictionary[item]/n_xytrain_sentences

        #Save Dictionary Data
        n = 0
        for dictionary in listofdicts: #Repeat for all dictionaries
            print(Fore.LIGHTGREEN_EX + f"[TTA] Saving Dictionary {n} Data" + Fore.RESET)
            print(dictionary)
            print("\n")
            path = r"C:\Users\delay\OneDrive\Documents\Code & Programs\Visual Studio Code\Python\The CT Project\Modules\Text to Action\Data" + f"\{n}_data.pkl"
            
            with open(path, "wb") as file:
                pickle.dump(dictionary, file)
            file.close()    
        
            n += 1

def isInRange(min, max, value):
    if value > min and value < max:
        return True

def addVectorList(vectors):
    x_forces = []
    y_forces = []
    for vector in vectors: #find the x & y component of each vector
        magnitude, direction = vector
        
        if direction == 360: #just in case
            direction = 0
        if isInRange(0, 90, direction): #quadrant 1 (+x, +y)
            a = 90 - direction
            a = (a/180)*math.pi #convert to radians
            Fx = math.cos(a) * magnitude
            Fy = math.sin(a) * magnitude
        elif isInRange(90, 180, direction): #quadrant 2 (+x, -y)
            a = direction - 90
            a = (a/180)*math.pi #convert to radians
            Fx = math.cos(a) * magnitude
            Fy = -(math.sin(a) * magnitude)
        elif isInRange(180, 270, direction): #quadrant 3 (-x, -y)
            a = 270 - direction
            a = (a/180)*math.pi #convert to radians
            Fx = -(math.cos(a) * magnitude)
            Fy = -(math.sin(a) * magnitude)
        elif isInRange(270, 360, direction): #quadrant 4 (-x, +y)
            a = direction - 270
            a = (a/180)*math.pi #convert to radians
            Fx = -(math.cos(a) * magnitude)
            Fy = math.sin(a) * magnitude
            
        elif direction == 0:
            Fx = 0
            Fy = magnitude
        elif direction == 90:
            Fx = magnitude
            Fy = 0
        elif direction == 180:
            Fx = 0
            Fy = -magnitude
        elif direction == 270: 
            Fx = -magnitude
            Fy = 0
        else:
            print(Fore.RED + "Direction Error" + Fore.RESET)
            
        x_forces.append(Fx)
        y_forces.append(Fy)
        
        #direction cannot be 360 as already adjusted in front
        
    #Sum of X & Y forces
    x_rf = 0
    y_rf = 0
    for force in x_forces:
        x_rf += force
        
    for force in y_forces:
        y_rf += force
        
    r_magnitude = math.sqrt((x_rf*x_rf)+(y_rf*y_rf)) #pythagoeras theorem
    
    if r_magnitude != 0:
        #finding the heading/direction via quadrant
        if x_rf > 0: #if resultant x force is positive
            if y_rf > 0: #quadrant 1
                r_direction = 90 - (math.atan(abs(y_rf)/abs(x_rf))/math.pi)*180   
            
            elif y_rf < 0: #quadrant 2
                r_direction = 90 + (math.atan(abs(y_rf)/abs(x_rf))/math.pi)*180
                
            else: #equals to zero
                r_direction = 90
        
        elif x_rf < 0:
            if y_rf > 0: #quadrant 4
                r_direction = (math.atan(abs(y_rf)/abs(x_rf))/math.pi)*180 + 270
            
            elif y_rf < 0: #quadrant 2
                r_direction = 270 - (math.atan(abs(y_rf)/abs(x_rf))/math.pi)*180
                
            else: #equals to zero
                r_direction = 270
            
        else: #x = 0
            if y_rf > 0: 
                r_direction = 0
                
            elif y_rf < 0:
                r_direction = 180
                
        return [r_magnitude, r_direction]
    
    else:
        return [0, 0]
        
def vectCalcXY(sentence):   
    theta = 360/len(listofcats) #Basic angle (Based on how many categories)
    dict_direction = {}
    
    a = 0
    for category in listofcats:
        dict_direction[a] = category
        a += theta

    sentence = sentence.lower()
    sentence = sentence.split()
    n_words = len(sentence)
    
    sentence_vectors = []
    dictionaries_data = []
    keywords = {}
    
    x = 0
    for dictionary in listofdicts:
        path = r"C:\Users\delay\OneDrive\Documents\Code & Programs\Visual Studio Code\Python\The CT Project\Modules\Text to Action\Data" + f"\{x}_data.pkl"
        with open(path, "rb") as dict_data:
            dictionaries_data.append(dict(pickle.load(dict_data)))
        x+=1
        
    for word in sentence: #word by word
        #remove punctuation
        if word.find("’s") >= 0:        
            word = word.replace("’s", "")

        if word != "a.m." and word != "p.m.":
            #remove any punctuation from training data and replace with ""
            for letter in word:
                if not (ord(letter) >= 97 and ord(letter) <= 122): 
                    word = word.replace(letter, "")
        
        #print(Fore.LIGHTCYAN_EX + f"[TTA] Calculating Vector for '{word}'" + Fore.RESET)
        angle = 0
        vectors = [] #should be storing all the vectors for each word
        
        for dictionary in dictionaries_data: #go through dictionary by dictionary
            if dictionary.get(word) != None: #if word is found
                magnitude = dictionary.get(word)
                direction = angle
                
            else: #if word is not found
                magnitude = 0
                direction = angle
            
            if magnitude != 0:
                dictionary_index = dictionaries_data.index(dictionary)
                dictionary_name = listofcats[dictionary_index]
                #print(Fore.YELLOW + f"| {dictionary_name.capitalize()} | Word: '{word}' | M: {magnitude} | D: {direction} |" + Fore.RESET)
            
            vectors.append([magnitude, direction]) #[[Magnitude, Direction], [M1, D1]]
            angle = angle + theta #each dictionary has a different direction
        
        #Vector Calculation
        resultant_vector = addVectorList(vectors)
        if (round(resultant_vector[1]/theta) * 45) == 360:
            category = dict_direction.get(0)
        else:
            category = dict_direction.get(round(resultant_vector[1]/theta) * 45)

        #print(Fore.GREEN + f"[TTA] Word: {word} | M:{resultant_vector[0]} D:{resultant_vector[1]} | Cat: {category}" + Fore.RESET + "\n")

        #Remove word if found in many dictionaries
        times_repeated = 0
        for vector in vectors:
            if vector[0] != 0:
                times_repeated += 1
        
        if times_repeated <= repeat_allowance:
            sentence_vectors.append(resultant_vector)
            keywords[word] = resultant_vector
        else: 
            #print(Fore.RED + f"[TTA] Disregarding '{word}' (Too Common!)" + Fore.RESET)
            pass
        
    #Filtration
    #print(Fore.LIGHTGREEN_EX + f"[TTA] Begin Filtration")
    temp_vectors = list(sentence_vectors)
    for vector in sentence_vectors:
        if vector[0] == 0:
            temp_vectors.pop(temp_vectors.index(vector))
            
    sentence_vectors = list(temp_vectors)

    #Vector Calculation for Sentence 
    #print(Fore.LIGHTCYAN_EX + f"[TTA] Calculating Vector for '{sentence}'" + Fore.RESET)
    resultant_vector = addVectorList(sentence_vectors)
    resultant_vector = [resultant_vector[0]/n_words, resultant_vector[1]]
    
    #print(Fore.GREEN + f"[TTA] Resultant Vector: {resultant_vector}" + Fore.RESET)
    #print(dict_direction)
    if (round(resultant_vector[1]/theta) * 45) == 360:
        category = dict_direction.get(0)
        
    else:
        category = dict_direction.get(round(resultant_vector[1]/theta) * 45)
    
    print(Fore.GREEN + f"[TTA] Resultant Vector: {resultant_vector} | Category: {category}" + Fore.RESET)
    return category, keywords

def vectCalcZ(sentence, returnbool = True):   
    req_bool = False #Default returns false
    sentence.lower()
    phrase = sentence.split()
    sum = 0
    word_count = 0
    
    with open(r"C:\Users\delay\OneDrive\Documents\Code & Programs\Visual Studio Code\Python\The CT Project\Modules\Text to Action\Data\request_data.pkl", "rb") as req_data:
        req_dict = dict(pickle.load(req_data))
        
    with open(r"C:\Users\delay\OneDrive\Documents\Code & Programs\Visual Studio Code\Python\The CT Project\Modules\Text to Action\Data\conversational_data.pkl", "rb") as conv_data:
        conv_dict = dict(pickle.load(conv_data))
    
    #Positive (Request Dict)
    for word in phrase:
        word_count += 1
        if req_dict.get(word) != None:
            sum += req_dict.get(word)
    
    #Negative (Conv Dict)
    for word in phrase:
        if conv_dict.get(word) != None:
            sum = sum - conv_dict.get(word)

    average = sum/word_count
    #print(f"Sentence: {sentence} | Sum: {sum} | Average: {average}")
    
    if average > 0: #if it is a request
        req_bool = True 
        print(Fore.GREEN + f"[TTA] Request: {sentence} | Score: {average}" + Fore.RESET)
    
    elif average <= 0:
        req_bool = False
        print(Fore.WHITE + f"Neutral: {sentence} | Score: {average}" + Fore.RESET)
    
    if returnbool == True:
        return req_bool #if req, return true, else False
    
    else: 
        return average

def identifyKeywords(keywords): #keywords should be a dictionary with definitions of words with their vector magnitudes & direction
    neutral_terms = []
    identifiers = []

    n_iteration = 0
    index_of_last_neutral = 0
    for keyword in keywords:
        n_iteration += 1
        if keywords[keyword][0] == 0: #if it does not have a magnitude
            if n_iteration-index_of_last_neutral == 1 and index_of_last_neutral!=0: #if the previous word is also neutral (no magnitude)
                combined = neutral_terms[-1] + " " + keyword #last word
                neutral_terms.pop()
                neutral_terms.append(combined)
                index_of_last_neutral = n_iteration
            
            else:
                neutral_terms.append(keyword)
                index_of_last_neutral = n_iteration
                
        else: #if it is a keyword!
            identifiers.append(keyword)
            
    return identifiers, neutral_terms
            
def process(sentence):
    sentence = sentence.lower()
    #if vectCalcZ(sentence): #if it is a request
    if True: #request needs much more training :/
        category, keywords = vectCalcXY(sentence)
        identifiers, neutral_terms = identifyKeywords(keywords)
        print(Fore.GREEN + f"[TTA] {identifiers} | {neutral_terms}" + Fore.RESET)
        
        return category, sentence, identifiers, neutral_terms
    
    else: #if it is not a request
        return None, sentence, [], [] #returns as string
    
