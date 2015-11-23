import json
from datetime import datetime, timedelta
from util import parse_dt, dt_to_str, raw_order_coll, config_coll

def smin(a, b):
    if a == None: return b
    if b == None: return a
    return min(a, b)

def smax(a, b):
    if a == None: return b
    if b == None: return a
    return max(a, b)

def filter_orders(orders, sites):
    # only process orders with right site and machine
    return [x for x in orders if x['site'] in sites.keys()
            and x['machine'] in sites[x['site']]['machines']]

def condense_orders(orders):
    # combine scans of the same patient
    by_mrn = {}
    for x in orders:
        if x['mrn'] not in by_mrn:
            by_mrn[x['mrn']] = x
        else:
            d = by_mrn[x['mrn']]
            d['accession'] = d['accession'] + '|' + x['accession']
            d['appointment_dt'] = smin(d['appointment_dt'], x['appointment_dt'])
            d['arrival_dt'] = smin(d['arrival_dt'], x['arrival_dt'])
            d['begin_dt'] = smin(d['begin_dt'], x['begin_dt'])
            d['completed_dt'] = smax(d['completed_dt'], x['completed_dt'])
            d['schedule_dt'] = smin(d['schedule_dt'], x['schedule_dt'])
            d['service'] = d['service'] + '|' + x['service']
            d['slot'] = d['slot'] + x['slot']

    return list(by_mrn.values())

def valid_order(x):
    # detect corrupted states
    if x['schedule_dt'] == None:
        # this will remove SDAOP who is not known yet
        return False
    if x['arrival_dt'] == None and x['begin_dt'] != None:
        return False
    if x['arrival_dt'] == None and x['completed_dt'] != None:
        return False
    if x['begin_dt'] == None and x['completed_dt'] != None:
        return False
    if x['arrival_dt'] != None and x['begin_dt'] != None and x['arrival_dt'] > x['begin_dt']:
        return False
    if x['arrival_dt'] != None and x['completed_dt'] != None and x['arrival_dt'] > x['completed_dt']:
        return False
    if x['begin_dt'] != None and x['completed_dt'] != None and x['begin_dt'] > x['completed_dt']:
        return False
    return True

def mask_dt(orders, time):
    for x in orders:
        for k in ['arrival_dt', 'begin_dt', 'completed_dt', 'schedule_dt']:
            if x[k] != None and x[k] > time:
                x[k] = None

def time_to_str(orders):
    for x in orders:
        for k in ['arrival_dt', 'begin_dt', 'completed_dt', 'schedule_dt', 'appointment_dt']:
            if x[k] != None:
                x[k] = dt_to_str(x[k])

def fix_completion_time(orders):
    # If a order is started on the same machine, then previous order will be marked as completed
    begin_orders = [x for x in orders if x['begin_dt'] != None]
    begin_orders.sort(key=lambda x : x['begin_dt'])
    h = {}
    for x in begin_orders:
        sm = '{}-{}'.format(x['site'], x['machine'])
        if sm not in h:
            h[sm] = []
        h[sm].append(x)

    for xs in h.values():
        for i in range(1, len(xs)):
            xs[i-1]['completed_dt'] = smin(xs[i-1]['completed_dt'], xs[i]['begin_dt'])

def get_schedule(time):
    # time is str of format '2012-05-05 12:30:15'
    # and we will get schedule of that day until that time
    sites = config_coll.find_one({'name': 'site'})['data']

    day = datetime.combine(time.date(), datetime.min.time())
    next_day = day + timedelta(1)

    orders = list(
        raw_order_coll.find({
            'appointment_dt': {
                '$gt': day,
                '$lt': next_day
            }
        })
    )
    for x in orders:
        del x['_id']

    mask_dt(orders, time)
    orders = [x for x in orders if valid_order(x)]
    orders = filter_orders(orders, sites)
    orders = condense_orders(orders)
    fix_completion_time(orders)
    orders.sort(key =lambda x : x['appointment_dt'])
#   time_to_str(orders)
    return orders

if __name__ == '__main__':
    time = parse_dt('2014-09-27 8:30:15')
    orders = get_schedule(time)
    for x in orders:
        print(x['site'], x['machine'])
