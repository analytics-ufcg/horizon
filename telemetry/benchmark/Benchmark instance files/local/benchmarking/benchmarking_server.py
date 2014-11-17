import json
import benchmarking_agent
from flask import Flask, make_response, request

app = Flask(__name__)


status = False

@app.route('/get_status')
def get_status():
    return str(status)


@app.route('/start_benchmarking')
def start_benchmarking():
    global status
    resp = 'ha um benchmark em execucao'
    if status:
        status = False
        resp = make_response(json.dumps(benchmarking_agent.start_benchmarking()))
        resp.headers['Access-Control-Allow-Origin'] = '*'
    
    return resp

@app.route('/get_benchmarking')
def get_benchmarking():
    global status
    resp = 'ha um benchmarking em execucao'
    if status:
        resp = make_response(json.dumps(benchmarking_agent.read_benchmarking()))
        resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

@app.route('/change_status')
def change_status():
    global status
    status = True
    return 'ok'

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5151)
