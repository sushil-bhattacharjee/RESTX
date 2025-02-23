from flask import Flask
from flask_restx import Resource, Api, reqparse

app = Flask("devnet")
api = Api(app)

@api.route("/devnet")
class Devnet(Resource):
    def get(self):
        return "Devnet"
    
@api.route("/multiply/<int:a>/<int:b>")
class Multiply(Resource):
    def get(self, a, b):
        return a * b
    
          
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
@api.route("/book")
class Book(Resource):
    def get(self):
        return library_data
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
    
if __name__ == "__main__":
    app.run(host="10.1.10.98", port=4999, debug=True)