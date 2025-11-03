import sqlite3

# Connect to SQLite database (creates file if not exists)
conn = sqlite3.connect("university_syllabus.db")
cur = conn.cursor()

# Drop old tables if any
tables = [
    "semesters", "subjects", "course_objectives", "course_outcomes",
    "course_units", "reference_books", "co_po_mapping"
]
for t in tables:
    cur.execute(f"DROP TABLE IF EXISTS {t}")

# Create tables
cur.execute("""
CREATE TABLE semesters (
    semester_id INTEGER PRIMARY KEY AUTOINCREMENT,
    semester_number INTEGER NOT NULL,
    semester_name TEXT NOT NULL,
    academic_year TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
""")

cur.execute("""
CREATE TABLE subjects (
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
);
""")

cur.execute("""
CREATE TABLE course_objectives (
    objective_id INTEGER PRIMARY KEY AUTOINCREMENT,
    subject_id INTEGER,
    objective_number INTEGER,
    objective_description TEXT NOT NULL,
    FOREIGN KEY (subject_id) REFERENCES subjects(subject_id)
);
""")

cur.execute("""
CREATE TABLE course_outcomes (
    outcome_id INTEGER PRIMARY KEY AUTOINCREMENT,
    subject_id INTEGER,
    outcome_number INTEGER,
    outcome_description TEXT NOT NULL,
    FOREIGN KEY (subject_id) REFERENCES subjects(subject_id)
);
""")

cur.execute("""
CREATE TABLE course_units (
    unit_id INTEGER PRIMARY KEY AUTOINCREMENT,
    subject_id INTEGER,
    unit_number INTEGER,
    unit_title TEXT NOT NULL,
    teaching_hours INTEGER,
    tutorial_hours INTEGER,
    unit_content TEXT,
    FOREIGN KEY (subject_id) REFERENCES subjects(subject_id)
);
""")

cur.execute("""
CREATE TABLE reference_books (
    book_id INTEGER PRIMARY KEY AUTOINCREMENT,
    subject_id INTEGER,
    book_type TEXT CHECK(book_type IN ('text','reference')),
    book_number INTEGER,
    book_details TEXT NOT NULL,
    FOREIGN KEY (subject_id) REFERENCES subjects(subject_id)
);
""")

cur.execute("""
CREATE TABLE co_po_mapping (
    mapping_id INTEGER PRIMARY KEY AUTOINCREMENT,
    subject_id INTEGER,
    course_outcome TEXT,
    po1 INTEGER, po2 INTEGER, po3 INTEGER, po4 INTEGER, po5 INTEGER, po6 INTEGER, po7 INTEGER,
    po8 INTEGER, po9 INTEGER, po10 INTEGER, po11 INTEGER, po12 INTEGER,
    pso1 INTEGER, pso2 INTEGER, pso3 INTEGER,
    FOREIGN KEY (subject_id) REFERENCES subjects(subject_id)
);
""")

# Insert semester
cur.execute("""
INSERT INTO semesters (semester_number, semester_name, academic_year)
VALUES (5, 'Fifth Semester', '2024-2025');
""")
semester_5 = cur.lastrowid

# Insert subjects
subjects_data = [
    (semester_5, '22UIS503C', 'Web Programming', 3, 2, 0, 2, 4, 50, 50, '2L-0T-2P'),
    (semester_5, '22UIS003E', 'Introduction to Artificial Intelligence', 3, 3, 0, 0, 3, 50, 50, '3L-0T-0P'),
    (semester_5, '22UIS501C', 'Software Engineering', 3, 3, 0, 0, 3, 50, 50, '3L-0T-0P'),
    (semester_5, '22UIS502C', 'Computer Networks (Integrated)', 3, 2, 0, 2, 4, 50, 50, '2L-0T-2P')
]
cur.executemany("""
INSERT INTO subjects (
    semester_id, subject_code, subject_title, credits, lecture_hours,
    tutorial_hours, practical_hours, total_contact_hours, cie_marks, see_marks, ltp_structure
) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
""", subjects_data)

# Get subject IDs
cur.execute("SELECT subject_id FROM subjects WHERE subject_code = '22UIS503C'")
web_programming = cur.fetchone()[0]

# Course Objectives
course_objectives_data = [
    (web_programming, 1, 'Understand the principles of World Wide Web and also to create an effective web page.'),
    (web_programming, 2, 'Use CSS to implement a variety of presentation effects in XHTML documents.'),
    (web_programming, 3, 'Develop basic programming skills using JavaScript.'),
    (web_programming, 4, 'Implement interactive and dynamic web pages using XHTML, CSS and JavaScript.'),
    (web_programming, 5, 'Understand how server-side programming works on the web using PHP technology and design responsive web pages using PHP.')
]
cur.executemany("""
INSERT INTO course_objectives (subject_id, objective_number, objective_description)
VALUES (?, ?, ?);
""", course_objectives_data)

# Course Outcomes
course_outcomes_data = [
    (web_programming, 1, 'Develop web pages using technologies like XHTML and CSS.'),
    (web_programming, 2, 'Develop JavaScript scripts for event handling.'),
    (web_programming, 3, 'Build dynamic documents using JavaScript and XHTML.'),
    (web_programming, 4, 'Implement web pages using PHP and MySQL.')
]
cur.executemany("""
INSERT INTO course_outcomes (subject_id, outcome_number, outcome_description)
VALUES (?, ?, ?);
""", course_outcomes_data)

# Course Units
course_units_data = [
    (web_programming, 1, 'FUNDAMENTALS OF WEB, XHTML', 7, 0,
     'Internet, HTTP request and HTTP response phase, MIME, The Web Programmers Toolbox. XHTML basics, syntax, tags, CSS styles.'),
    (web_programming, 2, 'Basics of JavaScript', 7, 0,
     'JavaScript syntax, arrays, DOM, events, event handling for buttons and forms.'),
    (web_programming, 3, 'Dynamic Documents with JavaScript', 6, 0,
     'Positioning elements, moving elements, dynamic contents, dragging & dropping.'),
    (web_programming, 4, 'Introduction to PHP', 6, 0,
     'PHP basics, syntax, arrays, functions, form handling, cookies, MySQL connectivity.')
]
cur.executemany("""
INSERT INTO course_units (subject_id, unit_number, unit_title, teaching_hours, tutorial_hours, unit_content)
VALUES (?, ?, ?, ?, ?, ?);
""", course_units_data)

# Reference Books
reference_books_data = [
    (web_programming, 'text', 1, 'Programming the World Wide Web - Robert W. Sebesta, 4th Edition, Pearson Education, 2008.'),
    (web_programming, 'reference', 1, 'Internet & World Wide Web How to program - M. Deitel, P.J.Deitel, A. B. Goldberg, 3rd Edition, Pearson Education / PHI, 2004.'),
    (web_programming, 'reference', 2, 'Web Programming Building Internet Applications - Chris Bates, 3rd Edition, Wiley India, 2006.'),
    (web_programming, 'reference', 3, 'The Web Warrior Guide to Web Programming - Xue Bai et al, Thomson, 2003.'),
    (web_programming, 'reference', 4, 'M.Srinivasan: Web Technology Theory and Practice, Pearson Education, 2012.'),
    (web_programming, 'reference', 5, 'Jeffrey.C.Jackson: Web Technologies - A Computer Science Perspective, Pearson Education, 2012.')
]
cur.executemany("""
INSERT INTO reference_books (subject_id, book_type, book_number, book_details)
VALUES (?, ?, ?, ?);
""", reference_books_data)

# CO-PO Mapping
co_po_mapping_data = [
    (web_programming, 'CO1', 3, 2, 3, None, 1, None, None, None, None, None, None, 1, 1, 2, 1),
    (web_programming, 'CO2', 3, 2, 3, None, 1, None, None, None, None, None, None, 1, 1, 2, 1),
    (web_programming, 'CO3', 3, 2, 3, None, 1, None, None, None, None, None, None, 1, 1, 2, 1),
    (web_programming, 'CO4', 3, 2, 3, None, 1, None, None, None, None, None, None, 1, 1, 2, 1)
]
cur.executemany("""
INSERT INTO co_po_mapping (
    subject_id, course_outcome, po1, po2, po3, po4, po5, po6, po7, po8, po9, po10, po11, po12, pso1, pso2, pso3
) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
""", co_po_mapping_data)

# Commit and close
conn.commit()
conn.close()

print("✅ SQLite database 'university_syllabus.db' created successfully.")
