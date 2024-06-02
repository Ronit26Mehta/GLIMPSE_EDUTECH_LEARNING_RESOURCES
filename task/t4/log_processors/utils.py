import random
from datetime import datetime, timedelta, timezone

def simulate_log_entry():
    ip = f"192.168.0.{random.randint(1, 255)}"
    timestamp = (datetime.now(timezone.utc) - timedelta(minutes=random.randint(1, 10000))).strftime('%d/%b/%Y:%H:%M:%S %z')
    request = random.choice(["GET /index.html HTTP/1.1", "POST /form HTTP/1.1", "GET /image.jpg HTTP/1.1"])
    status = random.choice([200, 404, 500, 403])
    size = random.randint(100, 5000)
    return f'{ip} - - [{timestamp}] "{request}" {status} {size}'

def generate_sample_logs(num_entries):
    return [simulate_log_entry() for _ in range(num_entries)]

def calculate_average_requests_per_hour(logs_by_date):
    total_requests = sum(len(logs) for logs in logs_by_date.values())
    total_hours = len(logs_by_date) * 24  # Assuming logs cover 24 hours per day
    if total_hours == 0:
        return 0  # Avoid division by zero
    return total_requests / total_hours
