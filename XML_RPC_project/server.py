from time import time
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
import datetime
import xml.etree.ElementTree as ET
import os
class RequestHandler(SimpleXMLRPCRequestHandler):
   rpc_paths = ('/RPC2',)



with SimpleXMLRPCServer(('localhost', 9000),
                        requestHandler=RequestHandler, allow_none=True) as server:
   
   def send_note(topic,title, text, timestamp):
      #########Creating XML and adding topic if new###########
      try:
         if (os.path.exists("db.xml")) == False:
            root = ET.Element("data")
            tree = ET.ElementTree(root)
            tree.write("db.xml")
         tree = ET.parse('db.xml')
         root = tree.getroot()
         new_topic = root.find("topic[@name='{}']".format(topic))
         if new_topic is None:
            new_topic = ET.SubElement(root,"topic", name=topic)
         noteElement = ET.SubElement(new_topic, "note", name=title)
        
         note1 = ET.SubElement(new_topic, "Text")
         note1.text = text
         timestampElement = ET.SubElement(noteElement, "timestamp")
         timestampElement.text = str(timestamp)
         tree.write("db.xml")
         print("Note is created with topic", topic)

      except Exception as e:
         print("Something went wrong with error:", e)

      

    
            
        
     

      

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

  