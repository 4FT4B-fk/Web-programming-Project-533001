from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import mysql.connector
import hashlib
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Replace with a secure key in production

# --- Upload configuration ---
UPLOAD_FOLDER = 'static/videos'
ALLOWED_EXTENSIONS = {'mp4', 'mov', 'avi'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# --- Database connection ---
def get_db_connection():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="123456",
        database="video_portal"
    )

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = hashlib.sha256(request.form['password'].encode()).hexdigest()

        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE username=%s AND password_hash=%s", (username, password))
        user = cursor.fetchone()
        cursor.close()
        db.close()

        if user:
            session['user_id'] = user['id']
            session['is_admin'] = user.get('is_admin', False)
            session['username'] = user['username']

            if session['is_admin']:
                return redirect(url_for('admin_dashboard'))
            else:
                return redirect(url_for('upload_video'))
        else:
            error = "❌ Invalid username or password."
    return render_template('index.html', error=error)

@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            error = "❌ Passwords do not match."
        else:
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            db = get_db_connection()
            cursor = db.cursor()
            try:
                cursor.execute("INSERT INTO users (username, email, password_hash) VALUES (%s, %s, %s)",
                               (username, email, password_hash))
                db.commit()
                return redirect(url_for('login'))
            except:
                error = "❌ Username or email already exists."
            finally:
                cursor.close()
                db.close()
    return render_template('register.html', error=error)

@app.route('/upload', methods=['GET', 'POST'])
def upload_video():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        file = request.files['video']

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
            file.save(file_path)

            cursor.execute("INSERT INTO videos (title, description, filename, user_id) VALUES (%s, %s, %s, %s)",
                           (title, description, filename, session['user_id']))
            db.commit()
            return redirect(url_for('play_video', filename=filename))

    cursor.execute("SELECT * FROM videos WHERE user_id = %s ORDER BY id DESC", (session['user_id'],))
    user_videos = cursor.fetchall()
    cursor.close()
    db.close()

    return render_template('upload.html', videos=user_videos)

@app.route('/play/<filename>')
def play_video(filename):
    return render_template('play.html', filename=filename)

@app.route('/api/videos')
def videos():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM videos")
    results = cursor.fetchall()
    cursor.close()
    db.close()

    videos_list = []
    for video in results:
        videos_list.append({
            'title': video['title'],
            'description': video['description'],
            'url': f"/static/videos/{video['filename']}"
        })

    return jsonify(videos_list)

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('is_admin', None)
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/admin')
def admin_dashboard():
    if not session.get('is_admin'):
        return "Access denied."

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    cursor.execute("SELECT * FROM videos")
    videos = cursor.fetchall()
    cursor.close()
    db.close()

    return render_template("admin.html", users=users, videos=videos)

@app.route('/admin/delete_user/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    if not session.get('is_admin'):
        return "Access denied."

    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
    db.commit()
    cursor.close()
    db.close()

    return redirect(url_for('admin_dashboard'))

@app.route('/admin/delete_video/<int:video_id>', methods=['POST'])
def delete_video(video_id):
    if not session.get('is_admin'):
        return "Access denied."

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT filename FROM videos WHERE id = %s", (video_id,))
    video = cursor.fetchone()

    if video:
        video_path = os.path.join(app.config['UPLOAD_FOLDER'], video['filename'])
        if os.path.exists(video_path):
            os.remove(video_path)
        cursor.execute("DELETE FROM videos WHERE id = %s", (video_id,))
        db.commit()

    cursor.close()
    db.close()
    return redirect(url_for('admin_dashboard'))

if __name__ == '__main__':
    app.run(debug=True)
