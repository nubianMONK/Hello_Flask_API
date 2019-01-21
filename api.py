import sys
import os
from flask import Flask
from flask_restful import reqparse, Resource, fields, marshal, \
    marshal_with, Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import MetaData

# setup database models
convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)
basedir = os.path.abspath(os.path.dirname(__file__))
DATABASE = 'greetings.db'
DATABASE_PATH = os.path.join(basedir, DATABASE)

# setup Flask
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///' + DATABASE_PATH
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(metadata=metadata)
migrate = Migrate()
api = Api()


# model
class Greeting(db.Model):

    __tablename__ = "greetings"

    id = db.Column(db.Integer, primary_key=True)
    language = db.Column(db.String(64), index=True, unique=True)
    message = db.Column(db.Text)


# Api Resource Fields
# Used to serialize returned data
greeting_fields = {
    'id': fields.Integer,
    'language': fields.String,
    'message': fields.String,
    'self_uri': fields.Url('greeting', absolute=False)

}


# Greeting resource api
class GreetingAPI(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('language', type=str, required=True,
                                   help='Language cannot be empty',
                                   location='json')
        self.reqparse.add_argument('message', type=str, required=True,
                                   help='Message cannot be empty',
                                   location='json')
        super().__init__()

    # HTTP methods/verbs
    def get(self, language):
        greeting = db.session.query(Greeting).filter_by(language=language.lower()) \
            .first()
        return {'greeting': marshal(greeting, greeting_fields)}

    def delete(self, language):
        db.session.query(Greeting).filter_by(language=language.lower()) \
            .delete()
        db.session.commit()
        return {'result': True}

    @marshal_with(greeting_fields)
    def put(self, language):

        args = self.reqparse.parse_args()
        updated_language = str(args['language'])
        updated_message = str(args['message'])
        greeting = {'language': updated_language,
                    'message': updated_message
                    }
        keys = []
        for k, v in greeting.items():
            if v is None:
                keys.append(k)

        for key in keys:
            del greeting[key]

        db.session.query(Greeting).filter_by(language=language.lower()) \
            .update(greeting)
        db.session.commit()
        updated_greeting = db.session.query(Greeting).filter_by(language=language.lower()) \
            .first()
        return {'id': updated_greeting.id,
                'language': updated_greeting.language,
                'message': updated_greeting.message
                }


# Greeting Collection Api
class GreetingListAPI(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('language', type=str, required=True,
                                   help='Language cannot be empty',
                                   location='json')
        self.reqparse.add_argument('message', type=str, required=True,
                                   help='Message cannot be empty',
                                   location='json')
        super().__init__()

# HTTP methods/verbs
    def get(self):
        greetings = db.session.query(Greeting).all()
        return {'greetings': [marshal(greeting, greeting_fields)
                              for greeting in greetings]}

    def post(self):
        args = self.reqparse.parse_args()
        greeting = Greeting(language=str.lower(args['language']),
                            message=args['message'])

        db.session.add(greeting)
        db.session.commit()
        return {'greeting': marshal(greeting, greeting_fields)}


# Add APi endpoint resources
api.add_resource(GreetingAPI, '/api/v1/greetings/<string:language>',
                 endpoint='greeting')
api.add_resource(GreetingListAPI, '/api/v1/greetings', endpoint='greetings')


# hook up extensions to app
db.init_app(app)
migrate.init_app(app, db)
api.init_app(app)


if __name__ == "__main__":
    if "--setup" in sys.argv:
        with app.app_context():
            db.drop_all()
            db.create_all()
            db.session.commit()
            print("Database tables created")
    else:
        app.run(host='0.0.0.0', port=8000, debug=True)
