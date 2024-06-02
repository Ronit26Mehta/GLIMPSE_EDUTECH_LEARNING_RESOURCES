import re
from collections import defaultdict, Counter
from datetime import datetime

log_pattern = re.compile(
    r'(?P<ip>\S+) - - \[(?P<timestamp>.+?)\] "(?P<request>.+?)" (?P<status>\d{3}) (?P<size>\d+)'
)

def parse_log_line(line):
    match = log_pattern.match(line)
    if match:
        return match.groupdict()
    return None

def analyze_logs(log_lines):
    logs_by_date = defaultdict(list)
    status_counter = Counter()
    
    for line in log_lines:
        data = parse_log_line(line)
        if data:
            timestamp = datetime.strptime(data['timestamp'], '%d/%b/%Y:%H:%M:%S %z')
            date_str = timestamp.date().isoformat()
            logs_by_date[date_str].append(data)
            status_counter[data['status']] += 1
    
    return logs_by_date, status_counter
