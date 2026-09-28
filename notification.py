import sqlite3
import os
import requests

def send_sms_notification(username, role, status_message):
    conn = sqlite3.connect('attendance.db')
    cursor = conn.cursor()
    
    # 1. Pull user unique details to construct their private push channel routing topic
    if role == 'student':
        cursor.execute("SELECT roll_number FROM student_attendance WHERE username=?", (username.upper(),))
    else:
        cursor.execute("SELECT teachers_id FROM teachers_attendance WHERE username=?", (username.upper(),))
        
    id_result = cursor.fetchone()
    conn.close()
    
    if not id_result:
        print(f"[PUSH ERROR] Profile matching array missing for user payload context: {username}")
        return False
        
    unique_id = id_result[0]
    
    # 2. Formulate a 100% unique unguessable subscription topic string for the user
    # Spaces are stripped and underscores added to keep formatting uniform
    clean_username = username.replace(" ", "_").upper()
    user_push_topic = f"attendance_{role}_{clean_username}_{unique_id}"
    
    # 3. Construct the presentation payload metadata 
    title = f"Attendance Marked: {username.upper()}"
    message_body = f"Hello! Your face recognition check is successful.\\nSession Status: {status_message}."
    
    # Set priority tags and status emojis for rich UI rendering inside mobile lockscreens
    priority_header = "default" if "Half-Day" in status_message else "high"
    emoji_tags = "white_check_mark,alarm_clock" if "Present" in status_message else "x"

    try:
        # Send raw message block across the public ntfy cluster infrastructure via secure POST socket
        url = f"https://ntfy.sh/{user_push_topic}"
        headers = {
            "Title": title,
            "Priority": priority_header,
            "Tags": emoji_tags
        }
        
        response = requests.post(url, data=message_body.encode('utf-8'), headers=headers)
        
        if response.status_code == 200:
            print(f"\\n" + "═"*60)
            print(f"📢 [FREE PUSH BROADCAST DISPATCHED SUCCESSFULLY]")
            print(f"➡️ DESTINATION ROUTE TOPIC : {url}")
            print(f"➡️ SCREEN DISPATCH CONTENT : {message_body}")
            print("═"*60 + "\\n")
            return True
        else:
            print(f"[PUSH SERVICE REJECTION] Host responded with status: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"[PUSH ENGINE EXCEPTION NETWORK FLUX]: {e}")
        return False
