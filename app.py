from flask import Flask, render_template, request, redirect, url_for
import mysql.connector as mysqltor
from mysql.connector import IntegrityError

app = Flask(__name__)

# MySQL database configuration
mydb = mysqltor.connect(host="localhost", user="root", passwd="Your_password", database="student_db1", )
mycur = mydb.cursor()

# Create the student table if not exists
creat_tb = "CREATE TABLE IF NOT EXISTS student_tb (sroll VARCHAR(30) PRIMARY KEY, sname VARCHAR(30), sdob VARCHAR(30), satt VARCHAR(30))"
mycur.execute(creat_tb)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_student', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        roll = request.form['roll']
        name = request.form['name']
        dob = request.form['dob']
        att = request.form['att']

        data = (roll, name, dob, att)

        try:
            mycur.execute("INSERT INTO student_tb (sroll, sname, sdob, satt) VALUES (%s, %s, %s, %s)", data)
            mydb.commit()
            return redirect(url_for('add_student'))
        except IntegrityError:
            error_message = "Duplication Error: The student with roll number {} already exists in the database.".format(roll)
            return render_template('add_student.html', error_message=error_message)

    return render_template('add_student.html')

@app.route('/search_student', methods=['GET', 'POST'])
def search_student():
    if request.method == 'POST':
        search_term = request.form['search_term']
        menu2 = request.form['menu2']

        if menu2 == '1':
            mycur.execute("SELECT * FROM student_tb WHERE sroll = %s", (search_term,))
        elif menu2 == '2':
            mycur.execute("SELECT * FROM student_tb WHERE sname = %s", (search_term,))
        elif menu2 == '3':
            mycur.execute("SELECT * FROM student_tb WHERE sdob = %s", (search_term,))
        elif menu2 == '4':
            mycur.execute("SELECT * FROM student_tb WHERE satt = 'P'")
        elif menu2 == '5':
            mycur.execute("SELECT * FROM student_tb WHERE satt = 'A'")

        result = mycur.fetchall()
        return render_template('search_student.html', result=result)

    return render_template('search_student.html')

@app.route('/view_records')
def view_records():
    mycur.execute("SELECT * FROM student_tb")
    result = mycur.fetchall()
    return render_template('view_records.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
