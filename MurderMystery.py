import datetime
import json
import tkinter as tk
from tkinter import *
from tkinter import Toplevel

# from _overlapped import NULL

with open('Murder-on-the-2nd-Floor-Raw-Data.json', 'r') as f:
    murd_dict = json.load(f)

people_dict = dict()
people_arr = []
room_arr = []
wifi_arr = []
murder_room = '210'

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
        self.entered_murd_room = FALSE

    def __str__(self):
        return self.name

    def get_room_dic(self):
        return dict(self.room_dict)

    def get_room(self, time):
        returned_loc = ''

        if self.room_dict.get(time):
            return get_room_name(self.room_dict[time]['device-id'])

        for person_curr_time in self.room_dict:
            person_curr_time = int(person_curr_time)
            if person_curr_time <= time:
                room_name = self.room_dict[str(person_curr_time)]['device-id']
                returned_loc = get_room_name(room_name)
        return returned_loc


# noinspection DuplicatedCode
class Room:

    def __init__(self, number):
        self.people = []
        self.number = number
        self.events = {}
        self.state = {}

    def add_event(self, event_time, action, room_person):
        self.events[event_time] = room_person, action

        if action == 'successful keycard unlock':
            if self.people.__contains__(room_person) == FALSE:
                self.people.append(room_person)
                peeps = self.people
                self.state[event_time] = str(peeps)

        if action == 'unlocked no keycard':
            if self.people.__contains__(room_person):
                self.people.remove(room_person)
                peeps = self.people
                self.state[event_time] = str(peeps)

    def get_people(self, time):
        return_peo = 'None'

        if self.state.get(time):
            return self.state[time]

        for state_curr_time in self.state:
            if int(state_curr_time) <= int(time):
                return_peo = self.state[state_curr_time]

        if return_peo.__len__() == 0:
            return_peo = 'Everyone left!'
        return return_peo

    def time_interval(self, start_time, end_time):
        interval_dict = {}
        return_interval_peo = 'No one enters or exits'
        for i in range(int(start_time), int(end_time)):
            if self.events.keys().__contains__(str(i)):
                interval_dict[i] = self.events[str(i)]

        if interval_dict.__len__() == 0:
            interval_dict[0] = return_interval_peo
        return interval_dict


class WIFI:
    def __init__(self, number):
        self.number = number
        self.people = []
        self.events = {}
        self.state = {}

    def add_event(self, event_time, action, room_person):
        self.events[event_time] = room_person, action

        if action == 'user connected' or action == 'new client':
            if self.people.__contains__(room_person) == FALSE:
                self.people.append(room_person)
                peeps = self.people
                self.state[event_time] = str(peeps)
        else:
            if action == 'user disconnected':
                if self.people.__contains__(room_person):
                    self.people.remove(room_person)
                    peeps = self.people
                    self.state[event_time] = str(peeps)

    def get_people(self, time):
        return_peo = 'None'

        if self.state.get(time):
            return self.state[time]

        for state_curr_time in self.state:
            if int(state_curr_time) <= time:
                return_peo = self.state[state_curr_time]

        if return_peo.__len__() == 0:
            return_peo = 'Everyone disconnected!'
        return return_peo

    def time_interval(self, start_time, end_time):
        interval_dict = {}
        return_interval_peo = 'No one connects or disconnects'
        for i in range(int(start_time), int(end_time)):
            if self.events.keys().__contains__(str(i)):
                interval_dict[i] = str(self.get_people(str(i))), self.events[str(i)]
        if interval_dict.__len__() == 0:
            interval_dict[0] = return_interval_peo
        return interval_dict


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
    for person_loc in people_arr:
        loc[person_loc.name] = person_loc.get_room(time)

    return loc


def check_time_interval(device_id, start_time, end_time):
    interval_dict = {}
    interval_dict.clear()
    for wifi in wifi_arr:
        if wifi.number == device_id:
            interval_dict.update(wifi.time_interval(start_time, end_time))
    for room in room_arr:
        if room.number == device_id:
            interval_dict.update(room.time_interval(start_time, end_time))
    for _ in sorted(interval_dict):
        pass
    return interval_dict


for person in people_dict:  # create dictionaries for ech person, containing their timeline
    people_dict[person] = event_dictionary(person)

for person in people_dict:  # initialize array of Person objects with initial locations
    people_arr.append(Person(person, people_dict[person]))

for room in rooms:
    if room[0] == '1' or room[0] == '2':
        room_arr.append(Room(room))
    if room[0:2] == 'ap':
        wifi_arr.append(WIFI(room))

for curr_time in murd_dict:
    for room in room_arr:
        if murd_dict[curr_time]['device-id'] == room.number:
            room.add_event(curr_time, murd_dict[curr_time]['event'], murd_dict[curr_time]['guest-id'])
    for wifi in wifi_arr:
        if murd_dict[curr_time]['device-id'] == wifi.number:
            wifi.add_event(curr_time, murd_dict[curr_time]['event'], murd_dict[curr_time]['guest-id'])


def who_is_dead():
    enters_murder_room = FALSE
    pos_victim = []
    for person in people_arr:
        last_event = max(person.get_room_dic().keys())
        if person.get_room_dic()[last_event]['event'] == 'successful keycard unlock' or person.get_room_dic()[last_event]['event'] == 'unlocked no keycard':
            pos_victim.append(person.name)
    return pos_victim


def who_did_it(pos_victim):
    pos_sus = []
    for person in people_arr:
        if person.name == 'n/a':
            break
        if pos_victim.__contains__(person.name):  # find time interval for the murder
            for time in person.room_dict:
                if person.room_dict[time]['event'] == 'successful keycard unlock' and person.room_dict[time]['device-id'] == murder_room:
                    start_time = time
            end_time = max(person.get_room_dic().keys())
        else:
            for time in person.room_dict:  # find everyone who entered the murder room
                if person.room_dict[time]['device-id'] == murder_room:
                    person.entered_murd_room = TRUE

            if person.entered_murd_room:
                pos_sus.append(person)
    for suspect in pos_sus:
        for time in suspect.room_dict:
            if time < end_time:
                device = suspect.room_dict[time]['device-id']
                if device != murder_room:
                    pos_removal = TRUE
                else:
                    pos_removal = FALSE

    return pos_sus


check_time_interval('210', 1578180000, 1578399300)
print(who_is_dead())
for sus in who_did_it(who_is_dead()):
    print(str(sus), end=' ')
# print(interval_dict)

"""""""""""
""""GUI""""
"""""""""""


def setUpGUI():
    r = tk.Tk()
    frame = tk.Frame(r)
    r.title("Martello Murder Mystery")
    frame.pack()

    def displayData(person):
        print(person)
        top = Toplevel()
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

        textBox.config(state="normal")  # Enable textbox editing so that we can write to it
        textBox.delete(1.0, END)  # Clear the textbox

        # This is a dictionary of all the enteries in murd_dict with that person in them
        filteredpeople_dict = [{i: j for (i, j) in murd_dict.items() if (j['guest-id'] in filteredPeople)}]

        # Let the user know what they're filtering by
        textBox.insert(tk.INSERT, "FILTERED BY: \n")
        textBox.insert(tk.INSERT, "PEOPLE: ")
        for p in filteredPeople:
            textBox.insert(tk.INSERT, p + " ")

        textBox.insert(tk.INSERT, "\n\n\n ")
        textBox.insert(tk.INSERT, ("{:<22} {:<12} {:<28} {:<20}".format('Time', 'Person', 'Event', 'Room') + "\n"))

        for element in filteredpeople_dict:
            for x, y in element.items():
                textBox.insert(tk.INSERT,
                               ("{:<22} {:<12}{:<28} {:<28}".format(convert_epoch_to_utc(int(x)), y['guest-id'],
                                                                    y['event'], rooms[y['device-id']]) + "\n"))

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
