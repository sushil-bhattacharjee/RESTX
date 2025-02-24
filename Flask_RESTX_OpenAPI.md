# Chapter 2: Flask-RESTX and OpenAPI

## Task 2.1: GET requests with parameters and Swagger UI

**Objective**: Create a REST API that includes the following endpoints:

- **GET /numberbot/double/{number}**  
  Must return the number multiplied by 2

- **GET /numberbot/random?low={number_a}&high={number_b}**  
  Must return a random number within the specified range

Try that Flask-RESTX generates the corresponding Swagger documentation at http://localhost:5000 and that you are able to try out the requests including the possibility to specify all the number-variables through the Swagger GUI.

**Hints**:
- Flask-RESTX documentation: [https://flask-restx.readthedocs.io/en/0.5.1/](https://flask-restx.readthedocs.io/en/0.5.1/)
- Docs → Quick Start → Resourceful Routing
- Docs → Request Parsing → The `@api.expect()` decorator
- `random.randint(a, b)`

---

## Task 2.2: POST requests with argument parsing and JSON response

**Objective**: Add HTTP methods and store state data between API calls.

Create a REST API server for a pizza ordering application, using Flask-RESTX to provide the following endpoints:

- **POST /pizzeria/order**  
  Request parameters:
  - `variant` may only be one of the following: **margherita**, **pepperoni**, or **hawaii**  
    The Swagger documentation must present them as a dropdown menu.  
  - `quantity` must be an integer  
    The Swagger documentation must indicate that you input an integer.

  You can store the sales results in a `sales_history` variable that you initialize in your Python script.

- **GET /pizzeria/salessummary**  
  Should return a JSON dictionary that summarizes how many of each pizza variant have been sold in total so far, for example:
  ```json
  {
    "margherita": 10,
    "pepperoni": 7,
    "hawaii": 5
  }
Try that Flask-RESTX generates the corresponding Swagger documentation at http://localhost:5000 and that you are able to try out the requests including the possibility to specify the JSON payload for the POST method.

Task 2.3: Re-using parsers and running on custom port
Objective: Utilize parser inheritance and other common features.

Create a REST API server for storing the inventory of a network.
Define the baseline inventory like this in your Python script:
inventory = {
  "R1": "router",
  "R2": "router",
  "NexusSwitch": "switch"
}
Use Flask-RESTX to provide the following API endpoints. In all cases, the type parameter may only be one of the following: switch, router, or firewall.

GET /network/inventory?hostname={searchstring}&type={type}
Expected result: Return a JSON list of inventory entries where the hostname or type matches the search string. The search string should be treated like a wildcard so "itc" matches "switch" in a search.
If no hostname or type is provided, return the entire inventory. It is up to you to choose the format of the stored and returned inventory.
Use HTTP status code 200 in the response.

DELETE /network/inventory?hostname={hostname}&type={type}
Reuse the RequestParser from the GET endpoint with Flask-RESTX parser inheritance.
Expected result: Delete the device with a matching hostname, or all devices of the indicated type.
Use HTTP status code 204 in the response if something was deleted. Use HTTP status code 304 if no devices were deleted.

POST /network/inventory
The API should receive request parameters through the HTTP POST body as JSON with the following format:
{
  "type": "switch",
  "hostname": "SW-01"
}
Reuse the RequestParser from the GET endpoint with Flask-RESTX parser inheritance. Replace arguments if needed.
Expected result: Add the network device to the inventory and use HTTP status code 201 in the response.

Make sure the API is exposed on TCP port 4109 and not the default port 5000.
Ensure that Flask-RESTX generates the corresponding Swagger docs at http://localhost:4109/doc.

Hints
Flask-RESTX documentation: https://flask-restx.readthedocs.io/en/0.5.1/
Docs → Quick Start → Endpoints
Docs → Request Parsing → Parser Inheritance
my_parser.replace_argument(..., location=...)
…run(port=...)
api = Api(app, doc='/doc')