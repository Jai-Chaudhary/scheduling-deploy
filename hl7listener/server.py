import flask
from pymongo import MongoClient
from util import parse_dt
import os

app = flask.Flask(__name__)
app.debug = True

if 'MONGO_PORT_27017_TCP_ADDR' in os.environ:
    client = MongoClient(
        host=os.environ['MONGO_PORT_27017_TCP_ADDR'],
        port=int(os.environ['MONGO_PORT_27017_TCP_PORT']))
else:
    client = MongoClient()

raw_order = client.schedule.raw_order

@app.route('/hl7json', methods=['POST'])
def hl7json():
    msg = flask.request.get_json()
    # NOTE we're only processing for outpatient MRI here
    if msg['Modality'] != 'MRI' or msg['Patient.Class'] != 'O':
        return flask.jsonify({'status': 'ignore'})

    if msg['Service.Description'].find('READ') != -1:
        return flask.jsonify({'status': 'ignore'})

    if msg['Service.Description'].find('ARCHIVE') != -1:
        return flask.jsonify({'status': 'ignore'})

    for x in ['Message.DT', 'Result.Change.DT', 'Scheduled.DT']:
        if msg[x] != None:
            msg[x] = parse_dt(msg[x])
    msg['Observation.Duration'] = int(msg['Observation.Duration'])
    if msg['Machine'] == '': msg['Machine'] = None

    key = {'accession': msg['h.accession.']}

    if raw_order.find_one(key) == None:
        raw_order.insert({
            'accession': msg['h.accession.'],
            'mrn': msg['h.mrn.'],
            'schedule_dt': msg['Message.DT'],
            'appointment_dt': None,
            'arrival_dt': None,
            'begin_dt': None,
            'completed_dt': None,
            'service': None,
            'slot': None,
            'site': None,
            'machine': None,
        })

    raw_order.update_one(
        key,
        {'$set': {
            'appointment_dt': msg['Scheduled.DT'],
            'service': msg['Service.Description'],
            'slot': msg['Observation.Duration'],
            'site': msg['Site'],
            'machine': msg['Machine'],
        }}
    )

    # Patient arrival message
    if msg['ResultStatus'] == 'I' and msg['OrderControlCode'] == 'SC' and msg['Result.Change.DT'] == None:
        raw_order.update_one(
            key,
            {'$set': {
                'arrival_dt': msg['Message.DT']
            }}
        )
    # Study begin message
    elif msg['ResultStatus'] == 'I' and msg['OrderControlCode'] == 'SC' and msg['Result.Change.DT'] != None:
        raw_order.update_one(
            key,
            {'$set': {
                'begin_dt': msg['Result.Change.DT']
            }}
        )
    # Study completion message
    elif msg['ResultStatus'] == 'C' and msg['OrderControlCode'] == 'SC' and msg['Result.Change.DT'] != None:
        raw_order.update_one(
            key,
            {'$set': {
                'completed_dt': msg['Result.Change.DT']
            }}
        )
    # Study cancel message
    elif msg['ResultStatus'] == 'X' and msg['OrderControlCode'] == 'CA':
        raw_order.delete_one(key)
    return flask.jsonify({'status': 'ok'})

app.run(host='0.0.0.0')



