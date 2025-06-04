from flask import Flask, render_template, request, redirect, session
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = 'your_secret_key'  

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Dhanush@1'  
app.config['MYSQL_DB'] = 'complaint_db'

mysql = MySQL(app)


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/submit', methods=['GET', 'POST'])
def submit_complaint():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        register_number = request.form['register_number']
        department = request.form['department']
        year = request.form['year']
        category = request.form['category']
        title = request.form['title']
        description = request.form['description']

        cur = mysql.connection.cursor()

       
        cur.execute("SELECT * FROM students WHERE register_number = %s AND department = %s AND year = %s",
                    (register_number, department, year))
        student = cur.fetchone()

        if not student:
            return render_template('submit_complaint.html', error="You are not a verified student. Complaint not accepted.")

    
        cur.execute("""
            INSERT INTO complaints (student_name, email, register_number, department, year, category, title, description, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 'Submitted')
        """, (name, email, register_number, department, year, category, title, description))
        mysql.connection.commit()

        return redirect(f'/my_complaint?email={email}')

    return render_template('submit_complaint.html')


@app.route('/my_complaint')
def my_complaints():
    email = request.args.get('email')
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM complaints WHERE email = %s", (email,))
    complaints = cur.fetchall()
    return render_template('my_complaint.html', complaints=complaints, email=email)


@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        admin_id = request.form['admin_id']
        password = request.form['password']

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM admins WHERE admin_id = %s AND password = %s", (admin_id, password))
        admin = cur.fetchone()

        if admin:
            session['admin_logged_in'] = True
            return redirect('/adminlogin')
        else:
            return render_template('adminlogin.html', error="Invalid ID or password")

    return render_template('adminlogin.html')

@app.route('/admin', methods=['GET', 'POST'])
def admin_dashboard():
    if not session.get('admin_logged_in'):
        return redirect('/adminlogin')

    cur = mysql.connection.cursor()

    if request.method == 'POST':
        complaint_id = request.form['complaint_id']
        new_status = request.form['status']
        cur.execute("UPDATE complaints SET status = %s WHERE complaint_id = %s", (new_status, complaint_id))
        mysql.connection.commit()

    cur.execute("SELECT * FROM complaints ORDER BY submitted_on DESC")
    complaints = cur.fetchall()
    return render_template('admindash.html', complaints=complaints)


@app.route('/admin_logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)