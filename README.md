# 🎥 Video Player Web Application

This is a **Video Player Web Application** developed as a course project for **Web Programming**. The app allows users to log in, upload videos, and play them on a dedicated video player page. It's built with **Flask (Python)** for the backend, **HTML/CSS** for the frontend, and uses a **MySQL** database to manage user authentication.

---

## 🚀 Features
 
* 🆕 User registration
* 🔐 User login with MySQL authentication
* 📤 Upload video files from local devices
* 🎬 Playback uploaded videos using HTML5 video player
* 🗄️ MySQL database integration for user data and session management
* ✅ Clean, simple user interface with form validation

---

## 🧰 Tech Stack

* **Frontend**: HTML, CSS
* **Backend**: Python with Flask
* **Database**: MySQL
* **Web Server**: Flask development server

---

## 🖥️ Application Workflow

1. **Login Page (`/`)**
  Users log in with credentials stored in a MySQL database.
   
2. **Register Page ('/register')**
  Users provide a username and password to create a new account. The data is stored in the MySQL database.

3. **Upload Page (`/upload`)**
   After successful login, users can upload a video file.

4. **Player Page (`/play`)**
   The uploaded video is played using an HTML5 `<video>` element.

---

## 🛠️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/4FT4B-fk/Web-programming-Project-533001.git
cd Web-programming-Project-533001
```

### 2. Set Up MySQL Database

```Create a new MySQL database using the commands given in the "create db.sql".

**### Database Connection Function**

Make sure your app.py includes this function:

import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="Your username",
        password="Your Password",
        database="Name of your Database"
    )
```

### 6. Run the Flask App

```bash
python app.py
```

Then open your browser and visit:

```
http://127.0.0.1:5000/
```

---
