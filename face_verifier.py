import sqlite3
import os
import base64
import io
from PIL import Image
import numpy as np

def verify_face_biometrics(username, role, live_image_base64):
    conn = sqlite3.connect('attendance.db')
    cursor = conn.cursor()
    
    if role == 'student':
        cursor.execute("SELECT photo_path FROM student_attendance WHERE username=?", (username.upper(),))
    else:
        cursor.execute("SELECT photo_path FROM teachers_attendance WHERE username=?", (username.upper(),))
        
    result = cursor.fetchone()
    conn.close()
    
    if not result:
        print("User photo record not found in database.")
        return False
        
    registered_photo_path = result[0]
    if not os.path.exists(registered_photo_path):
        print("Registered file path is missing on local drive storage.")
        return False
        
    try:
        # 1. Decode and normalize the live webcam stream frame
        header, encoded = live_image_base64.split(",", 1)
        live_bytes = base64.b64decode(encoded)
        live_img = Image.open(io.BytesIO(live_bytes)).convert('L') # Convert to Greyscale
        live_img = live_img.resize((150, 150)) # Standardize array grid resolution dimensions
        live_matrix = np.array(live_img, dtype=np.float32)
        
        # 2. Open and normalize the registered profile snapshot file from disk
        reg_img = Image.open(registered_photo_path).convert('L') # Convert to Greyscale
        reg_img = reg_img.resize((150, 150)) # Standardize array grid resolution dimensions
        reg_matrix = np.array(reg_img, dtype=np.float32)
        
        # 3. Structural Normalized Matrix Cross-Correlation Calculation
        v1_norm = live_matrix - np.mean(live_matrix)
        v2_norm = reg_matrix - np.mean(reg_matrix)
        
        denominator = np.sqrt(np.sum(v1_norm**2) * np.sum(v2_norm**2))
        if denominator == 0:
            return False
            
        similarity_score = np.sum(v1_norm * v2_norm) / denominator
        print(f"Biometric array structural similarity verification match factor: {similarity_score}")
        
        # Adjust the match sensitivity threshold. 
        # For pixel-to-pixel matrix matching on a stable face, 0.15 - 0.20 indicates a match.
        return similarity_score > 0.15
        
    except Exception as e:
        print(f"Matrix verification processing failure: {e}")
        return False
