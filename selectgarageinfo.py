import pandas as pd


CSV_FILE = "garage_info.csv"


def GetGarageId(garage):
    # read file car_info.csv
    df = pd.read_csv(CSV_FILE)
   
    # check garage name contains the given string and to ignore case
    # df1 = df[df['Model'].str.contains("(?i)" + model)]
    df1 = df[df['SvcCtrName'] == garage]
    
    if df1.empty or len(garage) == 0:
        return(1)
    else:
        # get the id value
        return(df1.iloc[0]['Id'])
       


# FUNCTION TO VIEW ALL SERVICE CENTER INFO IN THE DATABASE
def ListGarageInfo():
    garageinfolist = []
    with open(CSV_FILE,"r") as f:
        for line in f:
            line = line.rstrip()
            shop = line.split(",", 4)
            if not line: continue
            if shop[0] == 'Id': continue
            garageinfolist.append(shop)   # add garage info
    return(garageinfolist)


def SelectGarageInfo(defgrg=""):
    garageinfolist = ListGarageInfo()

    # get default garage id
    defid = GetGarageId(defgrg)
    
    print("\nSELECT THE CAR SERVICE CENTER: ")
    for grg in garageinfolist:
            print(grg[0] + ". " + grg[1] )

    choice = ""
    while True: 
        try:
            #GET USER CHOICE or use default
            choice = int(input("\nSelect the Service Center (1,2,3 etc):, default [%s]: " %defid))
            choice = choice or defid
            garageinfo = garageinfolist[choice-1]
        except IndexError:
            print("\nInvalid Selection!")
            continue
        except ValueError:
            if (not choice):    # check if choice empty string (user press 'Enter')
                garageinfo = garageinfolist[int(defid-1)]
                break
            print("\nInvalid Input!")
            continue
        else:
            return(garageinfo)   # return shop name of user choice

    return(garageinfo)



    


# def main():
#     # today = date.today()
#     # threemonths = datetime.datetime.now() + relativedelta(months=3)
#     # print("Today's date is ", today)
#     # print("3 months from today ", threemonths.strftime("%Y-%m-%d"))
#     print(SelectGarageInfo()[1])



# if __name__ == "__main__":
#     main()
