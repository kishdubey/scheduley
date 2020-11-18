import cv2
import pytesseract

class Course:
    def __init__(self, title, type, start_time, end_time, location):
        self.title = title
        self.type = type
        self.start_time = start_time
        self.end_time = end_time
        self.location = location

    def __repr__(self):
        return f'Title: {self.title} \n\n Type: {self.type} \n\n Time: {self.start_time}-{self.end_time} \n\n Location: {self.location}'

image = cv2.imread('data/schedule.png')

extracted_info = pytesseract.image_to_string(image).strip().replace("\n\n", "\n")

extracted_info_list = list(extracted_info.split("\n"))

for item in extracted_info_list:
    if item == " ":
        extracted_info_list.remove(item)

weekdays = set(["monday", "tuesday", "wednesday", "thursday", "friday"])

courses = []

i = 0
while i < len(extracted_info_list):
    item = extracted_info_list[i]
    # if weekday
    if item.lower() in weekdays:
        print(item)
        courses.append("\n")

        course_title = extracted_info_list[i+2].strip()
        course_type = extracted_info_list[i+3]
        time = extracted_info_list[i+4]
        course_start_time = time[:7]
        course_end_time = time[9:]
        course_location = extracted_info_list[i+5].replace("Location: ", "")

        course = Course(course_title, course_type, course_start_time, course_end_time, course_location)
        courses.append(course)
        i += 6

    # else if next course of same day
    else:
        course_title = extracted_info_list[i].strip()
        course_type = extracted_info_list[i+1]
        time = extracted_info_list[i+2]
        course_start_time = time[:7]
        course_end_time = time[9:]
        course_location = extracted_info_list[i+3].replace("Location: ", "")

        course = Course(course_title, course_type, course_start_time, course_end_time, course_location)
        courses.append(course)
        i += 4

for course in courses:
    print(course)
