import json
import datetime

with open('Murder on the 2nd Floor/Murder-on-the-2nd-Floor-Raw-Data.json', 'r') as f:
    murd_dict = json.load(f)

people_dict = dict()
people_arr = []
rooms = {'100': 'Front Lobby',
         '101': 'Reception Closet',
         '105': 'Dining Hall',
         '110': 'Conference Room',
         '130': 'Kitchen',
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
         '248': 'Junior Suite 4'}


class Person:
    def __init__(self, name, room):
        self.current_room = room
        self.prev_room = []
        self.name = name

    def update_room(self, room):
        self.prev_room.append(self.current_room)
        self.current_room = room

    def get_last_room(self):
        return self.prev_room[-1]


# noinspection DuplicatedCode
class Room:
    def __init__(self, number):
        self.people = []
        self.prev_people = []
        self.number = number

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


class Floor:
    def __init__(self, number):
        self.number = number
        self.people = []
        self.prev_people = []

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
            event_dic[convert_epoch_to_utc(int(event_key))] = murd_dict[event_key]
            count += 1
    return event_dic


def get_room_name(room_id):
    if rooms.get(str(room_id)):
        return rooms[room_id]
    return room_id


for person in people_dict:
    people_dict[person] = event_dictionary(person)

for person in people_dict:
    people_arr.append(Person(person, get_room_name(people_dict[person][list(people_dict[person])[0]]['device-id'])))

