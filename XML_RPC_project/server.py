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
         #if xml does not exist create it and root
         if (os.path.exists("db.xml")) == False:
            root = ET.Element("data")
            tree = ET.ElementTree(root)
            tree.write("db.xml")
         tree = ET.parse('db.xml')
         root = tree.getroot()
         #Had to change xml structure since i did not see that it had example structure.
         new_topic = root.find("topic[@name='{}']".format(topic))
         if new_topic is None:
            new_topic = ET.SubElement(root,"topic", name=topic)
         noteElement = ET.SubElement(new_topic, "note", name=title)
        
         note1 = ET.SubElement(noteElement, "Text") #Since Text is under note and not topic we have to do this.
         note1.text = text
         timestampElement = ET.SubElement(noteElement, "timestamp")
         timestampElement.text = str(timestamp)
         tree = ET.ElementTree(root)
         with open ("db.xml", "wb") as files :
            tree.write(files)


         print("Note is created with topic", topic)

      except Exception as e:
         print("Something went wrong with error:", e)

      

    
            
        
     

      

   # Lets register the note sending function
   server.register_function(send_note)
   #Creatig function for searching with topic 
   def search_note(topic):
      try:
        tree = ET.parse("db.xml")
        root = tree.getroot()
        notes_to_return = []
        topicElement = root.find("topic[@name='{}']".format(topic))
        if topicElement == None:
            print("No notes found")
            return [] # client waits for list to be returned this is good principle
        else:
            for topic_note in topicElement.findall("note"): #We want to search under note since Text is there and timestamp
               notes_to_return.append(topic)
               print(topic_note)
               title = topic_note.get("name")
               print("Title is ", title)
               notes_to_return.append(title)
               text = topic_note.find("Text").text
               print(text)
               notes_to_return.append(text)
               print("Topic is ", topic)
               print("topicin teksti on", text)
         
               timestamp = topic_note.find("timestamp").text
               notes_to_return.append(timestamp)
            print("Found some note for ", topic)
            return notes_to_return #return list of all the notes under topic
      except Exception as e:
        print("Error with finding notes with topic",e)
        return None #return none if error and print error message


   # Lets register the note searching function
   server.register_function(search_note)


      
   print("Functions are ready to use.")
   try:
      print("Exit with Ctrl + c or with 0")
      server.serve_forever()
   except KeyboardInterrupt:
      server.server_close()
      print("Closing server.")

  