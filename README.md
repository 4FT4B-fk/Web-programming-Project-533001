# Web Programming Project - University Class Timetable

This is a web application project **"University Class Timetable Portal"**. It provides functionality for students and professors to manage and view class schedules, notifications, and contact information.

## 🚀 Features

- User authentication (student and professor roles)
- Admin/professor interface to create courses and schedule classes
- Student dashboard with:
  - 📅 Monthly calendar view of selected courses
  - 📬 Notification box for updates
  - 👩‍🏫 Professor contact section
- MySQL database for storing users, courses, schedules
- Responsive frontend styled with HTML/CSS

## 🗂 Project Structure

├── Web-programming-Project-533001/
│ ├── app.py
│ ├── scripts/
│ │ └── sample_data.sql
│ │ └── database_setup.sql
│ ├── static/
│ │ └── style.css
│ │ └── images/
│ │ └── logo.png
│ ├── templates/
│ │ └── base.html
│ │ └── home.html
│ │ └── login.html
│ │ └── register.html
│ │ └── student_dashboard.html
│ │ └── professor_dashboard.html

## ⚙️ Technologies Used

- Python (Flask)
- MySQL
- HTML, CSS

## 📦 Setup Instructions

1. Clone the repository  
   `git clone https://github.com/4FT4B-fk/Web-programming-Project-533001.git`

2. Navigate to the project directory  
   `cd Web-programming-Project-533001`

3. Set up virtual environment and install dependencies  
   *(optional depending on your Python setup)*

4. Import `scripts/database_setup.sql` and `sample_data.sql` into MySQL

5. Run the app  
   `python app.py`
