from util import dist_coll

def get_duration_distribution(service, slot):
    d = dist_coll.find_one({'name': 'Duration {} {}'.format(service, slot)})
    if d == None:
        d = dist_coll.find_one({'name': 'Duration {}'.format(slot)})
    if d == None:
        print('used uniform distribution')
        return 'uniform({},{})'.format(slot-5, slot+5)
    return {
        'name': d['name'],
        'base': d['base'],
        'pmf': d['pmf']
    }

def get_lateness_distribution():
    return 'uniform(0,0)'

#   d = dist_coll.find_one({'name': 'Lateness'})
#   return {
#       'name': 'Lateness',
#       'base': d['base'] + lateness_offset,
#       'pmf': d['pmf']
#   }
