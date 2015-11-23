import requests
import json
from schedule import get_schedule
from dist import get_duration_distribution, get_lateness_distribution
from util import get_mins, parse_dt, config_coll

lateness_offset = 23        # TODO magic number

def get_patients(schedule, time):
    ret = []
    for x in schedule:
        p = {
            'name': x['mrn'],
            'clazz': '{}_{}'.format(x['service'], x['slot']),
            'appointment': get_mins(x['appointment_dt']),
            'slot': x['slot'],
            'durationDistribution': get_duration_distribution(x['service'], x['slot']),
            'latenessDistribution': get_lateness_distribution(),
            'volunteer': False,
            'seed': hash(x['mrn']) % (2**30),

            'site': x['site'],
            'machine': None if x['begin_dt'] == 'None' else x['machine'],
            'optimized': False,

            'stat': {
                'schedule': 0,
                'arrival': get_mins(x['arrival_dt']),
                'begin': get_mins(x['begin_dt']),
                'completion': get_mins(x['completed_dt']),
                'originalSite': x['site']
            }
        }

        stat = p['stat']
        if stat['begin'] != None:
            stat['arrival'] = min(stat['arrival'] + lateness_offset, stat['begin'])
        elif stat['arrival'] != None:
            stat['arrival'] += lateness_offset
            if stat['arrival'] > get_mins(time):
                stat['arrival'] = None

        ret.append(p)
    return ret

def get_state(time):
	return {
		'time': get_mins(time),
		'patients': get_patients(get_schedule(time), time),
		'sites': config_coll.find_one({'name': 'site'})['data'],
		'optimizer': {
			"active": False,
			"advanceTime": 60,
			"objective": {
				"waitNorm": "l1",
				"overTimeWeight": 10
			},
			"confidenceLevel": 0.7,
			"patientConfidenceLevel": 0.7,
			"numSamples": 100
		}
	}

if __name__ == '__main__':
    time = parse_dt('2014-09-27 8:30:15')
    state = get_state(time)
    r = requests.post('http://localhost:4567/evaluate', json=state)
    print(r.text)
