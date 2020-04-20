import sys
# import only system from os 
from os import system, name
from collections import namedtuple
from validate import validate
from selectcarinfo import SelectCarInfo
from selectgarageinfo import SelectGarageInfo
from datetime import datetime
from dateutil.relativedelta import relativedelta
from userinputfunct import inputNumber, inputFloat, inputDate
from serviceparts import DeletePart, DisplayParts, AddServicePart
from serviceparts import EditPart, DeletePartInSvcId, ViewAllParts
from serviceparts import SearchServiceParts, GetTotPartsAmt
from print_title import GetTheTitle, clear_screen
import pandas as pd
import shutil
from termcolor import colored, cprint
from tabulate import tabulate





#****************************************************************************************
#PROGRAM BY:    SAHARUL NIZAM SAAIDI                                                    *
#SECTION:       CAR SERVICE INFORMATION SYSTEM                                          *
#DATE:          15TH MARCH 2020                                                         *
#Program No.    YOUR FIRST PROGRAM IN 2020                                              *
#****************************************************************************************

CSV_FILE = "ServiceMaster.csv"
pd.options.display.float_format = '{:,.2f}'.format
pd.options.display.colheader_justify = 'center'
pd.options.display.max_colwidth = 30

# print color
print_red_on_cyan   = lambda x: cprint(x, 'red', 'on_cyan')
print_blue_on_green = lambda x: cprint(x, 'blue', 'on_green')




def DisplayTitle():
    print('*' * 100)
    print("n************************** PROGRAM TO MANAGE CAR SERVICES INFORMATION ****************************n")
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
                + service[4].upper() + ',' + service[5] + ',' + service[6] + ',' + service[7] + ',' + service[8] + 
                ',' + service[9] + '\n')
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
    Service = namedtuple("Service", "Id SvcDate Model Plate SvcCenter Mileage Nxt_Mileage " +
                            "Nxt_Date Labour_Chrg Amount")
    
    id = str(GetMaxId() + 1)

    date = inputDate("Enter Date of Service (DD/MM/YYYY) ", 
                            datetime.today().strftime('%d/%m/%Y'), "%d/%m/%Y")

    carinfo_selected = SelectCarInfo()
    model = carinfo_selected[0]   # Assign chosen model name
    plate = carinfo_selected[1]   # Assign chosen plate no
    
    grginfo_selected = SelectGarageInfo()
    svc_center = grginfo_selected[0]   # Assign chosen service center name
  
    mileage = inputNumber("\nEnter Mileage: ", "")
    nxt_mileage = inputNumber("\nEnter Next Service Mileage: ","")

    defdate = (datetime.strptime(date, "%d/%m/%Y") + relativedelta(months=3)).strftime("%d/%m/%Y")
    nxt_date = inputDate("\nEnter Date of Next Service (DD/MM/YYYY)", defdate, "%d/%m/%Y")

    labour_chrg = inputFloat("\nEnter Labour Charge: ","")

    amount = inputFloat("\nEnter Service Amount: ","")
    newService = Service(id, date, model, plate, svc_center, mileage, nxt_mileage, nxt_date, 
                             labour_chrg, amount)
    SaveService(newService)
    PrintBlankRow(1)
    print("Service was added successfully")
    PrintBlankRow(1)
    
    # Ask user if they want to add service parts
    user_input = input('Do you want to add service parts now? [(y)es/(n)o/(c)ancel] ')
    # input validation  
    if user_input.lower() in ('y', 'yes'):
        svclst = ['', '']  
        svclst[0] = id
        svclst[1] = date
        AddServicePart(svclst)
    


#  FUNCTION DISPLAY DETAILS OF A PARTICULAR SERVICE
def DisplayService2():
    
    ts = shutil.get_terminal_size((80, 20))
    pd.set_option('display.width', ts[0]) # set that as the max width in Pandas
    
    retval = ['','']   # init return value list[Service Id and Service date]
    
    input_id = input("\nEnter the ID of Service to display: ")
    try:
        svcid, date, model, plate, svc_center, mileage, nxt_mileage, nxt_date, amount = GetRecord(input_id).split(",")
        if (svcid == input_id):
            retval[0] = svcid
            retval[1] = date
            DisplayGrid(svcid, date, model, plate, svc_center, mileage, nxt_mileage, nxt_date, amount,True)
        return(retval)
    except AttributeError:
        PrintBlankRow(1)
        print("There was no record with Id " + input_id)
 
    

# FUNCTION TO DELETE A SERVICE FROM THE DATABASE
def DeleteService2():
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
    input('\nPress <ENTER> to continue')



#  FUNCTION TO DELETE A SINGLE PART RECORD FROM THE DATABASE
def DeleteService():

    while True:
        svcid = inputNumber("\nEnter the service id to delete: ", "")

        try:
            df = pd.read_csv(CSV_FILE, index_col=False)
            
            # # 2nd dataframe, the inverse of df1
            df1 = df[df.SvcId == int(svcid)]
            
            # reset df1 to new index
            newindex = [''] * len(df1)  # set newindex array size
            df1.index = newindex            
            
            if (df1.empty == True):
                cprint("\nService Id not found!", 'red', attrs=['bold'], file=sys.stderr)
                break
            
            # show to user the record that he was about to delete
            print(df1)
            # ask for user confirmation
            user_input = input('\nConfirm deletion? [(y)es/(n)o/(c)ancel] ')
            

            # input validation  
            if user_input.lower() in ('y', 'yes'):
     
                #df.index.name = "Key"
                
                # filter the dataframe to user input service id
                # df1 = df[df.SvcId == int(svcid)]

                # sort the dataframe according to svc id and part name
                #df1 = df1.sort_values(['SvcId', 'Name'])
             
                # get the index value of the record. if record not found
                # return 'no match'
                # idx = next(iter(df[df['SvcId'] == int(svcid)].index), 'no match')    

                # delete the part by user input key id
                # df1 = df1.drop(df1.index[idx])
                
                # # 2nd dataframe, the inverse of df1
                df2 = df[df.SvcId != int(svcid)]                

                # # sort by SvcId col
                df = df2.sort_values(['SvcId', 'Model'])

                df.to_csv (CSV_FILE, index = False, header=True)
                
                # Delete all parts for the svc id
                DeletePartInSvcId(svcid)

                print("\nService id " + svcid + " deleted succesfully")
                break

            elif user_input.lower() in ('n', 'no'):  # using this elif for readability
                continue
            elif user_input.lower() in ('c', 'cancel'):  # Cancel deletion process
                break

            else:
                # ... error handling ...
                print("Error: Input " + user_input + " unrecognised.")
                break

        except IndexError:
            print("\nkey id " + str(svcid) + " does not exist!")
            break
        except Exception as err:
            print(err)
            break
  

    input('\nPress <ENTER> to continue')




def EditService():
    # get the service id
    svcid = int(inputNumber("\nEnter the service id to edit: ", ""))

    try:
        df = pd.read_csv(CSV_FILE)

        # filter the dataframe to user input service id
        df1 = df[df.SvcId == svcid]

        # get the index value of user keyed in service id
        # return 'no match' if not found
        index = next(iter(df1[df1['SvcId']==svcid].index), 'no match')    
        
        # get the service date of the service id. Set as default date
        defdate = df1.loc[index, 'SvcDate']
        defmodel = df1.loc[index, 'Model']
        # defplate = df1.loc[index, 'Plate']
        defcenter = df1.loc[index, 'Svc_Center']
        defmile = df1.loc[index, 'Mileage']
        defnxtmile = df1.loc[index, 'Nxt_Mileage']
        defnxtdate = df1.loc[index, 'Nxt_Date']
        defamount = df1.loc[index, 'Amount']
        
        date = inputDate("Enter Service Date ", defdate, "%d/%m/%Y")
        carinfo_selected = SelectCarInfo(defmodel)
        model = carinfo_selected[1]   # Assign chosen model name
        plate = carinfo_selected[2]   # Assign chosen plate no
        
        grginfo_selected = SelectGarageInfo(defcenter)
        svc_center = grginfo_selected[1]   # Assign chosen service center name
      
        mileage = inputNumber("\nEnter Mileage, default [%s]: " %defmile, str(defmile))
        nxt_mileage = inputNumber("\nEnter Next Service Mileage, default [%s]: " %defnxtmile, str(defnxtmile))
        nxt_date = inputDate("\nEnter Date of Next Service (DD/MM/YYYY", defnxtdate, "%d/%m/%Y")
        amount = inputFloat("\nEnter Service Amount, default [%s]: " %defamount, str(defamount))

        # # Assign the modification made to dataframe
        df1.at[index, 'SvcDate'] = date
        df1.at[index, 'Model'] = model
        df1.at[index, 'Plate'] = plate
        df1.at[index, 'Svc_Center'] = svc_center
        df1.at[index, 'Mileage'] = mileage
        df1.at[index, 'Nxt_Mileage'] = nxt_mileage
        df1.at[index, 'Nxt_Date'] = nxt_date
        df1.at[index, 'Amount'] = amount


        # # # 2nd dataframe, the inverse of df1
        df2 = df[df.SvcId != svcid]

        # # # combine df1 and df2
        frames = [df2, df1]
        df = pd.concat(frames, ignore_index=True)

        # # # sort by SvcId col
        df = df.sort_values(['SvcId'])

        # write the result back to csv file
        df.to_csv (CSV_FILE, index = False, header=True)

        print("\nService was succesfully updated!")
        
        input('\nPress <ENTER> to continue')
        
    
    except KeyError: 
        print("Could not find service id " + str(svcid))
    
    except Exception as Err:
        print(Err)



# FUNCTION TO VIEW THE SERVICE BASE ON SERVICE ID
def DisplayService(svc_id):

    retval = ['','']   # init return value list[Service Id and Service date]
    # get svc id input from user
    # svc_id = input("\nEnter the ID of Service to display: ")
    # reading the service master csv file
    df = pd.read_csv(CSV_FILE, index_col=False)    

    # limit the name column width to 35
    df['Model'] = df['Model'].str[:15]



    # filter dataframe to show parts for user selected service id
    df_svc = df[df['SvcId'] == int(svc_id)]

    df_svc = df_svc[['SvcId','SvcDate','Model', 'Svc_Center', 'Nxt_Mileage', 'Nxt_Date', 
                            'Labour_Chrg', 'Amount']]
    
    # hide df_svc index
    newindex = [''] * len(df_svc)  # set newindex array size
    df_svc.index = newindex      
    
    if (df_svc.empty != True):
        # # set index name to 'Key'
        # df_svc.index.name = "Key"
        # get svc id
        retval[0] = svc_id
        # get service date
        retval[1] = df_svc.loc[df_svc.index[0], 'SvcDate']

        PrintBlankRow(1)
        header = ("Id","Date", "Car Model", "Service Center", 
                        "Next Mileage", "Next Date", "Labour", "Amount")
        print(tabulate(df_svc, headers=header, tablefmt="psql", floatfmt=".2f", showindex=False))
         
    return(retval)



def ViewAllServices():
    # df = pd.read_csv(CSV_FILE, index_col=False)
    # blankIndex=[''] * len(df)  #hide index column
    # df.index = blankIndex
    
    width = shutil.get_terminal_size((80, 20)) # find the width of the user's terminal window
    pd.set_option('display.width', width[0]) # set that as the max width in Pandas

    df = pd.read_csv(CSV_FILE, index_col=False)

    # limit the name column width to 35
    df['Model'] = df['Model'].str[:15]
    df['Svc_Center'] = df['Svc_Center'].str[:18]



    # filter the dataframe remove svcid = 0
    df = df[df.SvcId != 0]

    if (width[0] > 100) :
        df = df[['SvcId','SvcDate','Model', 'Svc_Center', 'Nxt_Mileage', 
                         'Nxt_Date', 'Labour_Chrg', 'Amount']]

        header = ("Id", "Date", "Car Model", "Service Center", 
                        "Next Mileage", "Next Date", "Labour", "Amount")
        print(tabulate(df, headers=header, tablefmt="psql", floatfmt=".2f", showindex=False))
    else:
        blankIndex=[''] * len(df)  #hide index column
        df.index = blankIndex
        print(df)
        
    input('\nPress <ENTER> to continue')
    


# display services base on a list of given SvcIds
def ViewServiceList(lstid):
    # reading the service master csv file
    df = pd.read_csv(CSV_FILE, index_col=False)    
    # filter dataframe to show parts for user selected service id
    df_svc = df[df['SvcId'].isin(lstid)]
    # set index name to 'Key'
    df_svc.index.name = "Key"
    # print blank row                    
    PrintBlankRow(1)
    # show the result
    return(df_svc)
    


#  FUNCTION TO SEARCH FOR A SERVICE IN THE DATABASE
def SearchService_prev():
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



#  FUNCTION TO SEARCH FOR A SERVICE IN THE DATABASE
def SearchService():
    criteria = input("Enter a search criteria: ")
    lstid = []
    # iterate every line in csv file
    with open(CSV_FILE,"r") as f:
        for line in f:
            line = line.rstrip()
            if line.upper().find(criteria.upper()) != -1:
                id, date, model, plate, svc_center, mileage, nxt_mileage, nxt_date, labour_chrg, amount = line.split(",")
                lstid.append(id)

    if len(lstid) == 0:
        print("\nSearch string was not found!")
    else:
        print(ViewServiceList(lstid))
        
    input('\nPress <ENTER> to continue')



def SearchService2():
    # Concatenation and merge 2 csv files
    # import pandas as pd

    criteria = input("Enter a search criteria: ")

    # declare list var CSV_FILE
    CSV_FILE = ['', '']
    CSV_FILE[0] = "ServiceMaster.csv"
    CSV_FILE[1] = "ServiceParts.csv"

    # read the csv file ServiceMaster.csv
    df = pd.read_csv(CSV_FILE[0])

    # apply lambda function search every cell in df for string contains 'SYNTIUM'
    # return a series with True and False values
    s = df.apply(lambda row: row.astype(str).str.contains(criteria, case=False).any(), axis=1)

    # name the series as 'Found'
    s.name = 'Found'

    # join the series with the dataset
    df_join = pd.concat([s, df], axis=1)

    # filter the dataset to get only row where Found is True
    df = df_join[df_join['Found'] == True]

    if (len(df) > 0):

        # display the dataset
        df = df[['SvcId', 'SvcDate', 'Model', 'Mileage','Nxt_Date','Nxt_Mileage', 'Labour_Chrg', 'Amount']]    
        header = ("Id", "Date", "Model", "Mileage", "Nxt Svc Date", "Nxt Mileage", "Labour Chrg", "Amount")
        print(tabulate(df, headers=header, tablefmt="psql", floatfmt=".2f", showindex=False))
 
    else:
        print("Search string was not found!")
    
    input('\nPress <ENTER> to continue')


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

    print_red_on_cyan("\n********** MAIN MENU ***********")
    print("CHOOSE AN OPERATION: ")
    menu = []
    menu.append("01. ADD A NEW SERVICE")
    menu.append("02. DISPLAY SERVICE & PARTS")
    menu.append("03. DELETE A SERVICE")
    menu.append("04. EDIT SERVICE")
    menu.append("05. SEARCH FOR SERVICES")
    menu.append("06. GET TOTAL NO OF SERVICES")
    menu.append("07. SPARE PART INFO")
    menu.append("08. VIEW ALL SERVICES")
    menu.append("10. VIEW NEXT SERVICE DATE")
    menu.append("09. EXIT")

    # Display choice to user and get user input
    # Then act accordingly
    for x in range(len(menu)):
        print(menu[x])



def DisplayChoice():
    choice = ''

    while choice != '09':
        GetTheTitle()
        DisplayMenu()

        #GET USER CHOICE
        choice = input("\nSelect an operation (01,02,03..09): ")

        #EXIT THE PROGRAM IF THE INPUT IS 7
        if choice == '09':
            #sys.exit()
            PrintBlankRow(1)
            print(colored("Bye..", 'yellow', attrs=['reverse', 'blink']))

        elif choice == '01':
            # clear the screen
            clear_screen()
            
            AddService()
        
        # display Service information and its Parts
        elif choice == '02':
            # # clear the screen
            clear_screen()
            # get svc id input from user
            svc_id = input("\nEnter the Service id: ")
            # display service and return value list of svcid and date
            svclst = DisplayService(svc_id)
            if len(svclst[0]) == 0:
                print("\nService Id not found or does not exist!")
                input('\nPress <ENTER> to continue')

            else:
                # Display Service Parts
                DisplayParts(svclst[0])  
                PrintBlankRow(1)  #print a blank line

        elif choice == '03':
            clear_screen()
            DeleteService()

        elif choice == '04':
            clear_screen()
            EditService()             

        elif choice == '05':
            clear_screen()
            SearchService2()

        elif choice == '06':
            clear_screen()
            PrintBlankRow(1)
            print(colored("There are " + str(GetTotal()-1) + " number of services!", 'green'))
            PrintBlankRow(1)
            input('\nPress <ENTER> to continue')
            
        elif choice == '07':
            clear_screen()
            DisplayPartsChoice() 

        elif choice == '08':
            clear_screen()
            ViewAllServices()
            
        elif choice == '10':
            clear_screen()
            ViewNxtSvcDate()
 
        else:
            PrintBlankRow(1)
            print("Invalid input!")
            PrintBlankRow(1)
            input('\nPress <ENTER> to continue')
            


#FUNCTION TO DISPLAY THE PARTS MENU
def DisplayPartsMenu():

    print_blue_on_green("\n********** PARTS MENU ***********")
    print("CHOOSE AN OPERATION:")
    
    menu = []
    menu.append("1. ADD A NEW SERVICE PART")
    menu.append("2. EDIT A SERVICE PART")
    menu.append("3. DELETE A SERVICE PART")
    menu.append("4. GO BACK TO MAIN MENU")
    menu.append("5. VIEW ALL SERVICE PARTS")
    menu.append("6. SEARCH SERVICE PARTS")
    menu.append("9. EXIT PROGRAM")
    
    # Display choice to user and get user input
    # Then act accordingly
    for x in range(len(menu)):
        print(menu[x])




def DisplayPartsChoice():
    choice = ''

    while (choice != 9):
        GetTheTitle()
        DisplayPartsMenu()

        #GET USER CHOICE
        choice = input("\nSelect an operation (1,2..9): ")

        #EXIT THE PROGRAM IF THE INPUT IS 7
        if choice == '9':
            PrintBlankRow(1)
            print("Bye..")
            # exit the system
            sys.exit()

        #Add Service Part
        elif choice == '1':       
            # get svc id input from user
            svc_id = inputNumber("\nEnter the Service id: ","")

            # display service and return value list of svcid and date
            svclst = DisplayService(svc_id)
            
            # Service Id not found
            if len(svclst[0]) == 0:
                print("\nService Id not found or does not exist!")
                input('\nPress <ENTER> to continue')

            else:
                # Display Service Parts
                DisplayParts(svclst[0])  
                # Add the part       
                AddServicePart(svclst)
                # get total sum of parts for the svc id
                # and update the total
                UpdSvcAmt(svc_id, GetTotPartsAmt(svc_id))
            
        # edit the Service Part
        elif choice == '2':
            # get svc id input from user
            svc_id = input("\nEnter the Service id: ")

            # display service and return value list of svcid and date
            svclst = DisplayService(svc_id)
            
            if len(svclst[0]) == 0:
                print("\nService Id not found or does not exist!")
                input('\nPress <ENTER> to continue')

            else:
                # Display Service Parts
                DisplayParts(svclst[0])  
                # edit part
                EditPart(svc_id)
                # get total sum of parts for the svc id
                # and update the total Amount
                UpdSvcAmt(svc_id, GetTotPartsAmt(svc_id))


        # delete the Service Part
        elif choice == '3':
            # get svc id input from user
            svc_id = input("\nEnter the Service id: ")

            # display service and return value list of svcid and date
            svclst = DisplayService(svc_id)
            
            if len(svclst[0]) == 0:
                print("\nService Id not found or does not exist!")
                input('\nPress <ENTER> to continue')

            else:
                # Display Service Parts
                DisplayParts(svclst[0])  
                # delete part
                DeletePart(svc_id)
                # get total sum of parts for the svc id
                # and update the total
                UpdSvcAmt(svc_id, GetTotPartsAmt(svc_id))
                 
                        
        elif choice == '4':
            # back to main menu
            break

        elif choice == '5':
            # back to main menu
            ViewAllParts()
        
        elif choice == '6':
            # back to main menu
            SearchServiceParts()

        else:
            PrintBlankRow(1)
            print("Invalid input!")
            PrintBlankRow(1)
            input('\nPress <ENTER> to continue')
            



def UpdSvcAmt(svcid, amount):
    svcid = int(svcid)
    # open ServiceMaster.csv file
    df = pd.read_csv(CSV_FILE)

    # filter the dataframe to pass service id
    df1 = df[df.SvcId == svcid]

    # get the index value of the service id row
    index = next(iter(df1[df1['SvcId']==svcid].index), 'no match') 

    # if index not equal to string 'no match' then update the amount field
    if (index != 'no match'):
        df1.at[index, 'Amount'] = amount

        # 2nd dataframe, the inverse of df1
        df2 = df[df.SvcId != svcid]

        # # # combine df1 and df2
        frames = [df2, df1]
        df = pd.concat(frames, ignore_index=True)

        # # # sort by SvcId col
        df = df.sort_values(['SvcId'])

        # Write back the updated dataframe to csv file
        df.to_csv (CSV_FILE, index = False, header=True)




def ViewNxtSvcDate():
    df = pd.read_csv(CSV_FILE, usecols=['Model', 'Nxt_Date'])
    
    df_nsd = df.groupby(['Model']).last()
    
    header=("Model", "Next Svc Date")

    print(tabulate(df_nsd, headers=header, tablefmt="psql"))
    input('\nPress <ENTER> to continue')



def ResizeTerm():
    sys.stdout.write("\x1b[8;{rows};{cols}t".format(rows=32, cols=120))



def main():
    #*********************** BEGINING OF MAIN PROGRAM *******************
    ResizeTerm()
    GetTheTitle()
    DisplayChoice()


if __name__ == "__main__":
    main()




