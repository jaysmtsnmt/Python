import pickle
from colorama import Fore

request_dictionary = {}
conversational_dictionary = {}
common_words = {}
deletion_repetition = 1

request_final = {}
conversational_final = {}

T_NEUTRAL = r"C:\Users\delay\OneDrive\Documents\Code & Programs\Visual Studio Code\Python\The CT Project\Modules\Text to Action\train_neutral.txt"
T_REQUEST = r"C:\Users\delay\OneDrive\Documents\Code & Programs\Visual Studio Code\Python\The CT Project\Modules\Text to Action\train_requests.txt"
T_TEST_NEUTRAL = r"C:\Users\delay\OneDrive\Documents\Code & Programs\Visual Studio Code\Python\The CT Project\Modules\Text to Action\test_neutral.txt"
T_TEST_REQUEST = r"C:\Users\delay\OneDrive\Documents\Code & Programs\Visual Studio Code\Python\The CT Project\Modules\Text to Action\test_requests.txt"

def training():
    request_file = open(T_REQUEST, "r", encoding="UTF-8")
    for sentence in request_file:
        #print(sentence)
        
        sentence = sentence.lower()
        sentence = sentence.split()
        
        for word in sentence:
            #remove ' from training data and replace with is
            if word.find("’s") >= 0:
                if request_dictionary.get("is") != None:
                    request_dictionary["is"] = request_dictionary["is"] + 1
                    
                else:
                    request_dictionary["is"] = 0
            
                word = word.replace("’s", "")
                
            #remove any punctuation from training data and replace with ""
            for letter in word:
                if not (ord(letter) >= 97 and ord(letter) <= 122): 
                    word = word.replace(letter, "")
            
            if request_dictionary.get(word) != None:
                request_dictionary[word] = request_dictionary[word] + 1
                
            else:
                request_dictionary[word] = 0
                
    #print(request_dictionary)    
    request_file.close()
    #print(request_dictionary)
    #print("\n")

    #Commence conversational dictionary
    conversational_file = open(T_NEUTRAL, "r", encoding="UTF-8")
    for sentence in conversational_file:
        #print(sentence)
        
        sentence = sentence.lower()
        sentence = sentence.split()
        
        for word in sentence:
            #remove ' from training data and replace with is
            if word.find("’s") >= 0:
                if conversational_dictionary.get("is") != None:
                    conversational_dictionary["is"] = conversational_dictionary["is"] + 1
                    
                else:
                    conversational_dictionary["is"] = 0
            
                word = word.replace("’s", "")
                
            #remove any punctuation from training data and replace with ""
            for letter in word:
                if not (ord(letter) >= 97 and ord(letter) <= 122): 
                    word = word.replace(letter, "")
            
            if conversational_dictionary.get(word) != None:
                conversational_dictionary[word] = conversational_dictionary[word] + 1
                
            else:
                conversational_dictionary[word] = 0
                
    conversational_file.close()
    #print(conversational_dictionary)
    #print("\n")
    
    request_final = dict(request_dictionary)
    conversational_final = dict(conversational_dictionary)
    #Commence Filtration
    for item in request_dictionary:
        if request_dictionary.get(item) <= deletion_repetition:
            request_final.pop(item)
        
    for item in conversational_dictionary:
        if conversational_dictionary.get(item) <= deletion_repetition:
            conversational_final.pop(item)
            
    print(request_final)
    print(conversational_final)
    
    #Save Dictionary Data
    
    request_data = open(r"C:\Users\delay\OneDrive\Documents\Code & Programs\Visual Studio Code\Python\The CT Project\Modules\Text to Action\Data\request_data.pkl", "wb")
    pickle.dump(request_final, request_data)
    request_data.close()
    
    conversational_data = open(r"C:\Users\delay\OneDrive\Documents\Code & Programs\Visual Studio Code\Python\The CT Project\Modules\Text to Action\Data\conversational_data.pkl", "wb")
    pickle.dump(conversational_final, conversational_data)
    conversational_data.close()

def self_train(loops = 1, cutoff_score = 6): #Number of training loops
    loopnumber = 1
    number_req_sentences = 0
    number_conv_sentences = 0
    
    while loopnumber <= loops:
        loopnumber += 1
        
        #Commence Training for requests
        request_file = open(T_REQUEST, "r", encoding="UTF-8")
        for sentence in request_file:
            number_req_sentences += 1 #IMPT for division later
            sentence = sentence.lower()
            sentence = sentence.split()
            
            for word in sentence:
                #remove ' from training data and replace with is
                if word.find("’s") >= 0:
                    if request_dictionary.get("is") != None:
                        request_dictionary["is"] = request_dictionary["is"] + 1
                        
                    else:
                        request_dictionary["is"] = 0
                
                    word = word.replace("’s", "")

                #remove any punctuation from training data and replace with ""
                for letter in word:
                    if not (ord(letter) >= 97 and ord(letter) <= 122): 
                        word = word.replace(letter, "")
                
                if request_dictionary.get(word) != None:
                    request_dictionary[word] = request_dictionary[word] + 1
                    
                else:
                    request_dictionary[word] = 0
                    
        request_file.close()
        
        #Commence training for conversational dictionary
        conversational_file = open(T_NEUTRAL, "r", encoding="UTF-8")
        for sentence in conversational_file:
            number_conv_sentences += 1
            sentence = sentence.lower()
            sentence = sentence.split()
            
            for word in sentence:
                #remove ' from training data and replace with is
                if word.find("’s") >= 0:
                    if conversational_dictionary.get("is") != None:
                        conversational_dictionary["is"] = conversational_dictionary["is"] + 1
                        
                    else:
                        conversational_dictionary["is"] = 0
                
                    word = word.replace("’s", "")
                    
                #remove any punctuation from training data and replace with ""
                for letter in word:
                    if not (ord(letter) >= 97 and ord(letter) <= 122): 
                        word = word.replace(letter, "")
                
                if conversational_dictionary.get(word) != None:
                    conversational_dictionary[word] = conversational_dictionary[word] + 1
                    
                else:
                    conversational_dictionary[word] = 0
                    
        conversational_file.close()
        
        request_final = dict(request_dictionary)
        conversational_final = dict(conversational_dictionary)
        #Commence Filtration
        for item in request_dictionary:
            if request_dictionary.get(item) <= deletion_repetition:
                request_final.pop(item)
            
        for item in conversational_dictionary:
            if conversational_dictionary.get(item) <= deletion_repetition:
                conversational_final.pop(item)
                
        #Scaling of Data
        for item in request_final:
            request_final[item] = request_final[item]/number_req_sentences
            
        for item in conversational_final:
            conversational_final[item] = conversational_final[item]/number_conv_sentences
        
        #print(request_final)
        #print(conversational_final)
        
        #Save Dictionary Data
        
        request_data = open(r"C:\Users\delay\OneDrive\Documents\Code & Programs\Visual Studio Code\Python\The CT Project\Modules\Text to Action\Data\request_data.pkl", "wb")
        pickle.dump(request_final, request_data)
        request_data.close()
        
        conversational_data = open(r"C:\Users\delay\OneDrive\Documents\Code & Programs\Visual Studio Code\Python\The CT Project\Modules\Text to Action\Data\conversational_data.pkl", "wb")
        pickle.dump(conversational_final, conversational_data)
        conversational_data.close()

        #Test Conversational Sentences
        wrongly_identified = {}
        with open(T_TEST_NEUTRAL, "r+", encoding="UTF-8") as test_data:
            n_sentences = 0
            n_wrongsentences = 0
            n_correctsentences = 0
            total_wrong_score = 0
            total_correct_score = 0
            
            for sentence in test_data:
                n_sentences += 1
                sentence = sentence.replace("\n", "")
                score = process(sentence, False)
                #total_correct_score = score + total_correct_score
                
                if score >= 0: #Testing for conversational sentences
                    n_wrongsentences += 1
                    #print("Wrongly Identified!\n") No need for this due to color coding
                    wrongly_identified[sentence] = score
                    total_wrong_score += score
                    
                else: #Find the average score for correct sentences
                    n_correctsentences += 1
                    total_correct_score += score
            
        test_data.close()
        
        print("\n")
        #print(f"Wrongly Identified Sentences: \n{wrongly_identified}\n")
        average_correct_score = total_correct_score/n_correctsentences
        average_wrong_score = total_wrong_score/n_wrongsentences
        print(Fore.LIGHTCYAN_EX + f"AvCorrScore: {average_correct_score} | AvWrongScore: {average_wrong_score} | Midpoint: {(average_correct_score + average_wrong_score)/2}")
        print(Fore.LIGHTGREEN_EX + f"Percentage Accuracy = {(n_sentences-n_wrongsentences)/n_sentences*100}%" + Fore.RESET)
        
        #Rewriting to file
        print(Fore.LIGHTYELLOW_EX + f"\nBegin Retraining" + Fore.RESET)
        with open(T_NEUTRAL, "a", encoding="UTF-8") as neutral_file:
            for sentence in wrongly_identified:
                if wrongly_identified[sentence] <= average_wrong_score:
                    neutral_file.write("\n" + sentence)
                    print(f"Sentence: {sentence} | Score: {wrongly_identified[sentence]}")
                    
        print(Fore.LIGHTYELLOW_EX + "Finished Retraining\n" + Fore.RESET)   
        
        #Test Request Sentences
        wrongly_identified = {}
        with open(T_TEST_REQUEST, "r+", encoding="UTF-8") as test_data:
            n_sentences = 0
            n_wrongsentences = 0
            n_correctsentences = 0
            total_wrong_score = 0
            total_correct_score = 0
            
            for sentence in test_data:
                n_sentences += 1
                sentence = sentence.replace("\n", "")
                score = process(sentence, False)
                #total_correct_score = score + total_correct_score
                
                if score <= 0: #Testing for request sentences
                    n_wrongsentences += 1
                    #print("Wrongly Identified!\n") No need for this due to color coding
                    wrongly_identified[sentence] = score
                    total_wrong_score += score
                    
                else: #Find the average score for correct sentences
                    n_correctsentences += 1
                    total_correct_score += score
            
        test_data.close()
        
        print("\n")
        #print(f"Wrongly Identified Sentences: \n{wrongly_identified}\n")
        average_correct_score = total_correct_score/n_correctsentences
        average_wrong_score = total_wrong_score/n_wrongsentences
        print(Fore.LIGHTCYAN_EX + f"AvCorrScore: {average_correct_score} | AvWrongScore: {average_wrong_score} | Midpoint: {(average_correct_score + average_wrong_score)/2}")
        print(Fore.LIGHTGREEN_EX + f"Percentage Accuracy = {(n_sentences-n_wrongsentences)/n_sentences*100}%" + Fore.RESET)
        
        #Rewriting to file
        print(Fore.LIGHTYELLOW_EX + f"\nBegin Retraining" + Fore.RESET)
        with open(T_REQUEST, "a", encoding="UTF-8") as request_file:
            for sentence in wrongly_identified:
                if wrongly_identified[sentence] <= average_wrong_score:
                    request_file.write("\n" + sentence)
                    print(f"Sentence: {sentence} | Score: {wrongly_identified[sentence]}")     
                    
        print(Fore.LIGHTYELLOW_EX + "Finished Retraining\n" + Fore.RESET)       
        
def view_overlap(): #see which words overlap
    with open(r"C:\Users\delay\OneDrive\Documents\Code & Programs\Visual Studio Code\Python\The CT Project\Modules\Text to Action\Data\request_data.pkl", "rb") as req_data:
        req_dict = dict(pickle.load(req_data))
        
    with open(r"C:\Users\delay\OneDrive\Documents\Code & Programs\Visual Studio Code\Python\The CT Project\Modules\Text to Action\Data\conversational_data.pkl", "rb") as conv_data:
        conv_dict = dict(pickle.load(conv_data))
        
    for item in req_dict:
        if conv_dict.get(item) != None:
            print(f"Overlap found: {item} | Conv: {conv_dict.get(item)} | Req: {req_dict.get(item)}")

def processSum(sentence):
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
            
    for word in phrase:
        if conv_dict.get(word) != None:
            sum = sum - conv_dict.get(word)


    print(f"Sentence: {sentence} | Sum: {sum} | Average: {sum/word_count}")
    
    return sum
    
def process(sentence, returnbool = True):   #If request, returns True, else, returns False
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
        print(Fore.GREEN + f"Request: {sentence} | Score: {average}" + Fore.RESET)
    
    elif average <= 0:
        req_bool = False
        print(Fore.WHITE + f"Neutral: {sentence} | Score: {average}" + Fore.RESET)
    
    if returnbool == True:
        return req_bool #if req, return true, else False
    
    else: 
        return average 

def testForConv():
    wrongly_identified = {}
    with open(r"C:\Users\delay\OneDrive\Documents\Code & Programs\Visual Studio Code\Python\The CT Project\Modules\Text to Action\test_sentences1.txt", "r+") as test_data:
        n_sentences = 0
        n_wrongsentences = 0
        for sentence in test_data:
            n_sentences += 1
            sentence = sentence.replace("\n", "")
            sum = process(sentence)
            
            if sum >= 0:
                n_wrongsentences += 1
                print("Wrongly Identified!\n")
                wrongly_identified[sentence] = sum
                
    
    test_data.close()
    
    print("\n")
    print(f"Wrongly Identified Sentences: \n{wrongly_identified}\n")
    print(f"Percentage Accuracy = {(n_sentences-n_wrongsentences)/n_sentences*100}%")
    
def testForReq():
    #Test Request Sentences
    wrongly_identified = {}
    with open(T_TEST_REQUEST, "r+", encoding="UTF-8") as test_data:
        n_sentences = 0
        n_wrongsentences = 0
        n_correctsentences = 0
        total_wrong_score = 0
        total_correct_score = 0
        
        for sentence in test_data:
            n_sentences += 1
            sentence = sentence.replace("\n", "")
            score = process(sentence, False)
            #total_correct_score = score + total_correct_score
            
            if score <= 0: #Testing for request sentences
                n_wrongsentences += 1
                #print("Wrongly Identified!\n") No need for this due to color coding
                wrongly_identified[sentence] = score
                total_wrong_score += score
                
            else: #Find the average score for correct sentences
                n_correctsentences += 1
                total_correct_score += score
        
    test_data.close()
    
    print("\n")
    #print(f"Wrongly Identified Sentences: \n{wrongly_identified}\n")
    average_correct_score = total_correct_score/n_correctsentences
    average_wrong_score = total_wrong_score/n_wrongsentences
    print(Fore.LIGHTCYAN_EX + f"AvCorrScore: {average_correct_score} | AvWrongScore: {average_wrong_score} | Midpoint: {(average_correct_score + average_wrong_score)/2}")
    print(Fore.LIGHTGREEN_EX + f"Percentage Accuracy = {(n_sentences-n_wrongsentences)/n_sentences*100}%" + Fore.RESET)
    
# while True:
#     sentence = input("User: ")
#     process(sentence)
