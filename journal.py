#!/usr/bin/env python3
# make a shabang line
# what this does is uses the env program to find whatever executable we're about to tell it; in workspaces we have to specify python3 otherwise it will run it with Python2

from collections import OrderedDict
import datetime
import os
import sys

from peewee import *

db = SqliteDatabase('journal.db')


class Entry(Model):
    # content
    content = TextField()
    # timestamp
    timestamp = DateTimeField(default=datetime.datetime.now)
    # notice there are no parentheses on the end of this, whenever it goes to create the default, it sees that it's a function and it will call it, and that way we get the date time now, whenever the entry is created.
    # we wouldn't get that if we put the parenthesis on there, it would make it to whatever the time was when we ran the script, obviously we don't want it to be one date time for all of our entries.


    class Meta:
        database = db


# function that will start it all
def initialize():
    '''Create the database and the table if they do not exist.'''
    db.connect()
    db.create_tables([Entry], safe=True)


def clear():
    # for clearing the screen between each entry
    # os.system lets you call a program from os that allows the code below to be executed
    # interpret the bellow line of code as: 'call program 'cls' if using windows os otherwise call program 'clear' if using linux, mac etc...
    os.system('cls' if os.name == 'nt' else 'clear')


def menu_loop():
    '''Show the menu'''
    # setting choice variable to None, initializing a variable without giving it a value
    choice = None

    while choice != 'q':
        clear()
        print('Enter "q" to quit.')
        # so long as they haven't chosen q as their choice, we're going to print out a message saying that hey you can put in 'q' in order to quit.

        for key, value in menu.items():
            print('{}) {}'.format(key, value.__doc__))
            # .__doc__ - a magic variable that holds the docstring of a function, method, or class
        # we're looping through each of the items in our dictionary, the key and the value (where the value will be one of the functions: add_entry or view_enteries and the dunder doc is the doc string for given function) and we're gonna print out the key and the value.

        # Then make a choice
        choice = input('Action: ').lower().strip()
        # if the choice is 'q' then quit, if it's 'a' then fun add_entry function and if it's 'v' then view_enteris function will run
        if choice in menu:
            clear()
            menu[choice]()


def add_entry():
    '''Add your thoughts..'''
    print('Enter your entry. Press ctrl+d when finished.')
    data = sys.stdin.read().strip()
    # sys.stdin is for capturing everything that was writen, stdin essentially is the keyboard -- so capture all from keyboard then rean then strip of all white spaces

    if data:
        if input('Do you want to save this entry? [Yn] ').lower() != 'n':
            Entry.create(content=data)
            print('Your journal entry was successfully saved!')


def view_entries(search_query=None):
    '''View your previous thoughts..'''
    entries = Entry.select().order_by(Entry.timestamp.desc())
    if search_query:
        entries = entries.where(Entry.content.contains(search_query))

    for entry in entries:
        timestamp = entry.timestamp.strftime('%A %B %d, %Y %I:%M%p')
        # %A = weekday name; %B = month name; %d = number of the month; %Y = year; %I = hour; %M = minutes; %p = either AM or PM
        clear()
        print(timestamp)
        print('=' * len(timestamp)) # printing an equal sign for however many characters are in the timestamp
        print(entry.content)
        print('\n\n' + '=' * len(timestamp)) # between each entry print two new lines and '=' for however many char were in timestamp for better UI
        print('n) next entry')
        print('d) delete entry')
        print('q) return to main menu')

        next_action = input('Action: [Ndq] ').lower().strip()
        if next_action == 'q':
            break
        elif next_action == 'd':
            delete_entry(entry)


def search_entries():
    '''Search entries for a string.'''
    view_entries(input('Search query: '))


def delete_entry(entry):
    '''Delete a thought.'''
    if input('Are you sure you want to delete this journal entry? [yN] ').lower() == 'y':
        entry.delete_instance()
        print('*******Your entry was deleted!*******') # this line of code is not visible anymore becasue of the clear() function


menu = OrderedDict([
    ('a', add_entry),
    ('v', view_entries),
    ('s', search_entries),
])


if __name__ == '__main__':
    initialize() # this allows to know if the database exists before getting around and running the application
    menu_loop()
