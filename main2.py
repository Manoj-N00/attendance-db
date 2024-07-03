import mysql.connector as msql
from datetime import date
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib

# Database connection
con = msql.connect(host='localhost', user='root', passwd='ojus2004', database='attendance_db', charset='utf8')

# Function to add a student
def add_student():
    first_name = input('Enter first name: ')
    last_name = input('Enter last name: ')
    date_of_birth = input('Enter date of birth (YYYY-MM-DD): ')
    grade_level = input('Enter grade level: ')
    school_id = int(input('Enter school ID: '))

    qry = 'INSERT INTO students (first_name, last_name, date_of_birth, grade_level, school_id) VALUES (%s, %s, %s, %s, %s)'
    val = (first_name, last_name, date_of_birth, grade_level, school_id)
    mcursor = con.cursor()
    mcursor.execute(qry, val)
    con.commit()
    print('Student added successfully.')
    main()

# Function to add a teacher
def add_teacher():
    first_name = input('Enter first name: ')
    last_name = input('Enter last name: ')
    subject = input('Enter subject: ')
    print('Available school IDs:')
    list_school_ids()
    school_id = int(input('Enter school ID: '))

    qry = 'INSERT INTO teachers (first_name, last_name, subject, school_id) VALUES (%s, %s, %s, %s)'
    val = (first_name, last_name, subject, school_id)
    mcursor = con.cursor()
    mcursor.execute(qry, val)
    con.commit()
    print('Teacher added successfully.')
    main()

# Function to list existing school IDs
def list_school_ids():
    qry = 'SELECT school_id, school_name FROM schools'
    mcursor = con.cursor()
    mcursor.execute(qry)
    schools = mcursor.fetchall()
    for school in schools:
        print(f"School ID: {school[0]}, School Name: {school[1]}")

# Function to add a counselor
def add_counselor():
    first_name = input('Enter first name: ')
    last_name = input('Enter last name: ')
    contact_info = input('Enter contact info: ')
    print('Available school IDs:')
    list_school_ids()
    school_id = int(input('Enter school ID: '))

    qry = 'INSERT INTO counselors (first_name, last_name, contact_info, school_id) VALUES (%s, %s, %s, %s)'
    val = (first_name, last_name, contact_info, school_id)
    mcursor = con.cursor()
    mcursor.execute(qry, val)
    con.commit()
    print('Counselor added successfully.')
    main()

# Function to add a school
def add_school():
    school_name = input('Enter school name: ')
    school_address = input('Enter school address: ')

    qry = 'INSERT INTO schools (school_name, address) VALUES (%s, %s)'
    val = (school_name, school_address)
    mcursor = con.cursor()
    mcursor.execute(qry, val)
    con.commit()
    print('School added successfully.')
    main()

# Function to add a class
def add_class():
    class_name = input('Enter class name: ')
    print('Available teacher IDs:')
    list_teacher_ids()
    teacher_id = int(input('Enter teacher ID: '))
    print('Available school IDs:')
    list_school_ids()
    school_id = int(input('Enter school ID: '))

    qry = 'INSERT INTO classes (class_name, teacher_id, school_id) VALUES (%s, %s, %s)'
    val = (class_name, teacher_id, school_id)
    mcursor = con.cursor()
    mcursor.execute(qry, val)
    con.commit()
    print('Class added successfully.')
    main()

# Function to list existing teacher IDs
def list_teacher_ids():
    qry = 'SELECT teacher_id, first_name, last_name FROM teachers'
    mcursor = con.cursor()
    mcursor.execute(qry)
    teachers = mcursor.fetchall()
    for teacher in teachers:
        print(f"Teacher ID: {teacher[0]}, Name: {teacher[1]} {teacher[2]}")

# Function to add attendance
def add_attendance():
    print('Available student IDs:')
    list_student_ids()
    student_id = int(input('Enter student ID: '))
    print('Available class IDs:')
    list_class_ids()
    class_id = int(input('Enter class ID: '))
    attendance_date = input('Enter date (YYYY-MM-DD): ')
    status = input('Enter status (Present/Absent/Late/Excused): ')

    qry = 'INSERT INTO attendance (student_id, class_id, attendance_date, status) VALUES (%s, %s, %s, %s)'
    val = (student_id, class_id, attendance_date, status)
    mcursor = con.cursor()
    mcursor.execute(qry, val)
    con.commit()

    if status.lower() == 'absent':
        send_absence_alert(student_id)

    print('Attendance record added successfully.')
    main()

# Function to list existing student IDs
def list_student_ids():
    qry = 'SELECT student_id, first_name, last_name FROM students'
    mcursor = con.cursor()
    mcursor.execute(qry)
    students = mcursor.fetchall()
    for student in students:
        print(f"Student ID: {student[0]}, Name: {student[1]} {student[2]}")

# Function to list existing class IDs
def list_class_ids():
    qry = 'SELECT class_id, class_name FROM classes'
    mcursor = con.cursor()
    mcursor.execute(qry)
    classes = mcursor.fetchall()
    for cls in classes:
        print(f"Class ID: {cls[0]}, Class Name: {cls[1]}")

# Function to send absence alert email
def send_absence_alert(student_id):
    qry = '''
        SELECT guardians.guardian_email, guardians.parent_type, students.first_name, students.last_name
        FROM guardians 
        JOIN students ON guardians.student_id = students.student_id 
        WHERE students.student_id = %s
    '''
    mcursor = con.cursor()
    mcursor.execute(qry, (student_id,))
    results = mcursor.fetchall()

    for result in results:
        guardian_email, parent_type, first_name, last_name = result
        send_email(
            guardian_email,
            'Absence Alert Notification',
            f'Dear {parent_type},\n\nYour child, {first_name} {last_name}, was marked absent today.\n\nRegards,\nSchool Administration'
        )
        print(f'Absence alert email sent to {guardian_email}')

# Function to send email
def send_email(to_email, subject, body):
    from_email = 'xyzxyza6969@gmail.com'
    from_password = 'kekh xfij ktye zhpb'

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(from_email, from_password)
    server.sendmail(from_email, to_email, msg.as_string())
    server.quit()

# Main menu
def main():
    print('Attendance Management System')
    print('1. Add Student')
    print('2. Add Teacher')
    print('3. Add Counselor')
    print('4. Add School')
    print('5. Add Class')
    print('6. Add Attendance')
    print('7. Exit')

    choice = int(input('Enter your choice: '))
    if choice == 1:
        add_student()
    elif choice == 2:
        add_teacher()
    elif choice == 3:
        add_counselor()
    elif choice == 4:
        add_school()
    elif choice == 5:
        add_class()
    elif choice == 6:
        add_attendance()
    elif choice == 7:
        print('Exiting...')
        con.close()
        exit()
    else:
        print('Invalid choice. Please try again.')
        main()

if __name__ == '__main__':
    main()
