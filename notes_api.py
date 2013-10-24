import webapp2
import json
import logging

from google.appengine.api import search

from utils import generate_return_message_to_kinvey

class NotesHandler(webapp2.RequestHandler):

  #Kinvey requests come via POST.
  def post(self):
    #Getting data from Kinvey
    body = json.loads(self.request.body)
    request = body["arguments"]["request"]
    response = body["arguments"]["response"]    

    logging.info("Running request from Kinvey.")

    #Here I added my code, to process what I needed
    #In my case, I was creating documents for the search engine when adding
    #or editing any entity on Kinvey datastore
    if request["method"] == "POST" or request["method"] == "PUT":
      #Creating the document for the search
      request_body = request["body"]

      #To have the entityId, my business logic runs after each action on Kinvey
      fields = [search.AtomField(name="id", value=request["entityId"]),
                search.TextField(name="name", value=request_body["name"]),
                search.TextField(name="surname", value=request_body["surname"]),
                search.TextField(name="text", value=request_body["text"])]

      document = search.Document(doc_id=request["entityId"],
                                 fields=fields)

      search.Index(namespace="kinvey", name="notes").put(document)

    elif request["method"] == "DELETE":
      #Delete document
      doc_index = search.Index(namespace="kinvey", name="person")
      #Use entity id to delete document
      doc_index.delete([request["entityId"]])

    #Creating the response to Kinvey

    string_to_send_to_kinvey = json.dumps(generate_return_message_to_kinvey(request, response))

    self.response.headers = {
                            'Content-Type': "application/json",
                            }
    self.response.status = 201
    self.response.body = string_to_send_to_kinvey
    self.response.complete = True

    return