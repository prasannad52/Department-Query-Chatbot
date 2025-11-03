from chatbot.db_helper import (
    get_subjects_by_semester,
    get_syllabus_by_semester,
    get_course_outcomes,
    get_reference_books,
    get_hod_info,
    get_faculty_list,
    get_faculty_by_specialization,
    get_faculty_by_name,
    get_supporting_staff,
    get_lab_info
)

def generate_response(intent, tokens):
    """
    Smart chatbot response generator that handles subjects, syllabus, faculty, labs, and staff info.
    """

    # --- 0️⃣ Greeting ---
    if intent == "greeting":
        return "👋 Hello! I'm Nexus AI, your department query assistant. How can I help you today?"

    # --- 0.5️⃣ Help ---
    elif intent == "help":
        return (
            "🤖 I'm Nexus AI, here to help with department queries!\n\n"
            "You can ask me about:\n"
            "• Semester subjects (e.g., 'Show 5th semester subjects')\n"
            "• Syllabus details (e.g., 'Show 5th semester syllabus')\n"
            "• Course outcomes (e.g., 'Web Programming outcomes')\n"
            "• Reference books (e.g., 'AI reference books')\n"
            "• Faculty info (e.g., 'Who is the HOD of ISE?', 'List Assistant Professors')\n"
            "• Lab details (e.g., 'Show lab details')\n"
            "• Supporting staff (e.g., 'List supporting staff')\n\n"
            "Just type your question!"
        )

    # --- 1️⃣ Semester Subjects ---
    if intent == "semester_subjects":
        for t in tokens:
            if t.isdigit():
                subjects = get_subjects_by_semester(int(t))
                if subjects:
                    res = f"📚 Subjects in Semester {t}:\n\n"
                    for s in subjects:
                        res += f"• {s['subject_code']} - {s['subject_title']} ({s['credits']} Credits, {s['ltp_structure']})\n"
                    return res
        return "Please specify a semester (e.g., 'Show 5th semester subjects')."

    # --- 1.5️⃣ Syllabus ---
    elif intent == "syllabus":
        for t in tokens:
            if t.isdigit():
                syllabus_data = get_syllabus_by_semester(int(t))
                if syllabus_data:
                    res = f"📚 Syllabus for Semester {t}:\n\n"
                    current_subject = None
                    for item in syllabus_data:
                        if current_subject != item['subject_code']:
                            current_subject = item['subject_code']
                            res += f"**{item['subject_code']}: {item['subject_title']}**\n"
                            res += f"Credits: {item['credits']}, LTP: {item['ltp_structure']}\n"
                            if item['outcome_number']:
                                res += "Course Outcomes:\n"
                        if item['outcome_number']:
                            res += f"  CO{item['outcome_number']}: {item['outcome_description']}\n"
                        if item['book_number']:
                            res += f"Reference Book {item['book_number']}: {item['book_details']}\n"
                    return res
        return "Please specify a semester (e.g., 'Show 5th semester syllabus')."

    # --- 2️⃣ Course Outcomes ---
    elif intent == "course_outcomes":
        for t in tokens:
            outcomes = get_course_outcomes(t)
            if outcomes:
                res = f"🎯 Course Outcomes for {t.title()}:\n\n"
                for o in outcomes:
                    res += f"CO{o['outcome_number']}: {o['outcome_description']}\n"
                return res
        return "Please specify a valid subject name (e.g., 'Web Programming outcomes')."

    # --- 3️⃣ Reference Books ---
    elif intent == "reference_books":
        for t in tokens:
            books = get_reference_books(t)
            if books:
                res = f"📖 Reference Books for {t.title()}:\n\n"
                for b in books:
                    res += f"{b['book_number']}. {b['book_details']}\n"
                return res
        return "Please specify a valid subject (e.g., 'Show AI reference books')."

    # --- 4️⃣ HoD Info ---
    elif intent == "hod_info":
        for t in tokens:
            if t.lower() in ["ise", "cse", "ece", "mech", "civil", "eee"]:
                hod = get_hod_info(t.upper())
                if hod:
                    return f"👨‍🏫 The Head of the {t.upper()} Department is {hod}."
                else:
                    return f"Sorry, I couldn’t find the HoD for {t.upper()} Department."
        return "Please specify the department name (e.g., 'Who is the HOD of ISE?')."

    # --- 5️⃣ Faculty Info ---
    elif intent == "faculty_list":
        for t in tokens:
            if t.lower() in ["professor", "assistant", "associate"]:
                faculty = get_faculty_list(t)
                if faculty:
                    res = f"👩‍🏫 Faculty with designation '{t.title()}':\n\n"
                    for f in faculty:
                        res += f"• {f['name']} ({f['specialization']})\n"
                    return res
        faculty = get_faculty_list()
        if faculty:
            res = "👨‍🏫 All Faculty Members:\n\n"
            for f in faculty:
                res += f"• {f['name']} - {f['designation']} ({f['specialization']})\n"
            return res
        return "No faculty data found."

    # --- 6️⃣ Supporting Staff ---
    elif intent == "supporting_staff":
        staff = get_supporting_staff()
        if staff:
            res = "🧰 Supporting Staff:\n\n"
            for s in staff:
                res += f"• {s['name']} - {s['designation']}\n"
            return res
        return "No supporting staff records found."

    # --- 7️⃣ Lab Info ---
    elif intent == "lab_info":
        labs = get_lab_info()
        if labs:
            res = "💻 Lab Infrastructure:\n\n"
            for l in labs:
                res += f"• {l['lab_no']} - {l['lab_name']} (Incharge: {l['incharge']})\n"
            return res
        return "No lab information available."

    # --- 8️⃣ Faculty Search by Specialization ---
    elif intent == "faculty_specialization":
        for t in tokens:
            fac = get_faculty_by_specialization(t)
            if fac:
                res = f"👩‍🔬 Faculty specialized in '{t.title()}':\n\n"
                for f in fac:
                    res += f"• {f['name']} ({f['designation']})\n"
                return res
        return "Please specify a specialization (e.g., 'Faculty specialized in Networking')."

    # --- 9️⃣ Faculty Search by Name ---
    elif intent == "faculty_name":
        for t in tokens:
            fac = get_faculty_by_name(t)
            if fac:
                res = f"👨‍🏫 Faculty matching '{t.title()}':\n\n"
                for f in fac:
                    res += (
                        f"• {f['name']} - {f['designation']} ({f['specialization']})\n"
                        f"📧 {f['email']} | 📞 {f['phone_no']}\n\n"
                    )
                return res
        return "Please specify a faculty name (e.g., 'Details of Dr. Patil')."

    # --- 🔟 Default Response ---
    else:
        return (
            "🤖 I'm not sure what you mean. Try asking:\n"
            "• 'Show 5th semester subjects'\n"
            "• 'Who is the HOD of ISE?'\n"
            "• 'Faculty specialized in Image Processing'\n"
            "• 'List Assistant Professors'\n"
            "• 'Show lab details'\n"
        )
