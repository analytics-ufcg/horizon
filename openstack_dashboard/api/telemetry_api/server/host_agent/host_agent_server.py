import json

from flask import Flask, make_response, request
import host_agent

app = Flask(__name__)

@app.route('/host_data')
def host_data():
    resp = make_response(json.dumps(host_agent.host_data()))
    resp.headers['Access-Control-Allow-Origin'] = "*"

    return resp

if __name__ == '__main__':
    app.debug = True    
    app.run(host='0.0.0.0', port=6556)

