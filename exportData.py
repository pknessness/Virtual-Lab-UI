from tkinter import Tk     # from tkinter import Tk for Python 3.x
from tkinter.filedialog import askopenfilename,askdirectory
import lib.shutil as shutil
import os

def export(material):
    Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
    dir = askdirectory() # show an "Open" dialog box and return the path to the selected file
    print(dir)
    src = os.path.abspath(__file__)

    shutil.copy2('raw_data\\'+material+'.xlsx', dir)