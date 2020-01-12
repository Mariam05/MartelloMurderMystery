import json
import datetime
import tkinter as tk
from tkinter import *
from tkinter import Toplevel
from faulthandler import disable
# from _overlapped import NULL
from http import client

with open('Murder on the 2nd Floor/Murder-on-the-2nd-Floor-Raw-Data.json', 'r') as f:
    murd_dict = json.load(f)

people_dict = dict()
people_arr = []
rooms = {'100': 'Front Lobby',
         '101': 'Reception Closet',
         '105': 'Dining Hall',
         '110': 'Conference Room',
         '130': 'Kitchen',
         '150': 'First Floor Stairwell',
         '151': 'Gym',
         '152': 'Mens Washroom',
         '154': 'Womans Washroom',
         '155': 'Pool',
         '156': 'Laundry Room',
         '156B': 'Stroage Room',
         '200': 'Hall',
         '210': 'Executive Suite (Murder)',
         '220': 'Executive Suite',
         '231': 'Comfort Room 1',
         '232': 'Comfort Room 2',
         '233': 'Comfort Room 3',
         '234': 'Ice and Vending Machines',
         '235': 'Comfort Room 4',
         '236': 'Comfort Room 5',
         '241': 'Junior Suite 1',
         '244': 'Junior Suite 2',
         '247': 'Junior Suite 3',
         '248': 'Junior Suite 4',
         '250': 'Second Floor Stairwell',
         'ap1-1': 'WIFI - Conference Room',
         'ap1-2': 'WIFI - AP1-2',
         'ap1-3': 'WIFI - AP1-3',
         'ap1-4': 'WIFI - AP1-4',
         'ap2-1': 'WIFI - AP2-1 (Murder)',
         'ap2-2': 'WIFI - AP2-2',
         'ap2-3': 'WIFI - AP2-3'}


class Person:

    def __init__(self, name, rooms):
        self.room_dict = rooms
        self.name = name

    def get_room(self, time):
        returned_loc = ''

        if self.room_dict.get(time):
            return get_room_name(self.room_dict[time]['device-id'])

        for curr_time in self.room_dict:
            curr_time = int(curr_time)
            if curr_time <= time:
                room_name = self.room_dict[str(curr_time)]['device-id']
                returned_loc = get_room_name(room_name)
        return returned_loc


# noinspection DuplicatedCode
class Room:

    def __init__(self, number):
        self.people = []
        self.number = number
        self.events = {}
        self.state = {}

    def add_event(self, event_time, action, person):
        self.events[event_time] = person, action

        if action == 'successful keycard unlock':
            self.people.append(person)
            self.state[event_time] = self.people

        if action == 'unlocked no keycard':
            if self.people.__contains__(person):
                self.people.remove(person)
                self.state[event_time] = self.people


    def get_people(self, time):
        return_peo = 'None'

        if self.state.get(time):
            return self.state[time]

        for curr_time in self.state:
            if int(curr_time) <= time:
                return_peo = self.state[curr_time]

        if return_peo.__len__() == 0:
            return_peo = 'Everyone left!'
        return return_peo


class WIFI:

    def __init__(self, number):
        self.number = number
        self.people = {}
        self.prev_people = {}

    def add_person(self, new_person):
        self.people.append(new_person)

    def remove_person(self, existing_person):
        self.prev_people.append(existing_person)
        self.people.remove(existing_person)

    def get_people(self):
        return self.people

    def last_person_to_enter(self):
        return self.people[-1]

    def last_person_to_leave(self):
        return self.prev_people[-1]


for key in murd_dict:
    people_dict[murd_dict[key]['guest-id']] = ''


def convert_epoch_to_utc(epoch):
    return datetime.datetime.utcfromtimestamp(epoch).strftime('%Y-%m-%d %H:%M:%S')


def event_dictionary(name):
    event_dic = {}
    count = 0
    for event_key in murd_dict:
        if murd_dict[event_key]['guest-id'] == name:
            event_dic[event_key] = murd_dict[event_key]
            count += 1
    return event_dic


def get_room_name(room_id):
    if rooms.get(str(room_id)):
        return rooms[room_id]
    return room_id


def get_everyone_loc(time):
    loc = {}
    for person in people_arr:
        loc[person.name] = person.get_room(time)

    return loc


for person in people_dict:  # create dictionaries for ech person, containing their timeline
    people_dict[person] = event_dictionary(person)

for person in people_dict:  # initialize array of Person objects with initial locations
    people_arr.append(Person(person, people_dict[person]))


def setUpGUI():
    r = tk.Tk()
    frame = tk.Frame(r)
    frame.pack()
    r.title("Martello Murder Mystery")

    def displayData(person):
        print(person)
        top = Toplevel();
        top.title(person + "'s events")
        msg = Message(top, text=people_dict[person])
        msg.pack()
        button = Button(top, text="Dismiss", command=top.destroy)
        button.pack()
        print(people_dict[person])
        
    for x in people_dict:
        button = tk.Button(frame, text=x, width=50, command=lambda x=x: displayData(x))    
        button.pack()

    r.mainloop()


"""
Second format where there's a menu bar that the user can use to filter .. 
I still haven't made it so that the data is displayed when one is clicked though. 
"""
def setUpGUI2():
    root = tk.Tk()

    filteredPerson = ""

    filteredPeople = []
    filteredRoom = ""
    
    textBox = tk.Text(root, height=50, width=100)
    textBox.pack()
    
    textBox.config(state="disabled")  # Don't allow the user to edit the textbox
    
    menubar = Menu(root)
    personMenu = Menu(menubar)
    roomMenu = Menu(menubar)

    # Display information about the person selected. TODO: If they click on it again, remove it from filtered
    def personSelected(person):
        if person in filteredPeople:
            filteredPeople.remove(person)
        else:
            filteredPeople.append(person)  # Add the person to the filtered ppl data


        textBox.config(state="normal") # Enable textbox editing so that we can write to it
        textBox.delete(1.0, END) # Clear the textbox

        #This is a dictionary of all the enteries in murd_dict with that person in them
        filteredpeople_dict = [{i:j for (i,j) in murd_dict.items() if (j['guest-id'] in filteredPeople)}]

        # Let the user know what they're filtering by
        textBox.insert(tk.INSERT, "FILTERED BY: \n")
        textBox.insert(tk.INSERT, "PEOPLE: ")
        for p in filteredPeople:
            textBox.insert(tk.INSERT, p + " ")

        textBox.insert(tk.INSERT, "\n\n\n ")
        textBox.insert(tk.INSERT, ("{:<15} {:<25} {:<20}".format('Time','Room','Person')+"\n"))


        for element in filteredpeople_dict:
            for x, y in element.items():
                textBox.insert(tk.INSERT, ("{:<15} {:<25}{:<20}".format(x, rooms[y['device-id']], y['guest-id'])+"\n"))




        textBox.config(state="disabled")  # disable it so that it can't be changed again

    # Create the menu bar for the people so that the user can select which user to filter by
    for person in people_dict:
        personMenu.add_command(label=person, command=lambda person=person: personSelected(person))
    menubar.add_cascade(label="People", menu=personMenu)

    # Create the menu bar for the rooms so that a user can select which room to filter by
    for room in rooms:
        roomMenu.add_command(label=room, command=lambda person=person: personSelected(person))
    menubar.add_cascade(label="Room", menu=roomMenu)

    # display the menu
    root.config(menu=menubar)
        
    root.mainloop()


# print("Murder Dict: " , murd_dict)
# for time, info in murd_dict.items():
#     print (info['guest-id'])
setUpGUI2()

