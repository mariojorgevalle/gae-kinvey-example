def create_kinvey_request_message(request):
  incoming_request = {
      "method": request["method"],
      "username": request["username"],
      "entityId": request["entityId"],
      "collectionName": request["collectionName"],
      "headers": {
          "connection": request["headers"]["connection"],
          "host": request["headers"]["host"],
          'x-forwarded-for': request["headers"]["x-forwarded-for"],
          'x-forwarded-port': request["headers"]["x-forwarded-port"],
          'x-kinvey-api-version': request["headers"]["x-kinvey-api-version"],
          'x-real-ip': request["headers"]["x-real-ip"],
          "authorization": request["headers"]["authorization"],
          'x-forwarded-proto': request["headers"]["x-forwarded-proto"],
      },
      "body": request["body"],
      "params": request["params"]
  }
  return incoming_request

def create_kinvey_response_message(response):
  outgoing_response = {
      "complete": True,
      "headers": {
          'x-powered-by': response["headers"]["x-powered-by"],
          'x-kinvey-api-version': response["headers"]["x-kinvey-api-version"],
          'x-kinvey-request-id': response["headers"]["x-kinvey-request-id"]
      },
      "body": response["body"],
      "error": None,
      "statusCode": 201
  }
  return outgoing_response

def generate_return_message_to_kinvey(request, response):
  incoming_request = create_kinvey_request_message(request)
  outgoing_response = create_kinvey_response_message(response)

  return {"request": incoming_request, "response": outgoing_response}