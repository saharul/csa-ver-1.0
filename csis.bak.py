import sys
from collections import namedtuple
from validate import validate
from selectcarinfo import SelectCarInfo
from selectgarageinfo import SelectGarageInfo
from datetime import datetime
from dateutil.relativedelta import relativedelta
from userinputfunct import inputNumber, inputFloat, inputDate
from serviceparts import DeletePart, DisplayParts, AddServicePart
import pandas as pd


#****************************************************************************************
#PROGRAM BY:    SAHARUL NIZAM SAAIDI                                                    *
#SECTION:       CAR SERVICE INFORMATION SYSTEM                                          *
#DATE:          15TH MARCH 2020                                                         *
#Program No.    YOUR FIRST PROGRAM IN 2020                                              *
#****************************************************************************************

CSV_FILE = "ServisMaster.csv"


def DisplayTitle():
    print('*' * 100)
    print("n************************** PROGRAM TO CREATE READ AND WRITE TO EXCEL *****************************nn")
    print('*' * 100)


def PrintBlankRow(numrow):
    i = 1
    while i <= numrow:
       print("\n")
       i += 1


def DisplayGrid(svcid,date,model,plate,svc_center,mileage,nxt_mileage,nxt_date,amount, showtitle=False):
    if showtitle == True:
        id_t,date_t,model_t,plate_t,svc_center_t,mileage_t,nxt_mileage_t,nxt_date_t,amount_t = GetRecord("SvcId").split(",")
        print('{0: <7}'.format(id_t) + '{0: <14}'.format(date_t) + '{0: <25}'.format(model_t) + '{0: <10}'.format(plate_t) + 
            '{0: <25}'.format(svc_center_t) + '{0: >12}  '.format(mileage_t) + '{0: >12}  '.format(nxt_mileage_t) +
            '{0: <14}'.format(nxt_date_t) + '{0: >10}  '.format(amount_t))
    print('{0: <7}'.format(svcid) + '{0: <14}'.format(date) + '{0: <25}'.format(model) + '{0: <10}'.format(plate) + 
        '{0: <25}'.format(str(svc_center).upper()) + '{0: >12}  '.format(mileage) + '{0: >12}  '.format(nxt_mileage) +
        '{0: <14}'.format(nxt_date) + '{0: >10}  '.format(amount))



# FUNCTION TO SAVE SERVICE TO FILE
def SaveService(service):
    f = open(CSV_FILE,"a+")
    f.write(service[0] + ',' + service[1] + ',' + service[2] + ',' + service[3] + ',' 
                + service[4].upper() + ',' + service[5] + ',' + service[6] + ',' + service[7] + ',' + service[8] + '\n')
    f.close()



#  FUNCTION TO RETRIEVE A SINGLE SERVICE RECORD FROM THE DATABASE
def GetRecord(input_id):
    with open(CSV_FILE,"r") as f:
         for line in f:
            line = line.rstrip()
            svcid = line.split(",", 1)
            if (svcid[0] == input_id):
                return line


#  FUNCTION TO ADD A SERVICE TO THE DATABASE
def AddService():
    Service = namedtuple("Service", "Id SvcDate Model Plate SvcCenter Mileage Nxt_Mileage Nxt_Date Amount")
    
    id = str(GetMaxId() + 1)

    date = inputDate("Enter Date of Service (DD/MM/YYYY) ", 
                            datetime.today().strftime('%d/%m/%Y'), "%d/%m/%Y")

    carinfo_selected = SelectCarInfo()
    model = carinfo_selected[0]   # Assign chosen model name
    plate = carinfo_selected[1]   # Assign chosen plate no
    
    grginfo_selected = SelectGarageInfo()
    svc_center = grginfo_selected[0]   # Assign chosen service center name
  
    mileage = inputNumber("Enter Mileage: ")
    nxt_mileage = inputNumber("Enter Next Service Mileage: ")

    defdate = (datetime.strptime(date, "%d/%m/%Y") + relativedelta(months=3)).strftime("%d/%m/%Y")
    nxt_date = inputDate("Enter Date of Next Service (DD/MM/YYYY", defdate, "%d/%m/%Y")

    amount = inputFloat("Enter Service Amount: ")
    newService = Service(id, date, model, plate, svc_center, mileage, nxt_mileage, nxt_date, amount)
    SaveService(newService)
    PrintBlankRow(1)
    print("Service was added successfully")
    PrintBlankRow(1)


#  FUNCTION DISPLAY DETAILS OF A PARTICULAR SERVICE
def DisplayService():
    input_id = input("\nEnter the ID of Service to display: ")
    try:
        svcid, date, model, plate, svc_center, mileage, nxt_mileage, nxt_date, amount = GetRecord(input_id).split(",")
        if (svcid == input_id):
            DisplayGrid(svcid, date, model, plate, svc_center, mileage, nxt_mileage, nxt_date, amount,True)
        return(input_id)
    except AttributeError:
        PrintBlankRow(1)
        print("There was no record with Id " + input_id)
 
    

# FUNCTION TO DELETE A SERVICE FROM THE DATABASE
def DeleteService():
    input_id = input("Enter the ID of the service to delete: ")
    f = open(CSV_FILE,"r+")
    d = f.readlines()
    f.seek(0)
    for line in d:
        record = line.rstrip()
        id = record.split(",", 1)
        if id[0] != input_id:
           f.write(line)
    f.truncate()
    f.close()
    PrintBlankRow(1)
    print("Service was successfully deleted from the database!")
    PrintBlankRow(1)


# FUNCTION TO VIEW ALL SERVICES IN THE DATABASE
def ViewService():
    with open(CSV_FILE,"r") as f:
        for line in f:
            line = line.rstrip()
            svcid, date, model, plate, svc_center, mileage, nxt_mileage, nxt_date, amount = line.split(",")
            if not line: continue
            DisplayGrid(svcid, date, model, plate, svc_center, mileage, nxt_mileage, nxt_date, amount)
    PrintBlankRow(1)


def ViewService_df():
    df = pd.read_csv(CSV_FILE, index_col=False)
    # blankIndex=[''] * len(df)  #hide index column
    # df.index=blankIndex
    df.index.name = "Key"
    print(df)  #show the parts
    PrintBlankRow(1)


#  FUNCTION TO SEARCH FOR A SERVICE IN THE DATABASE
def SearchService():
    criteria = input("Enter a search criteria: ")
    with open(CSV_FILE,"r") as f:
         shtitle = True
         for line in f:
             line = line.rstrip()
             if line.upper().find(criteria.upper()) != -1:
                 id, date, model, plate, svc_center, mileage, nxt_mileage, nxt_date, amount = line.split(",")
                 DisplayGrid(id, date, model, plate, svc_center, mileage, nxt_mileage, nxt_date, amount, shtitle)
                 shtitle = False # Turnimg off header
    PrintBlankRow(1)


# GET THE TOTAL NUMBER OF ALL SERVICES
def GetTotal():
        return sum(1 for line in open(CSV_FILE))


# FUNCTION TO GET THE MAXIMUM ID IN THE DB
def GetMaxId():
    with open(CSV_FILE,"r") as f:
        for line in f:
            line = line.rstrip()
            Id = line.split(",", 1)
            if not line: continue
        return(int(Id[0]))


#FUNCTION TO DISPLAY THE MENU
def DisplayMenu():

    print("\n********** MAIN MENU ***********")
    print("CHOOSE AN OPERATION. ")
    print("1. ADD A SERVICE")
    print("2. DISPLAY SERVICE PARTS")
    print("3. DELETE SERVICE")
    print("4. VIEW ALL SERVICES")
    print("5. SEARCH FOR SERVICE")
    print("6. GET TOTAL NUMBER OF SERVICES")
    print("7. EXIT")

    # Display choice to user and get user input
    # Then act accordingly



def DisplayChoice():
    choice = ''

    while choice != '7':

        DisplayMenu()

        #GET USER CHOICE
        choice = input("Select an operation (1,2,3,4,5,6,7): ")

        #EXIT THE PROGRAM IF THE INPUT IS 7
        if choice == '7':
            #sys.exit()
            PrintBlankRow(1)
            print("Bye..")

        elif choice == '1':
            AddService()

        elif choice == '2':
            svcid = DisplayService()
            
            PrintBlankRow(1)

            # Display Service Parts
            DisplayParts(svcid)  

            PrintBlankRow(1)  #print a blank line
    
            # Display Parts Menu for user selection
            DisplayPartsChoice(svcid)  

        elif choice == '3':
            DeleteService()

        elif choice == '4':
            ViewService_df()

        elif choice == '5':
            SearchService()

        elif choice == '6':
            PrintBlankRow(1)
            print("There are " + str(GetTotal()-1) + " number of services")
            PrintBlankRow(1)

        else:
            PrintBlankRow(1)
            print("Invalid input!")
            PrintBlankRow(1)        



#FUNCTION TO DISPLAY THE PARTS MENU
def DisplayPartsMenu(SvcId):

    print("\n********** SERVICE PARTS MENU ***********")
    print("CHOOSE AN OPERATION FOR SERVICE ID " + SvcId)
    print("1. ADD SERVICE PART")
    print("2. EDIT SERVICE PART")
    print("3. DELETE SERVICE PART")
    print("4. BACK TO MAIN MENU")
    print("7. EXIT PROGRAM")

    # Display choice to user and get user input
    # Then act accordingly



def DisplayPartsChoice(svcid):
    choice = ''

    while choice != '7':

        DisplayPartsMenu(svcid)

        #GET USER CHOICE
        choice = input("Select an operation (1,2,3,7): ")

        #EXIT THE PROGRAM IF THE INPUT IS 7
        if choice == '7':
            PrintBlankRow(1)
            sys.exit()

        elif choice == '1':
            AddServicePart()
            break

        elif choice == '2':
            #DisplayService()
            pass

        elif choice == '3':
            # delete part
            DeletePart(svcid)
            break

        elif choice == '4':
            # back to main menu
            break


def main():
    #*********************** BEGINING OF MAIN PROGRAM *******************
    DisplayTitle()
    DisplayChoice()


if __name__ == "__main__":
    main()




