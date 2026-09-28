# 📱 Cross-Platform Face Recognition Attendance System

A modern, responsive, web-based automated attendance platform optimized for both **Windows Desktop** and **Android Mobile** browsers. Built entirely using open-source tools with **zero hardware requirements** or costly third-party cloud messaging subscriptions.

---

## 🌟 Core Highlights
* **Cross-Platform Compatibility:** Runs on native desktop screens and mobile Android viewports utilizing responsive HTML5 and vanilla JavaScript camera APIs.
* **Open-Source Biometric Engine:** Bypasses complex C++ installation loops (`dlib`/`CMake`) by utilizing a custom **NumPy Pixel-Matrix Normalization & Cross-Correlation Engine** powered by `Pillow`.
* **Smart Session Engine:** Automatically calculates attendance status based on real-time check-in windows (Before 10:00 AM = Half-Day Present, Before 2:00 PM = Full-Day Present, post-2:00 PM/No Check-In = Absent).
* **100% Free Mobile Push Notifications:** Drops expensive hardware or cloud gateways (like Twilio) in favour of an instant, unlimited push alert stream using the **ntfy.sh** global pub-sub protocol.
* **Visualization Dashboard:** Includes an elegant tracking dashboard featuring responsive CSS percentage visualizer progress bars.

---

## 📁 VS Code Directory Architecture

Ensure your local folder structure is organized exactly like this before pushing to GitHub:

```text
attendance_project/
│
├── app.py                      # Main Flask App & Router Controller
├── database.py                 # SQLite Database Schema Definitions
├── auth.py                     # Case-Insensitive Auth Verification Engine
├── face_verifier.py            # NumPy Matrix Face Matching Engine
├── attendance_calc.py          # Session-Based Rules Matrix
├── notification.py             # Free ntfy.sh Push Notification Broadcaster
│
├── templates/                  # Responsive Frontend Web Templates
│   ├── welcome.html            # Page 1: Home Welcome
│   ├── signup_select.html      # Page 2: Signup Core router
│   ├── register.html           # Page 3: Enrollment Interface (Camera/Upload hybrid)
│   ├── success.html            # Page 4: Success Acknowledgement 
│   ├── login.html              # Page 5: Secure Credential Entry Gateway
│   ├── main_camera.html        # Page 6: Live Web-Cam Verification Face-Check
│   └── dashboard.html          # Page 7: Performance Analytics Dashboard
└── static/
    └── uploads/                # Secured Storage Space for Profile Pictures
```

---

## 🛠️ Step-by-Step Installation & Execution

### 1. Prerequisites
Ensure you have **Python 3.11+** installed on your operating system.

### 2. Download Project and Install Modules
Open your terminal space inside VS Code (`Ctrl + ~`) and install the lightweight, open-source dependency framework:
```bash
pip install Flask requests numpy Pillow pyopenssl
```

### 3. Kickstart Server Engine Loop
Run the master routing script to spin up the local database instances and launch the secure development web socket:
```bash
python app.py
```

### 4. Cross-Platform Network Access
Your server logs will display a localized network stream blueprint:
* **Testing locally on PC:** Navigate to `https://127.0.0.1:5000`
* **Testing from Android Mobile:** Ensure your phone is on the same local Wi-Fi router network. Open your mobile browser and enter your network IP directly (e.g., `https://10.116.134.171:5000`).

> ⚠️ **Important Security Context Step:** Because the server utilizes an auto-generated development encryption certificate (`ssl_context='adhoc'`), your browser will show a warning stating *"Your connection is not private"*. Click **Advanced** and choose **Proceed to IP (unsafe)**. This is required to let the browser safely spin up the device hardware camera without blocking it.

---

## 📱 Setting Up Mobile Lockscreen Push Alerts (100% Free)

To deliver instant attendance confirmation pings directly to target mobile phones without hardware chips, have users follow these quick configurations:

1. Download the free **ntfy** client app from the **Google Play Store** or **Apple App Store**.
2. Tap the **`+` (Subscribe to topic)** button.
3. Input the unique subscription string assigned dynamically by the system.
   * **Topic Format Rule:** `attendance_[role]_[CAPITALIZED_NAME]_[ID]`
   * *Example for Student named Saran with Roll Number 26AD001:* **`attendance_student_SARAN_26AD001`**
4. Tap **Subscribe**. 

Once the student finishes their facial verification matrix scan, the lockscreen will instantly sound an alert banner with verification metrics!

---

## 🧪 Tech Stack Profile
* **Backend Framework:** Flask (Python)
* **Database Layer:** SQLite3 (Embedded relational storage core)
* **Biometric Calculations Processing:** NumPy Matrix Normalization Engine
* **Image Processing Manipulation:** Pillow (PIL)
* **Notification Network API:** ntfy.sh Pub-Sub Gateway
