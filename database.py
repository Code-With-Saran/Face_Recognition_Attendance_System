import sqlite3

def init_db():
    conn = sqlite3.connect('attendance.db')
    cursor = conn.cursor()
    
    # Student Database Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS student_attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            username TEXT UNIQUE NOT NULL,
            department TEXT NOT NULL,
            batch TEXT NOT NULL,
            mobile_number TEXT NOT NULL,
            roll_number TEXT UNIQUE NOT NULL,
            student_password TEXT NOT NULL,
            photo_path TEXT NOT NULL
        )
    ''')
    
    # Teacher Database Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS teachers_attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            username TEXT UNIQUE NOT NULL,
            department TEXT NOT NULL,
            mobile_number TEXT NOT NULL,
            teachers_id TEXT UNIQUE NOT NULL,
            teachers_password TEXT NOT NULL,
            photo_path TEXT NOT NULL
        )
    ''')
    
    # Attendance Tracking Log
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS attendance_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            role TEXT NOT NULL,
            date TEXT NOT NULL,
            session TEXT NOT NULL,
            status TEXT NOT NULL
        )
    ''')
    
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    print("Databases initialized successfully.")
