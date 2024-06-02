import os
from log_processors.file_handler import ensure_directory_exists, read_log_files, read_log_file, write_log_file
from log_processors.data_analyzer import analyze_logs
from log_processors.report_generator import generate_summary_report, save_report
from log_processors.utils import generate_sample_logs, calculate_average_requests_per_hour

def main():
    current_directory = os.path.dirname(os.path.abspath(__file__))
    log_directory = os.path.join(current_directory, 'logs')
    output_directory = os.path.join(current_directory, 'output')
    
    ensure_directory_exists(log_directory)
    ensure_directory_exists(output_directory)
    
    # Parameters for log generation
    num_log_files = 5
    num_entries_per_file = 100
    
    # Generate log files with randomized entries
    for i in range(num_log_files):
        log_entries = generate_sample_logs(num_entries_per_file)
        write_log_file(os.path.join(log_directory, f"log_{i+1}.log"), log_entries)
    
    # Process the generated log files
    log_files = read_log_files(log_directory)
    all_log_lines = []
    
    for log_file in log_files:
        all_log_lines.extend(read_log_file(log_file))
    
    logs_by_date, status_counter = analyze_logs(all_log_lines)
    
    report = generate_summary_report(logs_by_date, status_counter)
    save_report(report, os.path.join(output_directory, "summary_report.txt"))
    
    avg_requests_per_hour = calculate_average_requests_per_hour(logs_by_date)
    print(f"Average Requests Per Hour: {avg_requests_per_hour}")

if __name__ == "__main__":
    main()
