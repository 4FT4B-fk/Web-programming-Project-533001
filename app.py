from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import calendar
import os
import hashlib
import secrets

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'university_portal'
}

def hash_password_simple(password):
    """Simple password hashing for testing purposes"""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password_simple(password, hashed):
    """Simple password verification for testing purposes"""
    return hashlib.sha256(password.encode()).hexdigest() == hashed

def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)

def get_day_classes(day_name, day_number):
    """Get CSS classes for a specific day"""
    classes = []
    
    classes.append(day_name.lower())
    
    special_dates = {
        15: 'exam-day',
        25: 'holiday',
        30: 'assignment-due'
    }
    
    if day_number in special_dates:
        classes.append(special_dates[day_number])
    
    return classes

def generate_calendar_data(enrolled_courses):
    """Generate calendar data for the current month"""
    now = datetime.now()
    current_month = now.month
    current_year = now.year
    
    month_name = calendar.month_name[current_month]
    
    first_day = calendar.monthrange(current_year, current_month)[0]
    days_in_month = calendar.monthrange(current_year, current_month)[1]
    
    first_day = (first_day + 1) % 7
    
    schedule_by_day = {}
    for course in enrolled_courses:
        if course.get('day_of_week') and course.get('start_time'):
            day = course['day_of_week']
            if day not in schedule_by_day:
                schedule_by_day[day] = []
            schedule_by_day[day].append({
                'course_code': course['course_code'],
                'start_time': course['start_time'],
                'room': course.get('room', 'TBA')
            })
    
    calendar_data = {
        'month_year': f"{month_name} {current_year}",
        'weeks': [],
        'today': now.day
    }
    
    current_week = []
    
    for i in range(first_day):
        current_week.append({'day': None, 'classes': [], 'css_classes': ['empty']})
    
    for day in range(1, days_in_month + 1):
        date_obj = datetime(current_year, current_month, day)
        day_name = date_obj.strftime('%A')
        
        classes = schedule_by_day.get(day_name, [])
        
        css_classes = get_day_classes(day_name, day)
        
        current_week.append({
            'day': day,
            'classes': classes,
            'is_today': day == now.day,
            'css_classes': css_classes
        })
        
        if len(current_week) == 7:
            calendar_data['weeks'].append(current_week)
            current_week = []
    
    if current_week:
        while len(current_week) < 7:
            current_week.append({'day': None, 'classes': [], 'css_classes': ['empty']})
        calendar_data['weeks'].append(current_week)
    
    return calendar_data

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        
        if user and (check_password_hash(user['password'], password) or verify_password_simple(password, user['password'])):
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['role'] = user['role']
            session['full_name'] = user['full_name']
            
            if user['role'] == 'student':
                return redirect(url_for('student_dashboard'))
            else:
                return redirect(url_for('professor_dashboard'))
        else:
            flash('Invalid username or password')
            return redirect(url_for('home'))
        
        cursor.close()
        conn.close()
    
    return redirect(url_for('home'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        full_name = request.form['full_name']
        
        
        
        try:
            hashed_password = generate_password_hash(password)
        except:
            hashed_password = hash_password_simple(password)
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                "INSERT INTO users (username, email, password, role, full_name) VALUES (%s, %s, %s, 'student', %s)",
                (username, email, hashed_password, full_name)
            )
            conn.commit()
            flash('Registration successful! Please login.')
            return redirect(url_for('login'))
        except mysql.connector.IntegrityError:
            flash('Username or email already exists')
        
        cursor.close()
        conn.close()
    
    return render_template('register.html')

@app.route('/student_dashboard')
def student_dashboard():
    if 'user_id' not in session or session['role'] != 'student':
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("""
        SELECT c.*, s.day_of_week, s.start_time, s.end_time, s.room, u.full_name as professor_name
        FROM courses c
        JOIN enrollments e ON c.id = e.course_id
        LEFT JOIN schedule s ON c.id = s.course_id
        LEFT JOIN users u ON c.professor_id = u.id
        WHERE e.student_id = %s
        ORDER BY s.day_of_week, s.start_time
    """, (session['user_id'],))
    enrolled_courses = cursor.fetchall()
    
    calendar_data = generate_calendar_data(enrolled_courses)
    
    cursor.execute("""
        SELECT n.*, c.course_name, u.full_name as professor_name
        FROM notifications n
        JOIN courses c ON n.course_id = c.id
        JOIN users u ON n.professor_id = u.id
        JOIN enrollments e ON c.id = e.course_id
        WHERE e.student_id = %s
        ORDER BY n.created_at DESC
        LIMIT 10
    """, (session['user_id'],))
    notifications = cursor.fetchall()
    
    cursor.execute("""
        SELECT DISTINCT u.full_name, u.email, pc.office_location, pc.office_hours, c.course_name
        FROM users u
        JOIN courses c ON u.id = c.professor_id
        JOIN enrollments e ON c.id = e.course_id
        LEFT JOIN professor_contacts pc ON u.id = pc.professor_id
        WHERE e.student_id = %s AND u.role = 'professor'
    """, (session['user_id'],))
    professor_contacts = cursor.fetchall()
    
    cursor.execute("""
        SELECT c.*, u.full_name as professor_name
        FROM courses c
        LEFT JOIN users u ON c.professor_id = u.id
        WHERE c.id NOT IN (
            SELECT course_id FROM enrollments WHERE student_id = %s
        )
    """, (session['user_id'],))
    available_courses = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return render_template('student_dashboard.html', 
                         enrolled_courses=enrolled_courses,
                         calendar_data=calendar_data,
                         notifications=notifications,
                         professor_contacts=professor_contacts,
                         available_courses=available_courses)

@app.route('/professor_dashboard')
def professor_dashboard():
    if 'user_id' not in session or session['role'] != 'professor':
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("SELECT * FROM courses WHERE professor_id = %s", (session['user_id'],))
    courses = cursor.fetchall()
    
    cursor.execute("""
        SELECT n.*, c.course_name
        FROM notifications n
        JOIN courses c ON n.course_id = c.id
        WHERE n.professor_id = %s
        ORDER BY n.created_at DESC
        LIMIT 10
    """, (session['user_id'],))
    notifications = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return render_template('professor_dashboard.html', courses=courses, notifications=notifications)

@app.route('/enroll_course', methods=['POST'])
def enroll_course():
    if 'user_id' not in session or session['role'] != 'student':
        return redirect(url_for('login'))
    
    course_id = request.form['course_id']
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute(
            "INSERT INTO enrollments (student_id, course_id) VALUES (%s, %s)",
            (session['user_id'], course_id)
        )
        conn.commit()
        flash('Successfully enrolled in course!')
    except mysql.connector.IntegrityError:
        flash('Already enrolled in this course')
    
    cursor.close()
    conn.close()
    
    return redirect(url_for('student_dashboard'))

@app.route('/drop_course', methods=['POST'])
def drop_course():
    if 'user_id' not in session or session['role'] != 'student':
        return redirect(url_for('login'))
    
    course_id = request.form['course_id']
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        "DELETE FROM enrollments WHERE student_id = %s AND course_id = %s",
        (session['user_id'], course_id)
    )
    conn.commit()
    
    cursor.close()
    conn.close()
    
    flash('Successfully dropped course!')
    return redirect(url_for('student_dashboard'))

@app.route('/add_notification', methods=['POST'])
def add_notification():
    if 'user_id' not in session or session['role'] != 'professor':
        return redirect(url_for('login'))
    
    course_id = request.form['course_id']
    title = request.form['title']
    message = request.form['message']
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        "INSERT INTO notifications (course_id, professor_id, title, message) VALUES (%s, %s, %s, %s)",
        (course_id, session['user_id'], title, message)
    )
    conn.commit()
    
    cursor.close()
    conn.close()
    
    flash('Notification added successfully!')
    return redirect(url_for('professor_dashboard'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
