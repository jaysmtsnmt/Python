import json
import datetime

TIMETABLE_A = r"C:\Users\delay\OneDrive\Documents\Code & Programs\Visual Studio Code\Python\The CT Project\Modules\Timetable\Timetables\Week A timetable.htm"
TIMETABLE_B = r"C:\Users\delay\OneDrive\Documents\Code & Programs\Visual Studio Code\Python\The CT Project\Modules\Timetable\Timetables\Week B Timetable.htm"


starting_time = "7:40"

lessons = { #does not include Econs Program #if there are lessons that program does not understand, flag #check for H1
    "PW" : "Project Work",
    "EC" : "Economics",
    "PE" : "PE",
    "MA" : "Math", 
    "GP" : "General Paper",
    "CH" : "Chemistry",
    "CP" : "Computing",
    "CT" : 'Civics',
    "CONNECT 2" : 'Civics'
    #"ASSEMBLY" : "Assembly"
}

def lesson_start(lesson_data, time="7:40"): #time can be passed as a list or as a string
    minutes = (int(lesson_data.get('fromslot')) - 1)*20
    repetitions = int(minutes/20)
    repetitions = repetitions * "-"
    
    if type(time) != list: 
        time = time.split(":") #splits the time into a list
    
    for repetition in repetitions:
        time[1] = int(time[1]) + 20 #add 20 to minutes
        if int(time[1]) == 60:
            time[1] = "00"
            time[0] = int(time[0]) + 1
            
    time[0] = int(time[0])
    time[1] = int(time[1])
    
    return time

def lesson_end(lesson_data, time="7:40"): #time can be passed as a list or as a string
    minutes = (int(lesson_data.get('toslot')) - 1)*20
    repetitions = int(minutes/20)
    repetitions = repetitions * "-"
    
    if type(time) != list: 
        time = time.split(":") #splits the time into a list
    
    for repetition in repetitions:
        time[1] = int(time[1]) + 20 #add 20 to minutes
        if int(time[1]) == 60:
            time[1] = "00"
            time[0] = int(time[0]) + 1
            
    time[0] = int(time[0])
    time[1] = int(time[1])
    
    return time


#start from slot 1 -> which is 7:40
#you will need to -1 from fromslot variable, then * the variable + starting 7:40

#print(add_time("7:40", 120)) 

#line 34 contains the week information

#print(type(p_raw))

# for categories in p_raw:
#     print(categories)
    
#p_raw.get("lessons_cc07d65f28866a930d803e10c79ecf67")[0] - monday
# Categories:
# options
# title
# students
# dates
# timeslots
# lessons_cc07d65f28866a930d803e10c79ecf67

# slot 1 - 7:40 - 8:00
# slot 2 - 8:00 - 8:20
    
#print(f"Lesson time: {get_time((int(lesson_info.get('fromslot')) -1)*20)} Lesson: {lesson_info.get('line1')}")

def a_timetable(day):     
    with open(TIMETABLE_A, "r") as jsfile:
        #print(jsfile.readlines())
        list = jsfile.readlines()
        #print(list[34])
        s_raw = str(list[34])
        s_raw = s_raw.split("var data = ")[1]
        s_raw = s_raw.split(";\n")[0]
        #print(s_raw)
        p_raw = json.loads(s_raw)

    weekly_schedule = p_raw.get("lessons_cc07d65f28866a930d803e10c79ecf67")[0].get("rows")
    monday = p_raw.get("lessons_cc07d65f28866a930d803e10c79ecf67")[0].get("rows")[0].get("lessons")

    weekly_schedule = p_raw.get("lessons_cc07d65f28866a930d803e10c79ecf67") #weekly schedule
    processed_lessons = []
    processed_weekly_lessons = {}

    n_day = 0
    for daily_schedule in weekly_schedule:
        n_day += 1
        daily_schedule = daily_schedule.get("rows")[0].get("lessons") #list of lessons
        
        for lesson in daily_schedule:
            start_time = lesson_start(lesson)
            end_time = lesson_end(lesson)
            
            if start_time[1] == 0:
                start_time[1] = "00"
                
            if end_time[1] == 0:
                end_time[1] = "00"
            
            name = lesson.get("line1")        
            location = lesson.get("line2")
            
            for lesson in lessons:      
                if name.find(f"{lesson}") >= 0 and name.find("PROG") == -1 and name.find("H1") == -1:
                    name = lessons.get(lesson)
                    
                    write = {
                        "name" : name,
                        "start" : start_time,
                        "end" : end_time,
                        "location" : location
                    }
                    
                    processed_lessons.append(write)

        if n_day == 1:
            processed_weekly_lessons["monday"] = processed_lessons
        elif n_day == 2:
            processed_weekly_lessons["tuesday"] = processed_lessons
        elif n_day == 3:
            processed_weekly_lessons["wednesday"] = processed_lessons
        elif n_day == 4:
            processed_weekly_lessons["thursday"] = processed_lessons
        elif n_day == 5:
            processed_weekly_lessons["friday"] = processed_lessons
        processed_lessons = []
        
    for lesson in processed_weekly_lessons.get(day):
        print(lesson)
        
    return processed_weekly_lessons.get(day)

def b_timetable(day):     
    with open(TIMETABLE_B, "r") as jsfile:
        #print(jsfile.readlines())
        list = jsfile.readlines()
        #print(list[34])
        s_raw = str(list[34])
        s_raw = s_raw.split("var data = ")[1]
        s_raw = s_raw.split(";\n")[0]
        #print(s_raw)
        p_raw = json.loads(s_raw)

    weekly_schedule = p_raw.get("lessons_cc07d65f28866a930d803e10c79ecf67")[0].get("rows")
    monday = p_raw.get("lessons_cc07d65f28866a930d803e10c79ecf67")[0].get("rows")[0].get("lessons")

    weekly_schedule = p_raw.get("lessons_cc07d65f28866a930d803e10c79ecf67") #weekly schedule
    processed_lessons = []
    processed_weekly_lessons = {}

    n_day = 0
    for daily_schedule in weekly_schedule:
        n_day += 1
        daily_schedule = daily_schedule.get("rows")[0].get("lessons") #list of lessons
        
        for lesson in daily_schedule:
            start_time = lesson_start(lesson)
            end_time = lesson_end(lesson)
            
            if start_time[1] == 0:
                start_time[1] = "00"
                
            if end_time[1] == 0:
                end_time[1] = "00"
            
            name = lesson.get("line1")        
            location = lesson.get("line2")
            
            for lesson in lessons:      
                if name.find(f"{lesson}") >= 0 and name.find("PROG") == -1 and name.find("H1") == -1:
                    name = lessons.get(lesson)
                    
                    write = {
                        "name" : name,
                        "start" : start_time,
                        "end" : end_time,
                        "location" : location
                    }
                    
                    processed_lessons.append(write)

        if n_day == 1:
            processed_weekly_lessons["monday"] = processed_lessons
        elif n_day == 2:
            processed_weekly_lessons["tuesday"] = processed_lessons
        elif n_day == 3:
            processed_weekly_lessons["wednesday"] = processed_lessons
        elif n_day == 4:
            processed_weekly_lessons["thursday"] = processed_lessons
        elif n_day == 5:
            processed_weekly_lessons["friday"] = processed_lessons
        processed_lessons = []
        
    for lesson in processed_weekly_lessons.get(day):
        #print(lesson)
        pass
        
    return processed_weekly_lessons.get(day)

# Library Usage

# calling the function a_timetable() or b_timetable() will return as a list.
# required variables that need to be passed into the definition:
#     1. day (monday - friday)
    
# Format of returned data:
#     1. List of lessons
#     2. Dictionary of information of lessons ("name", "location", "start", "end")
  
  
# week_number = datetime.datetime.now()
# week_number = week_number.strftime("%W")
# print((int(week_number) % 2))
              
#print(b_timetable("monday"))
