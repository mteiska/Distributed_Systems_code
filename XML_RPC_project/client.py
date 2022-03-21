from lib2to3.refactor import get_all_fix_names
import xmlrpc.client
import datetime
import xml.etree.ElementTree as ET

proxy = xmlrpc.client.ServerProxy('http://localhost:9000', verbose=True)
def main_menu():
    print("1)Send a note")
    print("2) Get a note with topic")
    print("0) Exit")
    choice = int(input("Your choice: "))
    return choice

while True:
    try:
        choice = main_menu()
        if choice == 1:
                
            topic = input("Give a Topic for note: ")
            text = input ("Give a Text for note:" )
            timestamp = datetime.datetime.now()
            proxy.send_note(topic,text,timestamp)
        if choice == 2:
            topic = input("Give a Topic for search: ")
            Notes = proxy.search_note(topic)
            if(len(Notes) == 0):
                print("No notes were found with given topic.")
            else:
                print(Notes)
        if choice == 0:
            break

        else:
            print("Choice is invalid. Try again.")

    except KeyboardInterrupt:
        print("Error occured.")
        break