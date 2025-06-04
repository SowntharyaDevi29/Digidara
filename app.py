from flask import Flask, render_template, request, redirect, session
import mysql.connector

app = Flask(__name__)
app.secret_key = 'your_secret_key'

db = mysql.connector.connect(
    host='localhost',
    user='root',
    password='Dhanush@1',
    database='complaint_db'
)
cursor = db.cursor()


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/submit', methods=['GET', 'POST'])
def submit_complaint():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        reg = request.form['register_number']
        dept = request.form['department']
        year = request.form['year']
        category = request.form['category']
        title = request.form['title']
        desc = request.form['description']

        cursor.execute("SELECT * FROM students WHERE register_number = %s AND department = %s AND year = %s", (reg, dept, year))
        student = cursor.fetchone()

        if not student:
            return render_template('submit_complaint.html', error="You are not a verified student.")

        cursor.execute("""
            INSERT INTO complaints (student_name, email, register_number, department, year, category, title, description, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 'Submitted')
        """, (name, email, reg, dept, year, category, title, desc))
        db.commit()

        return redirect(f'/my_complaints?email={email}')

    return render_template('submit_complaint.html')


@app.route('/my_complaint')
def my_complaints():
    email = request.args.get('email')
    cursor.execute("SELECT * FROM complaints WHERE email = %s", (email,))
    complaints = cursor.fetchall()
    return render_template('my_complaint.html', complaints=complaints, email=email)

@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        admin_id = request.form['admin_id']
        password = request.form['password']
        cursor.execute("SELECT * FROM admins WHERE admin_id = %s AND password = %s", (admin_id, password))
        admin = cursor.fetchone()

        if admin:
            session['admin_logged_in'] = True
            return redirect('/admin')
        else:
            return render_template('admin_login.html', error="Invalid ID or password")

    return render_template('admin_login.html')


@app.route('/admin', methods=['GET', 'POST'])
def admin_dashboard():
    if not session.get('admin_logged_in'):
        return redirect('/admin_login')

    if request.method == 'POST':
        complaint_id = request.form['complaint_id']
        status = request.form['status']
        cursor.execute("UPDATE complaints SET status = %s WHERE complaint_id = %s", (status, complaint_id))
        db.commit()

    cursor.execute("SELECT * FROM complaints ORDER BY submitted_on DESC")
    complaints = cursor.fetchall()
    return render_template('admin_dash.html', complaints=complaints)


@app.route('/admin_logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)