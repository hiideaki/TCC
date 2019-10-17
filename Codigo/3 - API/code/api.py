
from flask import Flask
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS


from model import Model


app = Flask(__name__)
CORS(app)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('text')

class Inference(Resource):

    def post(self):
        args = parser.parse_args()

        print(args['text'])
        results = Model(args['text']).inference()

        return {'results': results}, 200

    def get(self):

        return {'confirmation': 'Get request working properly'}, 200

    
api.add_resource(Inference, '/classification')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)