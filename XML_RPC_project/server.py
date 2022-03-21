from time import time
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
import datetime
import xml.etree.ElementTree as ET
import os
class RequestHandler(SimpleXMLRPCRequestHandler):
   rpc_paths = ('/RPC2',)
class Note():
    topic = '',
    text = " ",
    timestamp = datetime.datetime

list_of_notes =[]
with SimpleXMLRPCServer(('localhost', 9000),
                        requestHandler=RequestHandler, allow_none=True) as server:
   
   def send_note(topic, text, timestamp):
      note = Note
      note.topic = topic
      note.text = text
      note.timestamp = timestamp
      list_of_notes.append(note)
      #########Creating XML and adding topic if new###########
      if os.path.exists("notes.xml"):
         tree = ET.parse('notes.xml')
         root = tree.getroot()
         for event in root.findall("Topic"):
            new_topic = event.find(topic)
            if new_topic is None:
               userElement = ET.Element("Topic")
               topic1 = ET.SubElement(userElement, topic)
               note1 = ET.SubElement(topic1, "Text")
               note1.text = text
               timestampElement = ET.SubElement(note1, "timestamp")
               timestampElement.text = str(timestamp)
               root.insert(1, topic1)


      else:
         root = ET.Element("Notes")
         topic_header = ET.Element("Topic")
         root.append (topic_header)
         print("Creating the tree structure write your topic and note once more to be added.")
    
            
        
      tree = ET.ElementTree(root)
      with open ("notes.xml", "wb") as files :
         tree.write(files)

      

   # Lets register the note sending function
   server.register_function(send_note)
   def search_note(topic):
      try:
        tree = ET.parse("notes.xml")
        root = tree.getroot()
        notes_to_return = []
        topicElement = root.find(topic)
        if topicElement is None:
            print("No notes found")
            return []
        else:
            for note in topicElement.findall("Text"):
                notes_to_return.append(topic)
                text = note.text
                print("Topic on ", topic)
                print("topicin teksti on", text)
                notes_to_return.append(text)
                timestamp = note.find("timestamp").text
                notes_to_return.append(timestamp)
            print("Found some note for ", topicElement)
            return notes_to_return
      except:
        print("Something went wrong.")
        return False


   # Lets register the note searching function
   server.register_function(search_note)


      
   print("funktiot valmiina käyttöön")
   try:
      print("Exit with Ctrl + c")
      server.serve_forever()
   except KeyboardInterrupt:
      server.server_close()
      print("Closing server.")

  