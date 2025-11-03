import sqlite3
import os

# Create database
db_path = os.path.join('database', 'department.db')
os.makedirs('database', exist_ok=True)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Create tables
cursor.execute('''
CREATE TABLE IF NOT EXISTS semesters (
    semester_id INTEGER PRIMARY KEY AUTOINCREMENT,
    semester_number INTEGER NOT NULL,
    semester_name TEXT,
    academic_year TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS subjects (
    subject_id INTEGER PRIMARY KEY AUTOINCREMENT,
    semester_id INTEGER,
    subject_code TEXT NOT NULL UNIQUE,
    subject_title TEXT NOT NULL,
    credits INTEGER NOT NULL,
    lecture_hours INTEGER,
    tutorial_hours INTEGER,
    practical_hours INTEGER,
    total_contact_hours INTEGER,
    cie_marks INTEGER,
    see_marks INTEGER,
    ltp_structure TEXT,
    FOREIGN KEY (semester_id) REFERENCES semesters(semester_id)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS course_objectives (
    objective_id INTEGER PRIMARY KEY AUTOINCREMENT,
    subject_id INTEGER,
    objective_number INTEGER,
    objective_description TEXT NOT NULL,
    FOREIGN KEY (subject_id) REFERENCES subjects(subject_id)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS course_outcomes (
    outcome_id INTEGER PRIMARY KEY AUTOINCREMENT,
    subject_id INTEGER,
    outcome_number INTEGER,
    outcome_description TEXT NOT NULL,
    FOREIGN KEY (subject_id) REFERENCES subjects(subject_id)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS course_units (
    unit_id INTEGER PRIMARY KEY AUTOINCREMENT,
    subject_id INTEGER,
    unit_number INTEGER,
    unit_title TEXT NOT NULL,
    teaching_hours INTEGER,
    tutorial_hours INTEGER,
    unit_content TEXT,
    FOREIGN KEY (subject_id) REFERENCES subjects(subject_id)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS reference_books (
    book_id INTEGER PRIMARY KEY AUTOINCREMENT,
    subject_id INTEGER,
    book_type TEXT CHECK(book_type IN ('text', 'reference')),
    book_number INTEGER,
    book_details TEXT NOT NULL,
    FOREIGN KEY (subject_id) REFERENCES subjects(subject_id)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS co_po_mapping (
    mapping_id INTEGER PRIMARY KEY AUTOINCREMENT,
    subject_id INTEGER,
    course_outcome TEXT,
    po1 INTEGER, po2 INTEGER, po3 INTEGER, po4 INTEGER, po5 INTEGER, po6 INTEGER, po7 INTEGER, po8 INTEGER, po9 INTEGER, po10 INTEGER, po11 INTEGER, po12 INTEGER,
    pso1 INTEGER, pso2 INTEGER, pso3 INTEGER,
    FOREIGN KEY (subject_id) REFERENCES subjects(subject_id)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Faculty (
    faculty_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    designation TEXT NOT NULL,
    qualification TEXT,
    specialization TEXT,
    email TEXT,
    phone_no TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS SupportingStaff (
    staff_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    designation TEXT NOT NULL,
    phone_no TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS LabInfrastructure (
    lab_id INTEGER PRIMARY KEY AUTOINCREMENT,
    lab_no TEXT NOT NULL,
    lab_name TEXT NOT NULL,
    incharge TEXT NOT NULL
)
''')

# Insert sample data
# Semesters
cursor.execute("INSERT INTO semesters (semester_number) VALUES (1), (2), (3), (4), (5), (6), (7), (8)")

# Subjects for semester 5
cursor.execute("INSERT INTO subjects (subject_code, subject_title, credits, ltp_structure, semester_id) VALUES ('22UIS503C', 'Web Programming', 3, '2L-0T-2P', 5)")
cursor.execute("INSERT INTO subjects (subject_code, subject_title, credits, ltp_structure, semester_id) VALUES ('22UIS003E', 'Introduction to Artificial Intelligence', 3, '3L-0T-0P', 5)")
cursor.execute("INSERT INTO subjects (subject_code, subject_title, credits, ltp_structure, semester_id) VALUES ('22UIS501C', 'Software Engineering', 3, '3L-0T-0P', 5)")
cursor.execute("INSERT INTO subjects (subject_code, subject_title, credits, ltp_structure, semester_id) VALUES ('22UIS502C', 'Computer Networks (Integrated)', 3, '2L-0T-2P', 5)")

# Course outcomes for Web Programming
cursor.execute("INSERT INTO course_outcomes (subject_id, outcome_number, outcome_description) VALUES (1, 1, 'Develop web pages using technologies like XHTML and CSS.')")
cursor.execute("INSERT INTO course_outcomes (subject_id, outcome_number, outcome_description) VALUES (1, 2, 'Develop JavaScript scripts for event handling.')")
cursor.execute("INSERT INTO course_outcomes (subject_id, outcome_number, outcome_description) VALUES (1, 3, 'Build dynamic documents using JavaScript and XHTML.')")
cursor.execute("INSERT INTO course_outcomes (subject_id, outcome_number, outcome_description) VALUES (1, 4, 'Implement web pages using PHP and MySQL.')")

# Reference books for Web Programming
cursor.execute("INSERT INTO reference_books (subject_id, book_number, book_details) VALUES (1, 1, 'Programming the World Wide Web - Robert W. Sebesta, 4th Edition, Pearson Education, 2008.')")
cursor.execute("INSERT INTO reference_books (subject_id, book_number, book_details) VALUES (1, 2, 'Internet & World Wide Web How to program - M. Deitel, P.J.Deitel, A. B. Goldberg, 3rd Edition, Pearson Education / PHI, 2004.')")
cursor.execute("INSERT INTO reference_books (subject_id, book_number, book_details) VALUES (1, 3, 'Web Programming Building Internet Applications - Chris Bates,3rd Edition, Wiley India, 2006.')")

# Faculty
cursor.execute("INSERT INTO Faculty (name, designation, specialization, email, phone) VALUES ('Dr.S.P.Bangarashetti', 'Professor and Head Of Department', 'Image Processing', 'spbis@becbgk.edu', '+91 9448215955')")
cursor.execute("INSERT INTO Faculty (name, designation, specialization, email, phone) VALUES ('Dr.S.R.Patil', 'Professor', 'Image Processing', 'srpis@becbgk.edu', '+91 9449534202')")
cursor.execute("INSERT INTO Faculty (name, designation, specialization, email, phone) VALUES ('Prof.P.V.Kulakarni', 'Associate Professor', 'Database Systems', 'pvkis@becbgk.edu', '+91 9448939735')")
cursor.execute("INSERT INTO Faculty (name, designation, specialization, email, phone) VALUES ('Smt.P.Puranik', 'Associate Professor', 'Web Technology', 'pspis@becbg.edu', '+91 9449724440')")

# Supporting Staff
cursor.execute("INSERT INTO SupportingStaff (name, designation) VALUES ('Shri.Kupendrakumar.H.B', 'Foreman')")
cursor.execute("INSERT INTO SupportingStaff (name, designation) VALUES ('Shri.V.S.Nashi', 'Asst.Instructor')")

# Labs
cursor.execute("INSERT INTO LabInfrastructure (lab_no, lab_name, incharge) VALUES ('ISE LAB NO-01', 'Tim Berners-Lee Lab', 'Shri.M.V.Gennur')")
cursor.execute("INSERT INTO LabInfrastructure (lab_no, lab_name, incharge) VALUES ('ISE LAB NO-02', 'Abraham Silberschatz Lab', 'MR.Patil')")

conn.commit()
conn.close()
print("Database created and populated successfully.")
