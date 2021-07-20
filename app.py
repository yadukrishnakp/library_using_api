from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)


class LibraryModel(db.Model):
    name = db.Column(db.String(50), primary_key=True, nullable=False)
    author = db.Column(db.String(50), nullable=False)
    stocks = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Library(name = {name}, author ={author},stocks={stocks},price={price})"


library_args = reqparse.RequestParser()
library_args.add_argument("name", type=str, help="name of the book", required=True)
library_args.add_argument("author", type=str, help="name of the author", required=True)
library_args.add_argument("stocks", type=int, help="number of stock of book", required=True)
library_args.add_argument("price", type=int, help="price of the book", required=True)

library_update_args = reqparse.RequestParser()
library_update_args.add_argument("name", type=str, help="name of the book")
library_update_args.add_argument("author", type=str, help="name of the author")
library_update_args.add_argument("stocks", type=int, help="number of stock of book")
library_update_args.add_argument("price", type=int, help="price of the book")

resource_fields = {
    'name': fields.String,
    'author': fields.String,
    'stocks': fields.Integer,
    'price': fields.Integer
}


# add new book details
class Library(Resource):
    @marshal_with(resource_fields)
    def put(self, name):
        args = library_args.parse_args()
        search = LibraryModel.query.filter_by(name=name).first()
        if search:
            abort(409, message="name of book already exist")
        result = LibraryModel(name=args["name"], author=args["author"], stocks=args['stocks'], price=args['price'])
        db.session.add(result)
        db.session.commit()
        return result, 201

# selecting one book for seeing
    @marshal_with(resource_fields)
    def get(self, name):
        search = LibraryModel.query.filter_by(name=name).first()
        if not search:
            abort(404, message="name of book not found")
        return result

# delete books
    def delete(self, name):
        search = LibraryModel.query.filter_by(name=name).first()
        if not search:
            abort(404, message="name of book not found")
        else:
            LibraryModel.query.filter_by(name=name).delete()
            db.session.commit()
        return '', 204

# update details of books
    @marshal_with(resource_fields)
    def patch(self, name):
        search = LibraryModel.query.filter_by(name=name).first()
        if not search:
            abort(404, message="name of book not found")
        args = library_update_args.parse_args()
        search = LibraryModel.query.filter_by(name=name).first()
        if args["name"]:
            search.name = args["name"]
        if args["author"]:
            search.author = args["author"]
        if args["stocks"]:
            search.stocks = args["stocks"]
        if args["price"]:
            search.price = args["price"]
        db.session.commit()
        return search, 200


api.add_resource(Library, "/library/<string:name>")
if __name__ == '__main__':
    app.run(debug=True)
