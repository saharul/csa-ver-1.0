# import only system from os 
from os import system, name
from 05 import *
  
# import sleep to show output for some time period 
from time import sleep 
  
# define our clear function 
def clear_screen(): 
  
    # for windows 
    if name == 'nt': 
        _ = system('cls') 
  
    # for mac and linux(here, os.name is 'posix') 
    else: 
        _ = system('clear') 
  
def main():
    clear_screen()


if __name__ == '__main__':
    main()