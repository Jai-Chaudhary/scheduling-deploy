import flask
from util import parse_dt
from state import get_state

app = flask.Flask(__name__)
app.debug = True

@app.route('/get_state', methods=['POST'])
def post_state():
    msg = flask.request.get_json()
    state = get_state(parse_dt(msg['time']))
    return flask.jsonify(state)

app.run(host='0.0.0.0')
