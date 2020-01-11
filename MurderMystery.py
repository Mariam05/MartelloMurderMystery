import json
import datetime

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
            event_dic[event_key] = murd_dict[event_key]
            count += 1
    return event_dic


for person in people:
    print(person + ":")
    people[person] = event_dictionary(person)
    print(people[person])
    print("\n")
