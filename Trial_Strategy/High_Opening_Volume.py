import pandas as pd
import numpy as np
from pandas import ExcelWriter
from smartapi import SmartConnect
from tkinter import *
from tkinter.filedialog import askopenfilename

obj = SmartConnect(api_key='8q3pqVJY')
data = obj.generateSession('A545511','Kite@666')

root = Tk()
filePath = askopenfilename()
root.withdraw()

nifty_500_list = pd.read_excel(filePath)

print(nifty_500_list)
