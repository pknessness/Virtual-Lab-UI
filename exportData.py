from tkinter import Tk     # from tkinter import Tk for Python 3.x
from tkinter.filedialog import askopenfilename,askdirectory
import shutil
import os
import openpyxl
import random

randomization = 0.0001

def export(material, test):
    workbook = openpyxl.load_workbook('raw_data\\'+ test +'\\'+ material +'.xlsx')
    for i in workbook:
        for j in i:
            for k in j:
                if(type(k.value) == float):
                    k.value += random.randint(-1,1) * randomization
                    
    Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
    dir = askdirectory() # show an "Open" dialog box and return the path to the selected file
    print(dir)
    src = os.path.abspath(__file__)

    # shutil.copy2('raw_data\\'+material+'.xlsx', dir)
    # shutil.copy2('raw_data\\'+material+'.xlsx', dir)
    workbook.close()
    workbook.save(dir+'/' + material + test +'.xlsx')