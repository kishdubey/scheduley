"""
generating ICS file calendar with course contents
"""
import cv2
import pytesseract
from icalendar import Calendar, Event, vText
import datetime
from datetime import time
import os
from os.path import join, dirname, realpath

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
    extracted_info_list = list(filter(lambda item: item.strip() != '', extracted_info_list))

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

ACADEMIC_TERMS = {"summer": "01/05 - 31/08", "fall": "01/09 - 31/12", "winter": "01/01 - 30/04"}
WEEKDAYS = {"monday": 0, "tuesday": 1, "wednesday": 2, "thursday": 3, "friday": 4}

def get_academic_term(academic_term):
    """
    (string) -> tuple
    returns the start and end dates of the given academic term
    """
    term = ACADEMIC_TERMS[academic_term]
    start = term[0:5]
    end = term[8:]

    return start, end

def next_weekday(d, weekday):
    """
    (datetime, string) -> datetime
    returns the first ocurrence of the given weekday after the initial datetime d
    """
    days_ahead = weekday - d.weekday()
    if days_ahead <= 0:
        days_ahead += 7
    return d + datetime.timedelta(days_ahead)

def create_event(course, academic_term, year):
    """
    (course, string) -> event
    returns an event created from the course contents, complying with the dates of the academic_term
    """
    event = Event()
    event.add('summary', f"{course.title} - {course.type}".strip().replace("  ", " "))
    event['location'] = vText(course.location)

    # Term Dates
    term_start, term_end = get_academic_term(academic_term.lower())
    term_start_date = datetime.date(year, int(term_start[3:]), int(term_start[0:2]))

    # Course Start Date
    course_start_date = next_weekday(term_start_date, WEEKDAYS[course.day.lower()])
    course_start_hour, course_start_minute = int(course.start_time[:2]), int(course.start_time[3:])
    course_start_time = time(course_start_hour, course_start_minute, 0)

    course_start_datetime = datetime.datetime.combine(course_start_date, course_start_time)
    event.add('dtstart', course_start_datetime)

    # Course End Time
    course_end_hour, course_end_minute = int(course.end_time[:2]), int(course.end_time[3:])
    course_end_time = time(course_end_hour, course_end_minute, 0)

    course_end_datetime = datetime.datetime.combine(course_start_date, course_end_time)
    event.add('dtend', course_end_datetime)

    # Course End Date
    course_last_date = datetime.date(year, int(term_end[3:]), int(term_end[0:2]))
    course_last_datetime = datetime.datetime.combine(course_last_date, course_end_time)

    # Add event as recurring every week same time, until end of term
    event.add('rrule', {'freq': 'weekly', 'interval': 1, 'byday': f'{course.day[:2]}', 'until': course_last_datetime})

    return event

def write_calendar(calendar, academic_term):
    """
    (icalendar, string) -> writes the given icalendar to an .ics file
    """
    path = join(dirname(realpath(__file__)), '../image/uploads/timetable.ics')
    with open(path, 'wb') as ics:
        ics.write(calendar.to_ical())

def create_calendar(academic_term, year, path):
    """
    (string, integer, list) -> creates calendar based on all events created from list of courses
    """
    cal = Calendar()
    classes = get_schedule(path)

    for course in classes:
        event = create_event(course, academic_term, year)
        cal.add_component(event)

    write_calendar(cal, academic_term)
