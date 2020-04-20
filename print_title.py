import os
from os import system, name
from termcolor import colored, cprint


    
            
def DisplayTitle(str_ttl, str_star, str_sep):
    clear_screen()

    #print(colored('hello', 'red'), colored('world', 'green'))
    
    cprint(str_star, 'green')
    cprint(str_sep, 'green')
    #print(str_ttl.center(os.get_terminal_size().columns))
    cprint(str_ttl.center(os.get_terminal_size().columns), 'green', attrs=['bold'])
    cprint(str_sep, 'green')
    cprint(str_star, 'green')
    

def GetTheTitle():
    str_ttl1 = " CAR SERVICE INFORMATION SYSTEM "
    scr_wdth = os.get_terminal_size().columns
    star_lng = int(scr_wdth) // 2 - len(str_ttl1) // 2
    str_ttl = ('n' + '*' * (star_lng-1)) + str_ttl1 + ('*' * (star_lng-1) + 'n')
    str_star = ('*') * scr_wdth
    str_sep = ('*' + ' ' * (star_lng-1)) + (' ' * len(str_ttl1))  + (' ' * (star_lng-1) + '*')
    
    DisplayTitle(str_ttl, str_star, str_sep)



# FUNCTION TO CLEAR SCREEN
def clear_screen(): 
  
    # for windows 
    if name == 'nt': 
        _ = system('cls') 
  
    # for mac and linux(here, os.name is 'posix') 
    else: 
        _ = system('clear') 

# def main():
    # #GetTheTitle()


# if __name__ == "__main__":
    # main()
