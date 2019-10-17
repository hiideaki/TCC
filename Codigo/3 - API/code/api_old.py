from sanic import Sanic
from sanic.response import json
from sanic_cors import CORS, cross_origin

from model import Model

app = Sanic()
CORS(app, automatic_options=True)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route("/inference", methods=["POST"])
@cross_origin(app, origin='*', headers=['Content-Type'])
async def inference(request):
    print("Received request...")
    data = request.json
    results = Model(data['text']).inference()
    return json({"results": results})

    
@app.route("/test", methods=["GET"])
@cross_origin(app, origin='*', headers=['Content-Type'])
async def test(request):
    return json({"results": "ok"})


if __name__ == "__main__":
    app.run(host="localhost", port=8000)