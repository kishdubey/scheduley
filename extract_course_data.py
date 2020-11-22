"""
extracting courses data from an image of a course schedule
"""
import cv2
import pytesseract

class Course:
    def __init__(self, title, type, start_time, end_time, location, day):
        self.title = title
        self.type = type
        self.start_time = start_time
        self.end_time = end_time
        self.location = location
        self.day = day

    def __repr__(self):
        return f"""
                Title: {self.title}
                Type: {self.type}
                Time: {self.start_time} - {self.end_time}
                Location: {self.location}
                Day: {self.day}\n"""

def get_image(path):
    """
    (string) -> numpy.ndarray
    returns image for given path
    """
    return cv2.imread(path)

def extract_information(image):
    """
    (numpy.ndarray) -> list
    returns list of text extracted from given image
    """
    extracted_info = pytesseract.image_to_string(image).strip().replace("\n\n", "\n")
    extracted_info_list = list(extracted_info.split("\n"))

    for item in extracted_info_list:
        if item == " ":
            extracted_info_list.remove(item)

    return extracted_info_list

def helper_capitalize(text):
    """
    (string) -> string
    proprely capitalize course titles
    """
    capitalized = ''
    for char in text:
        if char.isalpha():
            capitalized += char.upper()
        else:
            capitalized += char

    return capitalized

def get_courses(info_list):
    """
    (list) -> list
    returns list of courses of type Course from given list of raw extracted text
    """
    WEEKDAYS = set(["monday", "tuesday", "wednesday", "thursday", "friday"])
    courses = []
    day = 'Monday'
    i = 0

    while i < len(info_list):
        current = info_list[i]
        if current.lower() in WEEKDAYS:
            day = current

            course_title = info_list[i+2].strip()
            course_type = info_list[i+3]
            time = info_list[i+4]
            course_start_time = time[:6]
            course_end_time = time[8:]
            course_location = info_list[i+5].replace("Location: ", "")

            this_course = Course(helper_capitalize(course_title), course_type, course_start_time, course_end_time, course_location, day)
            courses.append(this_course)
            i += 6

        else:
            course_title = info_list[i].strip()
            course_type = info_list[i+1]
            time = info_list[i+2]
            course_start_time = time[:6]
            course_end_time = time[8:]
            course_location = info_list[i+3].replace("Location: ", "")

            this_course = Course(helper_capitalize(course_title), course_type, course_start_time, course_end_time, course_location, day)
            courses.append(this_course)
            i += 4

    return courses

def get_schedule(path):
    """
    (string) -> list
    returns list of courses given the path to an image
    """
    img = get_image(path)
    info_list = extract_information(img)
    courses = get_courses(info_list)

    return courses
