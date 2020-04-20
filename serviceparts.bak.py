
#****************************************************************************************
#PROGRAM BY:    SAHARUL NIZAM SAAIDI                                                    *
#SECTION:       SERVICE SPARE PARTS                                                     *
#DATE:          16TH MARCH 2020                                                         *
#Program No.    PROGRAM IN 2020                                                         *
#****************************************************************************************

import pandas as pd
from collections import namedtuple
from userinputfunct import inputNumber, inputFloat

CSV_FILE = "ServiceParts.csv"


def DisplayGrid(id,date,name,qty,unitprice,discount,amount, showtitle=False):
    # if showtitle == True:
    #     id_t,date_t,model_t,plate_t,svc_center_t,mileage_t,nxt_mileage_t,nxt_date_t,amount_t = GetRecord("Id").split(",")
    #     print('{0: <5}'.format(id_t) + '{0: <14}'.format(date_t) + '{0: <25}'.format(model_t) + '{0: <10}'.format(plate_t) + 
    #         '{0: <25}'.format(svc_center_t) + '{0: >12}  '.format(mileage_t) + '{0: >12}  '.format(nxt_mileage_t) +
    #         '{0: <14}'.format(nxt_date_t) + '{0: >10}  '.format(amount_t))
    print('{0: <5}'.format(id) + '{0: <14}'.format(date) + '{0: <35}'.format(name) + '{0: >3}'.format(qty) + 
        '{0: >13}'.format(unitprice) + '{0: >7}  '.format(discount) + '{0: >10}'.format(amount))


# FUNCTION TO VIEW ALL PARTS IN THE DATABASE
def ViewParts():
    with open(CSV_FILE,"r") as f:
        for line in f:
            line = line.rstrip()
            id, date, name, qty, unitprice, discount, amount = line.split(",")
            if not line: continue
            DisplayGrid(id,date,name,qty,unitprice,discount,amount,False)
    #PrintBlankRow(1)


#  FUNCTION TO RETRIEVE A SINGLE SERVICE RECORD FROM THE DATABASE
def GetRecord(serviceid):
    with open(CSV_FILE,"r") as f:
         for line in f:
            line = line.rstrip()
            id = line.split(",", 1)
            if (id[0] == serviceid):
                return line


#  FUNCTION TO SAVE A SINGLE SERVICE RECORD INTO THE DATABASE
def SavePart(Part):
    
    # Open dataframe from csv_file
    df = pd.read_csv(CSV_FILE)
    
    df_newrow = pd.DataFrame({
     "SvcId":[Part[0]], 
     "Date":[Part[1]], 
     "Name": [Part[2]], 
     "Qty": [Part[3]],
     "UnitPrice": [Part[4]],
     "Disc": [Part[5]],
     "Amount": [Part[6]] })
    
    # # Append new row to dataframe
    df = df.append(df_newrow, ignore_index=True, sort=False)

    # # Write back new dataframe to csv file
    df.to_csv (r'ServiceParts.csv', index = False, header=True)

    PrintBlankRow(1)


#  FUNCTION TO DELETE A SINGLE PART RECORD FROM THE DATABASE
def DeletePart(svcid):

    while True:
        keyid = int(inputNumber("\nEnter the key id of the part to delete: "))

        user_input = input('Confirm deletion? [Y/N/C] ')

        # input validation  
        if user_input.lower() in ('y', 'yes'):
            try:
                df = pd.read_csv(CSV_FILE)
                #df.index.name = "Key"
                
                # filter the dataframe to user input service id
                df1 = df[df.SvcId == int(svcid)]

                df1 = df1.sort_values(['SvcId', 'Name'])
             
                # reset df1 to new index
                newindex = [''] * len(df1)  # set newindex array size
                for i in range(len(df1)):
                    newindex[i] = i  #set index column
                
                df1.index = newindex

                df1.index.name='Key'

                # get the name of the part
                partname = df1.loc[keyid, 'Name']

                # delete the part by user input key id
                df1 = df1.drop(df1.index[keyid])

                # # 2nd dataframe, the inverse of df1
                df2 = df[df.SvcId != int(svcid)]

                # # combine df1 and df2
                frames = [df2, df1]
                df = pd.concat(frames, ignore_index=True)

                # # sort by SvcId col
                df = df.sort_values(['SvcId', 'Name'])

                df.to_csv (CSV_FILE, index = False, header=True)

                print("\nParts " + partname + " deleted succesfully")

                # display back the new parts list
                DisplayParts(svcid)

            except IndexError:
                print("\nkey id " + str(keyid) + " does not exist!")

            break
        elif user_input.lower() in ('n', 'no'):  # using this elif for readability
            continue
        elif user_input.lower() in ('c', 'cancel'):  # Cancel deletion process
            break

        else:
            # ... error handling ...
            print("Error: Input " + user_input + " unrecognised.")
            break
    

#  FUNCTION DISPLAY DETAILS PARTS OF A PARTICULAR SERVICE ID
def DisplayParts(svcid):
    newindex = []
    
    df = pd.read_csv(CSV_FILE, index_col=False)
   
    # filter dataframe to show parts for user selected service id
    df_sel = df[df['SvcId'] == int(svcid)]

    # sort dataframe by SvcId and Part Name
    df_sel = df_sel.sort_values(['SvcId', 'Name'])

    # reset index to newindex list
    newindex = [''] * len(df_sel)  # set newindex array size
    for i in range(len(df_sel)):
        newindex[i] = i  #set index column
    df_sel.index = newindex

    # set index name to Key
    df_sel.index.name='Key'

    PrintBlankRow(1)

    print(df_sel)  #show the parts

 


#  FUNCTION TO ADD PART OF A PARTICULAR SERVICE ID
def AddServicePart(svcid, date):
    
    ServicePart = namedtuple("ServicePart", "SvcId Date Name Qty UnitPrice Disc Amount")
    
    name = input("Enter Spare Part name: ")
    
    qty = inputNumber("Enter Spare Part qty: ")
    unitprice = inputFloat("Enter unit price: ")
    disc = inputFloat("Enter discount: ")

    amount = inputFloat("Enter part amount: ")
    ServicePart = ServicePart(svcid, date, name, qty, unitprice, disc, amount)
    
    SavePart(ServicePart)
    
    PrintBlankRow(1)
    print("Service part was added successfully")
    PrintBlankRow(1)
    
    print("Parts added succesfully")



def PrintBlankRow(numrow):
    i = 1
    while i <= numrow:
       print("\n")
       i += 1





# def main():
#     #ViewParts()
#     # DisplayParts("4")
#     # AddServicePart(4, "16/04/2020")
#     #DeletePart()


# if __name__ == "__main__":
#     main()