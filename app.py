from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import os
import sqlite3
import base64
from database import init_db
from auth import verify_user
from face_verifier import verify_face_biometrics
from attendance_calc import calculate_and_log_attendance
from notification import send_sms_notification

app = Flask(__name__)
app.secret_key = 'super_secure_attendance_system_key'
UPLOAD_FOLDER = os.path.join('static', 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

init_db()

@app.route('/')
def page_1_welcome():
    return render_template('welcome.html')

@app.route('/signup-select')
def page_2_signup_select():
    return render_template('signup_select.html')

@app.route('/register/<role>')
def page_3_register(role):
    return render_template('register.html', role=role)

@app.route('/submit-registration', methods=['POST'])
def submit_registration():
    role = request.form.get('role')
    name = request.form.get('name').strip().upper()
    department = request.form.get('department')
    mobile = request.form.get('mobile')
    photo_data = request.form.get('photo') # Base64 web stream frame string
    
    # Input Validation checks
    if len(mobile) != 10 or not mobile.isdigit():
        return "Error: Mobile number must contain exactly 10 digits.", 400

    username = name # System requirement specification
    
    conn = sqlite3.connect('attendance.db')
    cursor = conn.cursor()
    
    # Decode and save target capture profile photo path safely
    header, encoded = photo_data.split(",", 1)
    img_bytes = base64.b64decode(encoded)
    filename = f"{username}_{role}.jpg"
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    with open(filepath, "wb") as f:
        f.write(img_bytes)

    if role == 'student':
        batch_prefix = int(request.form.get('batch'))
        batch_suffix = batch_prefix + 4
        batch_string = f"{batch_prefix}-{batch_suffix}"
        roll_number = request.form.get('roll_number').strip().upper()
        password = roll_number
        
        try:
            cursor.execute("""INSERT INTO student_attendance 
                (name, username, department, batch, mobile_number, roll_number, student_password, photo_path) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)""", 
                (name, username, department, batch_string, mobile, roll_number, password, filepath))
        except sqlite3.IntegrityError:
            conn.close()
            return "Error: Roll Number or Username already exists.", 400
    else:
        teachers_id = request.form.get('teachers_id').strip().upper()
        password = teachers_id
        
        try:
            cursor.execute("""INSERT INTO teachers_attendance 
                (name, username, department, mobile_number, teachers_id, teachers_password, photo_path) 
                VALUES (?, ?, ?, ?, ?, ?, ?)""", 
                (name, username, department, mobile, teachers_id, password, filepath))
        except sqlite3.IntegrityError:
            conn.close()
            return "Error: Teacher ID or Username already exists.", 400
            
    conn.commit()
    conn.close()
    return redirect(url_for('page_4_success'))

@app.route('/success')
def page_4_success():
    return render_template('success.html')

@app.route('/login/<role>')
def page_5_login(role):
    return render_template('login.html', role=role)

@app.route('/verify-login', methods=['POST'])
def verify_login():
    username = request.form.get('username')
    password = request.form.get('password')
    role = request.form.get('role')
    
    if verify_user(username, password, role):
        session['user'] = username.strip().upper()
        session['role'] = role
        return redirect(url_for('page_6_main_camera'))
    else:
        return "Invalid Credentials. Go back and check uppercase entries.", 401

@app.route('/main-camera')
def page_6_main_camera():
    if 'user' not in session:
        return redirect(url_for('page_1_welcome'))
    return render_template('main_camera.html', username=session['user'], role=session['role'])

@app.route('/process-attendance', methods=['POST'])
def process_attendance():
    if 'user' not in session:
        return jsonify({"success": False, "message": "Unauthorized session status"}), 401
        
    data = request.json
    live_frame = data.get('image')
    username = session['user']
    role = session['role']
    
    # 1. Biometric Match verification engine processing
    face_matched = verify_face_biometrics(username, role, live_frame)
    
    if face_matched:
        # 2. Time-window session calculation logs execution
        status_message, is_new_log = calculate_and_log_attendance(username, role)
        
        # 3. Trigger free push notifications stream channel explicitly
        # This sends notifications on every verification match for robust live testing!
        send_sms_notification(username, role, status_message)
            
        return jsonify({"success": True, "message": f"Verified! Status: {status_message}"})
    else:
        return jsonify({"success": False, "message": "Face recognition verification failed! Position camera clearly."})


@app.route('/dashboard')
def page_7_dashboard():
    if 'user' not in session:
        return redirect(url_for('page_1_welcome'))
        
    username = session['user']
    conn = sqlite3.connect('attendance.db')
    cursor = conn.cursor()
    
    # Fetch log distribution data for the visualization metrics tracking engine
    cursor.execute("SELECT status, COUNT(*) FROM attendance_logs WHERE username=? GROUP BY status", (username,))
    logs = cursor.fetchall()
    conn.close()
    
    data_dict = {"Full-Day Present": 0, "Half-Day Present": 0, "Absent": 0}
    for status, count in logs:
        if status in data_dict:
            data_dict[status] = count
            
    return render_template('dashboard.html', username=username, metrics=data_dict)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('page_1_welcome'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True, ssl_context='adhoc')

