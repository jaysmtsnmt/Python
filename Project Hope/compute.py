import openpyxl as xl
import datetime as dt
import os

ticket_sales = {
    "General Sales" : [0, 0],
    "Performer Discount" : [0, 0],
    "Early Bird Promotion" : [0, 0],
    "2 x Ticket Promotion" : [0, 0],
    "5 x Ticket Promotion" : [0, 0],
    "10 x Ticket Promotion" : [0, 0]
}

column_info = {
    "Buyer ID": 1,
    "Ticket Type" : 4,
    "QTY" : 5,
    "Amount" : 6
}

goal = 1000
worksheet_path = r"C:\Users\delay\Downloads\Concert Clarus 2.0.xlsx"
wb = xl.load_workbook(worksheet_path)
ticketing_sheet = wb['TICKETS']
customer_sheet = wb['CUSTOMER INFO']

path = r"C:\Users\delay\OneDrive\Documents\Code & Programs\Visual Studio Code\Python\Project Hope\previousdata.txt"


def main():
    p = 0
    #check for early birds first
    rn = 2 #start row 2
    QTY_value = int(customer_sheet.cell(rn, column_info['QTY']).value) #start row 2 
    TYPE_value = customer_sheet.cell(rn, column_info['Ticket Type']).value
    AMOUNT_value = int(customer_sheet.cell(rn, column_info["Amount"]).value)

    while TYPE_value != None:
        #print(str(rn) + " " + TYPE_value + " " + str(AMOUNT_value))
        if TYPE_value == "Early Bird Promotion":
            ticket_sales["Early Bird Promotion"][0] += QTY_value
            ticket_sales["Early Bird Promotion"][1] += AMOUNT_value
            
        elif TYPE_value == "General Sales" or TYPE_value == "Genral Sales":
            # if QTY_value > 1:
            #     print(f"{QTY_value}")
            # p += 1*QTY_value
            # print(p)
            if AMOUNT_value % 14 == 0: #Pure General Tix
                ticket_sales["General Sales"][0] += QTY_value
                ticket_sales["General Sales"][1] += AMOUNT_value
            
            elif AMOUNT_value % 11 == 0: #Pure discount tix
                ticket_sales["Performer Discount"][0] += QTY_value
                ticket_sales["Performer Discount"][1] += AMOUNT_value
                
            else: #must be 1 discount code but multiple general tix
                ticket_sales["Performer Discount"][0] += 1
                ticket_sales["Performer Discount"][1] += 11
                
                QTY_value -= 1
                AMOUNT_value -= 11
                
                if AMOUNT_value % 14 != 0:
                    print("ERROR")
                    quit()
                    
                else:  
                    ticket_sales["General Sales"][0] += QTY_value
                    ticket_sales["General Sales"][1] += AMOUNT_value
                
        elif TYPE_value == "2 x Tickets" or TYPE_value == "2 Tickets x 2 QR" or TYPE_value == "2 Tickets x 1 QR": #remember that 2 x Ticket Promotion = 2 tickets in final calculation
            #ticket_sales["2 x Ticket Promotion"][0] += QTY_value #becos sheet was updated
            ticket_sales["2 x Ticket Promotion"][0] += 1
            ticket_sales["2 x Ticket Promotion"][1] += AMOUNT_value
            
        elif TYPE_value == "5 x Tickets" or TYPE_value == "5 Tickets x 5 QR" or TYPE_value == "5 Tickets x 1 QR":
            #ticket_sales["5 x Ticket Promotion"][0] += QTY_value
            ticket_sales["5 x Ticket Promotion"][0] += 1
            ticket_sales["5 x Ticket Promotion"][1] += AMOUNT_value
            
        elif TYPE_value == "Orientation Promotion(10 Tickets)":
            #ticket_sales["5 x Ticket Promotion"][0] += QTY_value
            ticket_sales["10 x Ticket Promotion"][0] += 1
            ticket_sales["10 x Ticket Promotion"][1] += AMOUNT_value
            
        else: 
            print("broken")
            print(f"TYPE: {TYPE_value}")
        
        #update the row info
        rn += 1
        QTY_value = customer_sheet.cell(rn, column_info['QTY']).value #start row 2 
        TYPE_value = customer_sheet.cell(rn, column_info['Ticket Type']).value
        AMOUNT_value = customer_sheet.cell(rn, column_info["Amount"]).value
        
    #print(ticket_sales)

    total_tickets = 0
    total_profits = 0
    #Total Tickets Sold
    for cat in ticket_sales:
        if cat == "2 x Ticket Promotion":
            total_tickets += int(ticket_sales[cat][0]) * 2
            total_profits += ticket_sales[cat][1]
            
        elif cat == "5 x Ticket Promotion":
            total_tickets += int(ticket_sales[cat][0]) * 5
            total_profits += ticket_sales[cat][1]
    
        elif cat == "10 x Ticket Promotion":
            total_tickets += int(ticket_sales[cat][0]) * 10
            total_profits += ticket_sales[cat][1]
            
            
        else:
            total_tickets += ticket_sales[cat][0]
            total_profits += ticket_sales[cat][1]

    #final formatting
    print(f"*AS OF [{dt.datetime.now().strftime('%c')}]*")
    for cat in ticket_sales:
        print(f"{cat} | {int(ticket_sales[cat][0])}x | Profit: ${int(ticket_sales[cat][1])}")
        if cat == "Performer Discount":
            print(f"General/Discount | {int(ticket_sales['General Sales'][0]) + int(ticket_sales['Performer Discount'][0])}x | Profit: ${int(ticket_sales['General Sales'][1]) + (ticket_sales['Performer Discount'][1])} ")
    
    print(f"\nSold: {int(total_tickets)}/{goal} | Profit: SGD${total_profits}0")

    file2 = open(path, "r+")
    file = open(path, "a+")
    data_to_write = f"{dt.datetime.now().strftime('%c')}/{int(total_tickets)}/{goal}"
    lines2 = file2.readlines()\

    if data_to_write.split()[0] != lines2[-1].split()[0]:
        file.write("\n"+data_to_write)
        
    file.close()
    file2.close()

    data = open(path, "r")
    i=0
    previous = []
    lines = data.readlines() 

    print("\n*Sales History*")
    for line in lines: #date + / + tickets
        if line != "\n":
            line_list = line.split("/")
            
            if i > 0:
                tickets_sold = int(line_list[1]) - int(previous[1])
                print(f"{line_list[0]} | {line_list[1]}/{goal} | +{tickets_sold}")
                
            else:   
                print(f"{line_list[0]} | {line_list[1]}/{goal} |")
                
            previous = line_list
            i += 1
            line = data.readline(i)
            
    data.close()            

main()

while True:
    command = input("\nAwaiting Command (q/quit) (d/del) >")
    
    if command == "q":
        wb.close()
        quit()
        
    elif command == "d":
        temp_file = open(path, "r+", errors="ignore")
        lines = temp_file.readlines()
        lines = lines[:-1]
        temp_file.close()

        os.remove(path) #im so tired of this fuk ing thing so im jsut going to delete it
        
        file3 = open(path, "a+", errors="ignore")
        lines[-1] = lines[-1].strip("\n")
        file3.writelines(lines)
        file3.close()    
    