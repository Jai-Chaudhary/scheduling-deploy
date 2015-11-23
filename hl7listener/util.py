from datetime import datetime

def parse_dt(s):
    dt = datetime.strptime(s, '%Y-%m-%d %H:%M:%S')
    return dt

def dt_to_str(dt):
    return dt.strftime('%Y-%m-%d %H:%M:%S')
