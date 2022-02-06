import os
from flask import Flask, request, render_template, redirect
from flask_sqlalchemy import SQLAlchemy

current_dir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)

db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.join(current_dir, 'database.sqlite3')

class student(db.Model):
    student_id = db.Column(db.Integer, primary_key = True)
    roll_number = db.Column(db.String, unique = True, nullable = False)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String)
    enrolls = db.relationship("enrollments")

class course(db.Model):
    course_id = db.Column(db.Integer, primary_key = True)
    course_code = db.Column(db.String, unique = True, nullable = False)
    course_name = db.Column(db.String, nullable = False)
    course_description = db.Column(db.String)
    enrolled_course = db.relationship("enrollments")

class enrollments(db.Model):
    enrollment_id = db.Column(db.Integer, primary_key=True)
    estudent_id = db.Column(db.Integer, db.ForeignKey("student.student_id"), nullable=False)
    ecourse_id = db.Column(db.Integer, db.ForeignKey("course.course_id"), nullable=False)


@app.route('/')
def index():

    all_list = student.query.all()
    return render_template("index.html", all_list = all_list)

@app.route('/student/create', methods=['POST', 'GET'])
def student_create():
    if request.method == 'POST':
        # Retrieving Data from form
        roll_no = request.form['roll']
        f_name = request.form['f_name']
        l_name = request.form['l_name']
        course_s = request.form.getlist("courses")

        # checking if the data already exists in the db
        # if data already exists, return already-exists.html page, else move to pushing data into db
        checker = student.query.filter_by(roll_number = roll_no).first()
        if checker != None:
            return render_template("already-exists.html")

        #inserting in student table
        s = student(roll_number = roll_no, first_name = f_name, last_name = l_name)
        db.session.add(s)
        db.session.commit()

        course_dict = {
            "course_1": "MAD I",
            "course_2": "DBMS",
            "course_3": "PDSA",
            "course_4": "BDM"
        }
        
        course_list = []
        for cs in course_s:
            course_list.append(course_dict[cs])
            c = course.query.filter_by(course_name = course_dict[cs]).first()
            e = enrollments(estudent_id = s.student_id, ecourse_id = c.course_id)
            db.session.add(e)
        
        db.session.commit()
        return redirect('/')
    
    return render_template("add_student.html")



@app.route('/student/<int:student_id>')
def student_r(student_id):
    student_details = student.query.get(student_id)
    li = []
    for i in student_details.enrolls:
        li.append(i.ecourse_id)
    
    courses_details = []
    for x in li:
        data = course.query.get(x)
        courses_details.append(data)
        
    return render_template("student.html", data = student_details, my_courses = courses_details)


@app.route('/student/<int:student_id>/update', methods = ['GET', 'POST'])
def update_student(student_id):
    if request.method == 'POST':
        cur_data = student.query.get(student_id)

        # Retrieving Data from form
        f_name = request.form['f_name']
        l_name = request.form['l_name']
        course_s = request.form.getlist("courses")
        cur_data.first_name = f_name
        cur_data.last_name = l_name

        course_dict = {
            "course_1": "MAD I",
            "course_2": "DBMS",
            "course_3": "PDSA",
            "course_4": "BDM"
        }

        enrollments.query.filter_by(estudent_id = student_id).delete()
        db.session.commit()
        course_list = []
        for cs in course_s:
            course_list.append(course_dict[cs])
            c = course.query.filter_by(course_name = course_dict[cs]).first()
            e = enrollments(estudent_id = student_id, ecourse_id = c.course_id)
            db.session.add(e)


        db.session.commit()
        return redirect('/')

    cur_data = student.query.get(student_id)

    return render_template("update-form.html", cur_data = cur_data)

@app.route('/student/<int:student_id>/delete')
def delete_student(student_id):
    student.query.filter_by(student_id = student_id).delete()
    enrollments.query.filter_by(estudent_id = student_id).delete()
    db.session.commit()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
