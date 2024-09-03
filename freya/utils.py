from datetime import datetime, timedelta

def calculate_job_apply_end_date(last_seen):
    try:
        last_seen_date = datetime.strptime(last_seen, "%Y-%m-%d %H:%M:%S")
        end_date = last_seen_date + timedelta(days=30)
        return end_date.strftime("%Y-%m-%d %H:%M:%S")
    except ValueError:
        return 'N/A'
    
def clean_string(s):
    # Implement string cleaning logic
    return s.strip()

def format_date(date_string):
    # Implement date formatting logic
    return date_string