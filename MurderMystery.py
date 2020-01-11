import json
import datetime
import tkinter as tk

print("Hello World!")

names = {"Jason", "Selina", "Mariam"}


def convertEpochtoUTC(epoch):
    return datetime.datetime.utcfromtimestamp(epoch).strftime('%Y-%m-%d %H:%M:%S');


r = tk.Tk()

r.title("Martello Murder Mystery")

thisdict = {"brand":"Frod", "model": "Mustang", "year": 1954}

for x in names:
    button = tk.Button(r, text=x, width=50, command=r.destroy )    
    button.pack()
    
def displayData():
    print("Hello");
    
r.mainloop() 
