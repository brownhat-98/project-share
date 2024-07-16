
from datetime import datetime

def parse_time(time_str):
    time_str = time_str.strip().lower().replace(' ', '')
    if 'am' in time_str or 'pm' in time_str:
        return datetime.strptime(time_str, '%I:%M%p').time()
    return datetime.strptime(time_str, '%H:%M').time()
