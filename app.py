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


db.create_all()
library_args = reqparse.RequestParser()
library_args.add_argument("name", type=str, help="name of the book", required=True)
library_args.add_argument("author", type=str, help="name of the author", required=True)
library_args.add_argument("stocks", type=int, help="number of stock of book", required=True)
library_args.add_argument("price", type=int, help="price of the book", required=True)

resource_fields = {
    'name': fields.String,
    'author': fields.String,
    'stocks': fields.Integer,
    'price': fields.Integer
}


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

    @marshal_with(resource_fields)
    def get(self, name):
        search = LibraryModel.query.filter_by(name=name).first()
        if not search:
            abort(404, message="name of book not found")
        return result

api.add_resource(Library, "/library/<string:name>")
if __name__ == '__main__':
    app.run(debug=True)
