import nltk
from nltk.tokenize import word_tokenize
import re

nltk.download('punkt')

def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    tokens = word_tokenize(text)
    return tokens

def detect_intent(text):
    text = text.lower()
    if any(word in text for word in ["hi", "hello", "hey", "greetings", "good morning", "good afternoon", "good evening"]):
        return "greeting"
    elif any(word in text for word in ["help", "what can you do", "commands", "options"]):
        return "help"
    elif "hod" in text:
        return "hod_info"
    elif "faculty" in text:
        return "faculty_list"
    elif "lab" in text:
        return "lab_info"
    elif "syllabus" in text:
        return "syllabus"
    elif "subject" in text or "semester" in text:
        return "semester_subjects"
    elif "outcome" in text or "co" in text:
        return "course_outcomes"
    elif "book" in text or "reference" in text:
        return "reference_books"
    else:
        return "unknown"
