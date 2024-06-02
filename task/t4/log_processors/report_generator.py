def generate_summary_report(logs_by_date, status_counter):
    report = []
    report.append("Summary Report\n")
    report.append("====================\n\n")
    
    report.append("Status Code Count:\n")
    for status, count in status_counter.items():
        report.append(f"{status}: {count}\n")
    
    report.append("\nLogs by Date:\n")
    for date, logs in logs_by_date.items():
        report.append(f"{date}: {len(logs)} log entries\n")
    
    return "\n".join(report)

def save_report(report, output_path):
    with open(output_path, 'w') as file:
        file.write(report)
