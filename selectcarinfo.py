import pandas as pd


CSV_FILE = "car_info.csv"


def GetModelId(model):
    # read file car_info.csv
    df = pd.read_csv(CSV_FILE)
   
    # check model name contains the given string and to ignore case
    # df1 = df[df['Model'].str.contains("(?i)" + model)]
    df1 = df[df['Model'] == model]
    
    if df1.empty or len(model) == 0:
        return(1)
    else:
        # get the id value
        return(df1.iloc[0]['Id'])



# FUNCTION TO VIEW ALL CARS IN THE DATABASE
def ListCarInfo():
    carinfolist = []
    with open(CSV_FILE,"r") as f:
        for line in f:
            line = line.rstrip()
            model = line.split(",", 8)
            if not line: continue
            if model[0] == 'Id': continue
            carinfolist.append(model)   # add car model
    return(carinfolist)


def SelectCarInfo(defmodel=""):
    carinfolist = ListCarInfo()
    
    # get default model id
    defid = GetModelId(defmodel)

    print("\nCHOOSE YOUR CAR MODEL: ")
    for car in carinfolist:
        print(car[0] + ". " + car[1])
 
    choice = ""
    while True: 
        try:
            #GET USER CHOICE
            choice = int(input("\nSelect your car model (1,2), default [%s]: " %defid))
            choice = choice or defid
            carinfo = carinfolist[choice-1]
        except IndexError:
            print("\nInvalid Selection!")
            continue
        except ValueError:
            if (not choice):    # check if choice empty string (user press 'Enter')
                carinfo = carinfolist[int(defid-1)]
                break
            else:
                print("\nInvalid Input!")
                continue
        else:
            #print(carinfo)
            return(carinfo)

    return(carinfo)


# def main():
#     print(SelectCarInfo()[1])
#     #print(SelectCarInfo('bezza')[1])



# if __name__ == "__main__":
#     main()
