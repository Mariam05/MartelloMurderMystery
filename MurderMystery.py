import json
import datetime
import tkinter as tk
from tkinter import *
from tkinter import Toplevel
from faulthandler import disable
from _overlapped import NULL

with open('Murder on the 2nd Floor/Murder-on-the-2nd-Floor-Raw-Data.json', 'r') as f:
    murd_dict = json.load(f)

people = {}

for key in murd_dict:
    people[murd_dict[key]['guest-id']] = ''


def convert_epoch_to_utc(epoch):
    return datetime.datetime.utcfromtimestamp(epoch).strftime('%Y-%m-%d %H:%M:%S')


def event_dictionary(name):
    event_dic = {}
    count = 0
    for event_key in murd_dict:
        if murd_dict[event_key]['guest-id'] == name:
            event_dic[convert_epoch_to_utc(int(event_key))] = murd_dict[event_key]
            count += 1
    return event_dic


for person in people:
    people[person] = event_dictionary(person)
    
"""
First format where each person is a button
"""


def setUpGUI():
    r = tk.Tk()
    frame = tk.Frame(r)
    frame.pack()
    r.title("Martello Murder Mystery")
   
    def displayData(person):
        print(person)
        top = Toplevel();
        top.title(person + "'s events")
        msg = Message(top, text=people[person])
        msg.pack()
        button = Button(top, text="Dismiss", command=top.destroy)
        button.pack()
        print(people[person]);
        
    for x in people:
        button = tk.Button(frame, text=x, width=50, command=lambda x=x: displayData(x))    
        button.pack()
            
    r.mainloop()


"""
Second format where there's a menu bar that the user can use to filter 
"""
def setUpGUI2():
    root = tk.Tk()
    
    filteredPerson = ""
    filteredRoom = ""
    
    textBox = tk.Text(root, height=50, width=100)
    textBox.pack()
    
    textBox.config(state="disabled")
    
    menubar = Menu(root)
    personMenu = Menu(menubar)
    
    def personSelected(person):
        filteredPerson = person
        textBox.config(state="normal")
        textBox.delete(1.0, END)
        textBox.insert(tk.INSERT, "FILTERED BY: " + filteredPerson + "\n")
        textBox.insert(tk.INSERT, person + "\n")  
        textBox.config(state="disabled")
        
    for person in people:
        personMenu.add_command(label=person, command=lambda person=person: personSelected(person))
        
    menubar.add_cascade(label="People", menu=personMenu)
    
    # display the menu
    root.config(menu=menubar)
        
    root.mainloop()
    
    
setUpGUI2();
