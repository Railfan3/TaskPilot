# utils.py

from datetime import datetime

def parse_date(date_str):
    for fmt in ("%Y-%m-%d", "%d-%m-%Y", "%d/%m/%Y", "%Y/%m/%d"):
        try:
            return datetime.strptime(date_str, fmt).date()
        except ValueError:
            continue
    raise ValueError(f"Date format not recognized: {date_str}")

def parse_time(time_str):
    time_str = time_str.strip().replace('.', ':').upper()
    for fmt in ("%I:%M %p", "%H:%M", "%I:%M%p"):
        try:
            return datetime.strptime(time_str, fmt).strftime("%I:%M %p")
        except ValueError:
            continue
    raise ValueError(f"Time format not recognized: {time_str}")
