from datetime import datetime, time
import pymongo

db = pymongo.MongoClient().schedule
raw_order_coll = db.raw_order
dist_coll = db.distribution
config_coll = db.config

def parse_dt(s):
    dt = datetime.strptime(s, '%Y-%m-%d %H:%M:%S')
    return dt

def dt_to_str(dt):
    return dt.strftime('%Y-%m-%d %H:%M:%S')

def get_mins(dt):
    if dt == None:
        return None
    date = datetime.combine(dt.date(), time.min)
    return round((dt - date).total_seconds() / 60)
