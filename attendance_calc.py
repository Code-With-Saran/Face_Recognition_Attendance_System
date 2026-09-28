from datetime import datetime
import sqlite3

def calculate_and_log_attendance(username, role):
    now = datetime.now()
    current_time = now.time()
    current_date = now.strftime("%Y-%m-%d")
    
    # Rule Evaluation Engine Parameters
    time_10am = datetime.strptime("10:00:00", "%H:%M:%S").time()
    time_2pm = datetime.strptime("14:00:00", "%H:%M:%S").time()
    
    session = ""
    status = ""
    
    if current_time <= time_10am:
        session = "Morning"
        status = "Half-Day Present"
    elif current_time <= time_2pm:
        session = "Afternoon"
        status = "Full-Day Present"
    else:
        session = "Late"
        status = "Absent"
        
    conn = sqlite3.connect('attendance.db')
    cursor = conn.cursor()
    
    # Check if duplicate log for current session exists to avoid override tracking bugs
    cursor.execute("SELECT id FROM attendance_logs WHERE username=? AND date=? AND session=?", (username.upper(), current_date, session))
    if cursor.fetchone():
        conn.close()
        return f"Already marked for {session} session.", False
        
    cursor.execute("INSERT INTO attendance_logs (username, role, date, session, status) VALUES (?, ?, ?, ?, ?)",
                   (username.upper(), role, current_date, session, status))
    conn.commit()
    conn.close()
    
    return status, True
