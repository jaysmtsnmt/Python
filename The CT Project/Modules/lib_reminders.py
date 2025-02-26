import pickle 
import datetime
REMINDER_FILE = r"C:\Users\delay\OneDrive\Documents\Code & Programs\Visual Studio Code\Python\The CT Project\Modules\Reminder\r_data"

#Timing that reminder is set will be saved. 
# if timing is specified, eg. hours is inside (inside main.py)

class Reminder:
    # def __init__(self, payload, timing):
    #     self.payload = payload
    #     self.timing = timing
    def reset():
        empty = []
        with open(REMINDER_FILE, "wb") as file:
            pickle.dump(empty,file)
            
        file.close()


    def op(identifiers, neutral): #this acts as a filter for timings
        timing = None
        index = 0
        final_neutral = []
        
        for payload in neutral:
            if payload.find("tomorrow") != -1:
                date = datetime.datetime.now()
                timing = [date.strftime("%x"), date.strftime("%X"), 1] #12/31/18, 17:41:00	1 (add one because tomorrow)
                final_neutral.append(payload.replace("tomorrow", ""))    
                
            elif payload.find("later") != -1:
                date = datetime.datetime.now()
                timing = [date.strftime("%x"), date.strftime("%X"), 0.5] #12/31/18, 17:41:00	0.5 (add 6 hours because tomorrow)
                final_neutral.append(payload.replace("later", ""))    
                
            elif payload.find("today") != -1:
                date = datetime.datetime.now()
                timing = [date.strftime("%x"), date.strftime("%X"), 0] #12/31/18, 17:41:00	0 (remind by end of day)
                final_neutral.append(payload.replace("today", ""))              
            
            else:
                final_neutral.append(payload)
            
            index += 1
        
            for item in final_neutral:
                if item == '':
                    final_neutral.remove(item)
            
        return_list = [identifiers, final_neutral, timing]
        return return_list
            
    def add(payload, timing): #timing | date, time, 0/0.5/1 MUST PASS PAYLOAD AS A STRING
        try:
            with open(REMINDER_FILE, "rb") as file:
                reminders = pickle.load(file)
                #print(reminders)
                
                reminder = {
                    "payload" : payload,
                    "timing" : timing,
                    "status" : True
                }
                
                reminders.append(reminder)
                #print(f"ASDASD {reminders}")
                #pickle.dump(reminders, file)
                file.close()
                
            with open(REMINDER_FILE, "wb+") as file:
                pickle.dump(reminders, file)
                file.close()
                
        except EOFError:
            reminders = []
            print("first reminder")
            with open(REMINDER_FILE, "rb+") as file:
                #save reminders in a list, dictionaries in a list
                #status = True -> completed
                
                reminder = {
                    "payload" : payload,
                    "timing" : timing,
                    "status" : True
                }
                
                reminders.append(reminder)
                
                pickle.dump(reminders, file)

                file.close()
            
    def view(mode = "all"): #all, today, tomorrow
        if mode == "all":
            with open(REMINDER_FILE, "rb") as file:
                reminders = pickle.load(file)
                
                i = 1
                for reminder in reminders:
                    payload = reminder.get("payload")
                    timing = reminder.get("timing")
                    date = timing[0]
                    time = timing[1]
                    status = reminder.get("status")
                    
                    print(f"[REMIND] {i}. | {payload} | Scheduled on: {time}, {date} | Status: {status}")
                    
                    i += 1
                    
                file.close()
                
        elif mode == "today":
            with open(REMINDER_FILE, "rb") as file:
                reminders = pickle.load(file)
                
                reminders = []
                
        return reminders
                
# r = Reminder
    
# r.reset()
# after = r.op([["Identifiers"], ["tomorrow", "brush teeth"]])
# print(after)
# r.add(after[1][0], after[2])
# r.view("all")