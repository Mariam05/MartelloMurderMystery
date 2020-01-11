import json
import datetime

def convertEpochtoUTC(epoch):
    return datetime.datetime.utcfromtimestamp(epoch).strftime('%Y-%m-%d %H:%M:%S');

import json

with open('Murder on the 2nd Floor/Murder-on-the-2nd-Floor-Raw-Data.json', 'r') as f:
    murd_dict = json.load(f)

people = {}

def event_dictionary(name):
    event_dic = {}
    count = 0
    for key in murd_dict:
        if murd_dict[key]['guest-id'] == name:
            event_dic[key] = murd_dict[key]
            count += 1
    return event_dic

for key in murd_dict:
    people[murd_dict[key]['guest-id']] = ''

for person in people:
    print(person + ":")
    print(event_dictionary(person))
    print("\n")
