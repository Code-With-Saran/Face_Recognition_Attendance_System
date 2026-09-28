import sqlite3

def verify_user(username, password, role):
    # Enforce global input rules: convert incoming checks into clean uppercase matching database records
    username_cap = username.strip().upper()
    password_cap = password.strip().upper()
    
    conn = sqlite3.connect('attendance.db')
    cursor = conn.cursor()
    
    if role == 'student':
        cursor.execute("SELECT name FROM student_attendance WHERE username=? AND student_password=?", (username_cap, password_cap))
    else:
        cursor.execute("SELECT name FROM teachers_attendance WHERE username=? AND teachers_password=?", (username_cap, password_cap))
        
    user = cursor.fetchone()
    conn.close()
    return user is not None
