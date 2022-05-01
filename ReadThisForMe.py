import sys 

import subprocess
try:
    from PIL import Image
except ImportError:
    import Image


import keyboard
import os

dirName =  os.getcwd()
screenshotsDir = dirName + '/screenshots'


lang = sys.argv[1]

#print(choice)

print("Hello welcome to ReadThisForMe")
# languages = {"1": "eng","2":"tam","3":"ara",
# "4":"chi_sim", "5":"spa", "6":"deu",
# "7":"fra","8":"ita","9":"hin" }
# print(languages)
# lang = languages[choice]

while True: 
    
        try:  # used try so that if user pressed other than the given key error will not be shown
            if keyboard.is_pressed('ctrl'):
                if keyboard.is_pressed('alt'):
                    if keyboard.is_pressed('x'):
                        print("U can screenshot")
                        print('.\dist\Snip\Snip.exe ' +lang)
                        subprocess.call(['python', 'Snip.py', lang])
                        #subprocess.call('.\ReadThisForMe\Snip\Snip.exe ' +lang, shell=False)


            if keyboard.is_pressed('q'):
                print('You Quit!')
                break
            

        except:
            break


