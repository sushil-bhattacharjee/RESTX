from flask import Flask
from flask_restx import Resource, Api, reqparse
import random

app = Flask("devnet")
api = Api(app)

@api.route("/devnet")
class Devnet(Resource):
    def get(self):
        return "Devnet"
    
        
# Must return the number multiplied by 2
@api.route("/numberbot/double/<int:a>/")
class Multiply(Resource):
    def get(self, a):
        return a * 2

# Must return a random number with the specified range
random_parser = reqparse.RequestParser()
random_parser.add_argument("low", type=int, required=True, location="args")
random_parser.add_argument("high", type=int, required=True, location="args")

@api.route("/numberbot/random")
class Random(Resource):
    @api.expect(random_parser)
    def get(self):
        args = random_parser.parse_args()
        low = args.get("low")
        high = args.get("high")
        if  low > high:
            return {"error": "low must be less than or equal to high"}, 400
        number = random.randint(low, high)
        return {"random_number": number}

calculator_parser = reqparse.RequestParser()
calculator_parser.add_argument("function", choices=("add", "subtract", "divide"))
calculator_parser.add_argument("a", type=int)
calculator_parser.add_argument("b", type=int)

@api.route("/calculator")
class Claculator(Resource):
    @api.expect(calculator_parser)
    def get(self):
        args = calculator_parser.parse_args()
        if args.function == "add":
            result = args.a + args.b 
        elif args["function"] == "subtract":
            result = args["a"] - args["b"]
        elif args['function'] == "divide":
            result = args.a / args['b']
        return result

library_data = {
  "11111": "Overcome your Devnet fever",
  "22222": "Get out of fears to get out of Devnet fever",
  "33333": "Sit on desk keep coding!! OneDay will be Devnet Expert",
  "44444": "Nothing is impossible!!!",
  "55555": "Welcome to James Bond world!!!"
}

remove_book_parser = reqparse.RequestParser()
remove_book_parser.add_argument("isbn", location="json")
add_book_parser = remove_book_parser.copy()
add_book_parser.add_argument("title", location="json")
book_parser = reqparse.RequestParser()
book_parser.add_argument("isbn", type=str, location="args", required=False)

@api.route("/book")
class Book(Resource):
    @api.expect(book_parser)
    def get(self):
        args = book_parser.parse_args()
        isbn = args.get("isbn")
        if isbn:
            if isbn in library_data:
                return {isbn: library_data[isbn]}, 200
            else:
                return {"error": "ISBN not found"}, 404
        return library_data, 200
    @api.expect(add_book_parser)
    def post(self):
        args = add_book_parser.parse_args()
        library_data[args.isbn] = args.title
        return "Successfully added" + args.title , 201
    @api.expect(remove_book_parser)
    def delete(self):
        args = remove_book_parser.parse_args()
        library_data.pop(args.isbn)
        return "" , 204
    
#Creating Flask-Restx-server for Router/Switches inventory
inventory = {"R1": "router", "R2": "router", "NexusSwitch": "switch"}
inv_parser = reqparse.RequestParser()
inv_parser.add_argument("hostname", type=str, location="args")
inv_parser.add_argument("type", type=str, location="args", choices=["switch", "router", "firewall"])
inv_post_parser = inv_parser.copy()
for arg in inv_post_parser.args:
    arg.location = "json"
    arg.required = True
@api.route("/network/inventory")
class Inventory(Resource):
    @api.expect(inv_parser)
    def get(self):
        args = inv_parser.parse_args()
        h, t = args.hostname, args.type 
        results = [
            {"hostname": host, "type": dev_type}
            for host, dev_type in inventory.items()
            if (not h and not t) or (h and h in host) or (t and t in dev_type)
        ]
        return results, 200

    @api.expect(inv_parser)
    def delete(self):
        args = inv_parser.parse_args()
        h, t = args.get("hostname"), args.get("type")
        keys_to_delete = [host for host, dev_type in inventory.items() if (h and h in host) or (t and t in dev_type)]
        if keys_to_delete:
            for key in keys_to_delete:
                inventory.pop(key)
            return "", 204
        return "", 304
    @api.expect(inv_post_parser)
    def post(self):
        args = inv_post_parser.parse_args()
        hostname, dev_type = args["hostname"], args["type"]
        inventory[hostname] = dev_type
        return {"message": f"Added {hostname} as {dev_type}"}, 201

if __name__ == "__main__":
    app.run(host="10.1.10.98", port=4999, debug=True)