from flask import Flask
from flask_restx import Resource, Api, reqparse
import random

app = Flask("devnet")
api = Api(app)
  
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

#Pizza sales order
sales_history = {
    "margherita": 0,
    "pepperoni": 0,
    "hawaii": 0
}

pizza_parser = reqparse.RequestParser()
pizza_parser.add_argument("variant", type=str, required=True, choices=("margherita", "pepperoni", "hawaii"), location="json")
pizza_parser.add_argument("quantity", type=int, required=True, location="json")

@api.route("/pizzeria/salessummary")
class SalesSummary(Resource):
    def get(self):
        """
        Returns a summary of all pizza sales so far.
        """
        return sales_history

@api.route("/pizzeria/order")
class PizzaOrder(Resource):
    @api.expect(pizza_parser)
    def post(self):
        """
        Places a pizza order.
        Expects JSON: {"variant": "margherita", "quantity": 2}
        """
        args = pizza_parser.parse_args()
        variant = args["variant"]
        quantity = args["quantity"]
        sales_history[variant] += quantity
        return {"message": f"Ordered {quantity} {variant} pizza(s)."}, 201

if __name__ == "__main__":
    app.run(host="10.1.10.98", port=4999, debug=True)