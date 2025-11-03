import sqlite3
import os

# ✅ Database connection
def get_connection():
    db_path = os.path.join(os.path.dirname(__file__), '..', 'database', 'department.db')
    return sqlite3.connect(db_path)

# ✅ Get subjects by semester
def get_subjects_by_semester(semester_number):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        query = """
            SELECT subject_code, subject_title, credits, ltp_structure
            FROM subjects s
            JOIN semesters sem ON s.semester_id = sem.semester_id
            WHERE sem.semester_number = ?
        """
        cursor.execute(query, (semester_number,))
        data = cursor.fetchall()
        # Convert to dictionary format for consistency
        columns = [desc[0] for desc in cursor.description]
        result = [dict(zip(columns, row)) for row in data]
        return result
    except Exception as e:
        print(f"Error getting subjects by semester: {e}")
        return []
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()


# ✅ Get syllabus by semester (subjects + outcomes + books)
def get_syllabus_by_semester(semester_number):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        query = """
            SELECT s.subject_code, s.subject_title, s.credits, s.ltp_structure,
                   co.outcome_number, co.outcome_description,
                   rb.book_number, rb.book_details
            FROM subjects s
            LEFT JOIN course_outcomes co ON s.subject_id = co.subject_id
            LEFT JOIN reference_books rb ON s.subject_id = rb.subject_id
            JOIN semesters sem ON s.semester_id = sem.semester_id
            WHERE sem.semester_number = ?
            ORDER BY s.subject_code, co.outcome_number, rb.book_number
        """
        cursor.execute(query, (semester_number,))
        data = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        result = [dict(zip(columns, row)) for row in data]
        return result
    except Exception as e:
        print(f"Error getting syllabus by semester: {e}")
        return []
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()


# ✅ Get course outcomes by subject title
def get_course_outcomes(subject_title):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        query = """
            SELECT co.outcome_number, co.outcome_description
            FROM course_outcomes co
            JOIN subjects s ON co.subject_id = s.subject_id
            WHERE s.subject_title LIKE ?
            ORDER BY co.outcome_number
        """
        cursor.execute(query, (f"%{subject_title}%",))
        data = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        result = [dict(zip(columns, row)) for row in data]
        return result
    except Exception as e:
        print(f"Error getting course outcomes: {e}")
        return []
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()


# ✅ Get reference books by subject title
def get_reference_books(subject_title):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        query = """
            SELECT book_number, book_details
            FROM reference_books r
            JOIN subjects s ON r.subject_id = s.subject_id
            WHERE s.subject_title LIKE ?
            ORDER BY book_number
        """
        cursor.execute(query, (f"%{subject_title}%",))
        data = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        result = [dict(zip(columns, row)) for row in data]
        return result
    except Exception as e:
        print(f"Error getting reference books: {e}")
        return []
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()


# ✅ Get HoD information (from Faculty table)
def get_hod_info(dept_code):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        query = """
            SELECT name, designation
            FROM Faculty
            WHERE designation LIKE '%Head%'
        """
        cursor.execute(query)
        data = cursor.fetchone()
        if data:
            columns = [desc[0] for desc in cursor.description]
            return dict(zip(columns, data))["name"]
        return None
    except Exception as e:
        print(f"Error getting HoD info: {e}")
        return None
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()


# ✅ Get all faculty members
def get_faculty_list():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        query = """
            SELECT name, designation, specialization
            FROM Faculty
            ORDER BY designation
        """
        cursor.execute(query)
        data = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        result = [dict(zip(columns, row)) for row in data]
        return result
    except Exception as e:
        print(f"Error getting faculty list: {e}")
        return []
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()


# ✅ Get all supporting staff
def get_supporting_staff():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        query = """
            SELECT name, designation
            FROM SupportingStaff
            ORDER BY designation
        """
        cursor.execute(query)
        data = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        result = [dict(zip(columns, row)) for row in data]
        return result
    except Exception as e:
        print(f"Error getting supporting staff: {e}")
        return []
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()


# ✅ Get lab information
def get_lab_info():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        query = """
            SELECT lab_no, lab_name, incharge
            FROM LabInfrastructure
            ORDER BY lab_no
        """
        cursor.execute(query)
        data = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        result = [dict(zip(columns, row)) for row in data]
        return result
    except Exception as e:
        print(f"Error getting lab info: {e}")
        return []
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()


def get_faculty_by_specialization(keyword):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        query = """
            SELECT name, designation, specialization
            FROM Faculty
            WHERE specialization LIKE ?
        """
        cursor.execute(query, (f"%{keyword}%",))
        data = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        result = [dict(zip(columns, row)) for row in data]
        return result
    except Exception as e:
        print(f"Error getting faculty by specialization: {e}")
        return []
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()


def get_faculty_by_name(name):
    """
    Fetch faculty details (designation, specialization, contact info)
    based on a partial name match.
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        query = """
            SELECT name, designation, specialization, email, phone
            FROM Faculty
            WHERE name LIKE ?
        """
        cursor.execute(query, (f"%{name}%",))
        data = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        result = [dict(zip(columns, row)) for row in data]
        return result
    except Exception as e:
        print(f"Error getting faculty by name: {e}")
        return []
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()
