
#****************************************************************************************
#PROGRAM BY:    SAHARUL NIZAM SAAIDI                                                    *
#SECTION:       SERVICE SPARE PARTS                                                     *
#DATE:          16TH MARCH 2020                                                         *
#Program No.    PROGRAM IN 2020                                                         *
#****************************************************************************************

import pandas as pd
from collections import namedtuple
from userinputfunct import inputNumber, inputFloat
from tabulate import tabulate
from userinputfunct import inputDate


pd.options.display.max_colwidth = 25


# VARIABLE CSV_FILE STORE LIST OF CSV FILE USED IN THIS APP
CSV_FILE = ["ServiceMaster.csv", "ServiceParts.csv", "partslist.csv"]


#  FUNCTION TO EDIT A SINGLE SPARE PART RECORD IN THE DATABASE
def EditPart(svcid):
    # get the key id
    keyid = int(inputNumber("\nEnter the key id of the part name to edit: ", ""))

    try:
        df = pd.read_csv(CSV_FILE[1])
        #df.index.name = "Key"

        # filter the dataframe to user input service id
        df1 = df[df.SvcId == int(svcid)]
        
        # sort the dataframe according to svc id and part name
        df1 = df1.sort_values(['SvcId', 'Name'])
        
        # reset df1 to new index
        newindex = [''] * len(df1)  # set newindex array size
        for i in range(len(df1)):
            newindex[i] = i  #set index column
        
        df1.index = newindex

        df1.index.name='Key'

        # get the name of the part
        defpartname = df1.loc[keyid, 'Name']
        defqty = str(df1.loc[keyid, 'Qty'])
        defunitprice = str(df1.loc[keyid, 'UnitPrice'])
        defdisc = str(df1.loc[keyid, 'Disc'])

        partname = input("Enter Part Name [%s] :" %defpartname)
        partname = partname or defpartname
        qty = inputNumber("Enter Spare Part qty [%s] :" %defqty, defqty)
        unitprice = inputFloat("Enter unit price [%s]: " %defunitprice, defunitprice)
        disc = inputFloat("Enter discount [%s]: " %defdisc, defdisc)

        amount = ((int(qty) * float(unitprice)) - float(disc))

        # Assign the modification made to dataframe
        df1.at[keyid, 'Name'] = partname
        df1.at[keyid, 'Qty'] = int(qty)
        df1.at[keyid, 'UnitPrice'] = float(unitprice)
        df1.at[keyid, 'Disc'] = float(disc)
        df1.at[keyid, 'Amount'] = str(round(amount, 2))


        # # 2nd dataframe, the inverse of df1
        df2 = df[df.SvcId != int(svcid)]

        # # combine df1 and df2
        frames = [df2, df1]
        df = pd.concat(frames, ignore_index=True)

        # # sort by SvcId col
        df = df.sort_values(['SvcId', 'Name'])

        # write the result back to csv file
        df.to_csv (CSV_FILE[1], index = False, header=True)

        print("\nPart was succesfully updated!")
        
        input('\nPress <ENTER> to continue')
        
    
    except KeyError: 
        print("Could not find key no " + str(keyid))
    
    except Exception as Err:
        print(Err)


#  FUNCTION TO SAVE A SINGLE SPARE PART RECORD INTO THE DATABASE
def SavePart(Part):
    
    # Open dataframe from csv_file
    df = pd.read_csv(CSV_FILE[1])
    
    df_newrow = pd.DataFrame({
     "SvcId":[Part[0]], 
     "Date":[Part[1]], 
     "Name": [Part[2].upper()], 
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
        keyid = int(inputNumber("\nEnter the key id of the part name to delete: ", ""))

        user_input = input('Confirm deletion? [(y)es/(n)o/(c)ancel] ')

        # input validation  
        if user_input.lower() in ('y', 'yes'):
            try:
                df = pd.read_csv(CSV_FILE[1])
                #df.index.name = "Key"
                
                # filter the dataframe to user input service id
                df1 = df[df.SvcId == int(svcid)]

                # sort the dataframe according to svc id and part name
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

                df.to_csv (CSV_FILE[1], index = False, header=True)

                print("\nParts " + partname + " deleted succesfully")

                #display service info
                ViewService(svcid)

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
    
    df = pd.read_csv(CSV_FILE[1], index_col=False)

    df['Name'] = df['Name'].str[:35]
   
    # filter dataframe to show parts for user selected service id
    df_sel = df[df['SvcId'] == int(svcid)]
    
    # drop column date if svc id != 0
    if (svcid != '0'):
        df_sel = df_sel.drop(columns=['Date'])
        header = ("Key", "Id", "Name", "Qty", "Unit Price", "Discount", "Amount")
    else:
        header = ("Key", "Id", "Date", "Name", "Qty", "Unit Price", "Discount", "Amount")


    if (df_sel.empty != True):
        # sort dataframe by SvcId and Part Name
        df_sel = df_sel.sort_values(['SvcId', 'Name'])


        # # reset index to newindex list
        newindex = [''] * len(df_sel)  # set newindex array size
        for i in range(len(df_sel)):
            newindex[i] = i  #set index column
        df_sel.index = newindex

        # # set index name to Key
        df_sel.index.name='Key'

        PrintBlankRow(1)

        print(tabulate(df_sel, headers=header, tablefmt="psql", floatfmt=".2f", showindex=True))
 
    else:
        print("\n===> There are no parts for this service!")

    input('\nPress <ENTER> to continue')



# FUNCTION TO GET PART NAME FROM USER
def GetPartName():
    while True:
        userinput = input("\nEnter part name or key no (press 'Enter' to view part list): ")

        if not userinput.lstrip():
            df = ShowParts()
        else:
            try:
                val = int(userinput)

                # filter dataframe to show parts for user selected key no
                dfpart = df.loc[val]
    
                # get the part name
                partname = dfpart.iloc[0]
                break
            except ValueError:
                #user enter part name
                partname = userinput
                break
            except KeyError:
                print("\nKey No does not exist!")

    return(partname)


# FUNCTION TO DISPLAY ALL PARTS USED IN THIS APP
def ShowParts():
    df = pd.read_csv(CSV_FILE[1])

    df = df.sort_values(['Name'])

    # reset index to newindex list
    newindex = [''] * len(df)  # set newindex array size
    for i in range(len(df)):
        newindex[i] = i  #set index column
    df.index = newindex

    df.index.name = "Key"
    
    # dropping ALL duplicte values 
    df.drop_duplicates(subset ="Name", keep = "first", inplace = True)
    
    df = df[["Name"]]

    #df[['Name']]    

    print(tabulate(df, showindex=True, headers=["Key", "Name"]))
    #print(df[['Name']])
    return(df)


#  FUNCTION TO ADD PART OF A PARTICULAR SERVICE ID
def AddServicePart(svclst):
    
    try:
        print("Svc Id: " + svclst[0] )               # Date: " + svclst[1])
   
        while (True) :
            ServicePart = namedtuple("ServicePart", "SvcId Date Name Qty UnitPrice Disc Amount")
            
            # get the date
            date = inputDate("Enter Date (DD/MM/YYYY) ", svclst[1], "%d/%m/%Y")

            # get the part name from user
            name = GetPartName() 
            # get the part qty used
            qty = inputNumber("Enter Spare Part qty: ", "")
            # get the part unit price
            unitprice = inputFloat("Enter unit price: ", "")
            # get the discount amount in rm
            disc = inputFloat("Enter discount (in RM): ", "")
            # calculate the amount
            amount = (float(qty) * float(unitprice)) - float(disc)
            ServicePart = ServicePart(svclst[0], date, name, qty, unitprice, disc, amount)
            
            SavePart(ServicePart)
            
            PrintBlankRow(1)
            print("Service part was added successfully")
            PrintBlankRow(1)
            
            user_input = input('\nAdd another part? (y/n)')
            if (user_input.lower() == 'n'):
                break
    except Exception as err:
        print(err)
 
def GetTotPartsAmt(svcid):
    svcid = int(svcid)  # make sure integer value

    df = pd.read_csv(CSV_FILE[1])
    df = df.sort_values(['SvcId'])
    df = df.groupby(['SvcId'])[['Amount']].sum()

    return("{:.2f}".format(df.loc[svcid,'Amount']))



def PrintBlankRow(numrow):
    i = 1
    while i <= numrow:
       print("\n")
       i += 1


# FUNCTION TO VIEW THE SERVICE BASE ON SERVICE ID
def ViewService(svcid):

    df = pd.read_csv(CSV_FILE[0], index_col=False)

    # filter dataframe to show parts for user selected service id
    df_svc = df[df['SvcId'] == int(svcid)]
    
    # blankIndex=[''] * len(df)  #hide index column
    # df.index.name = "Key"
    df_svc.index.name = "Key"
    
    svcdate = df_svc.loc[df_svc.index[0], 'SvcDate']

    PrintBlankRow(1)
    print(svcdate)


#  FUNCTION TO DELETE ALL PART RECORD IN A GIVEN SERVICE ID 
def DeletePartInSvcId(svcid):

    try:
        # read ServiceParts database
        df = pd.read_csv(CSV_FILE[1])
        
        # get dataframe that is not in svc id passed
        df2 = df[df.SvcId != int(svcid)]

        # sort by SvcId col
        df = df2.sort_values(['SvcId', 'Name'])

        # write back the dataframe to csv file
        df.to_csv (CSV_FILE[1], index = False, header=True)

    except Exception as Err:
        print(Err)



def ViewAllParts():
    CSV_FILE = "ServiceParts.csv"

    df = pd.read_csv(CSV_FILE)

    df = df.sort_values(['SvcId'])

    # dropping ALL duplicte values 
    # df.drop_duplicates(subset ="Name", keep = "first", inplace = True)

    #df[['Name']]

    headers = ["Svc Id", "SvcDate", "Part Name", "Qty", "Unit Price", "Disc", "Amount"]

    print(tabulate(df, showindex=False, headers=headers, tablefmt="psql", floatfmt=".2f"))

    input('\nPress <ENTER> to continue')


def SearchServiceParts():
    # Concatenation and merge 2 csv files
    import pandas as pd


    criteria = input("Enter a search criteria: ")

    # declare list var CSV_FILE
    CSV_FILE = ['', '']
    CSV_FILE[0] = "ServiceMaster.csv"
    CSV_FILE[1] = "ServiceParts.csv"

    # read the csv file ServiceMaster.csv
    df = pd.read_csv(CSV_FILE[0])
    # read the csv file ServiceParts.csv
    df1 = pd.read_csv(CSV_FILE[1])

    # merge the two files base on SvcId 
    df_merge_col = pd.merge(df1, df, on='SvcId')

    # apply lambda function search every cell in df for string contains 'SYNTIUM'
    # return a series with True and False values
    s = df_merge_col.apply(lambda row: row.astype(str).str.contains(criteria, case=False).any(), axis=1)

    # name the series as 'Found'
    s.name = 'Found'

    # join the series with the merged dataset
    df_col = pd.concat([s, df_merge_col], axis=1)

    # filter the dataset to get only row where Found is True
    df = df_col[df_col['Found'] == True]

    if (len(df) > 0):

        # display the dataset
        df = df[['SvcId', 'Date', 'Name', 'UnitPrice', 'Model', 'Svc_Center']]    
        header = ("Id", "Date", "Part Name", "Unit Price", "Model", "Svc Center")
        print(tabulate(df, headers=header, tablefmt="psql", floatfmt=".2f", showindex=False))
 
    else:
        print("Search string was not found!")
    
    input('\nPress <ENTER> to continue')


# def main():
#     #ViewParts()
#     # DisplayParts("4")
#     # AddServicePart(4, "16/04/2020")
#     #DeletePart()


# if __name__ == "__main__":
#     main()

