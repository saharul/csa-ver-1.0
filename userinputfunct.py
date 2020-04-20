import datetime as dt
from datetime import datetime

def inputNumber(message, defval):
  while True:
    try:
       userInput = int(input(message))       
    except ValueError:
       if(not(defval and defval.strip())):
         print("Not a Number! Try again.")
         continue
       else:
         return(str(defval))
    else:
       return(str(userInput))

def inputFloat(message, defval):
   while True:
      try:
        userInput = float(input(message))
      except ValueError:
         if(not(defval and defval.strip())):
            print("Not a valid number value! Try again.")
            continue
         else:
            return("{:.2f}".format(defval))
      else:
         return("{:.2f}".format(userInput))


def inputDate(message, defdate, datformat):
    message = message + ", default [%s]: " %defdate
    while True:
        try:
            userInput = input(message)
            userInput = userInput or defdate
            dt.datetime.strptime(userInput, datformat)
        except ValueError:
            print("Incorrect data format, should be DD/MM/YYYY")
            continue
        else:
            return(userInput)



def main():
   #  value = inputFloat("Please input an amount: ")
   #  print(value)
   #  print(type(value))
    value = inputFloat("Please input an amount: ", "")
    print(value)
    #inputDate("Please enter date: ", "02/03/2020", "%d/%m/%Y")


if __name__ == "__main__":
    main()