"""
generating ICS file calendar with course contents
"""
from icalendar import Calendar, Event, vText
import datetime
from extract_course_data import get_schedule
from datetime import time

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
    if days_ahead <= 0: # Target day already happened this week
        days_ahead += 7
    return d + datetime.timedelta(days_ahead)

def create_event(course, academic_term):
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
    with open(f'{academic_term}-timetable.ics', 'wb') as ics:
        ics.write(cal.to_ical())

def create_calendar(academic_term, year, path):
    """
    (string, integer, list) -> creates calendar based on all events created from list of courses
    """
    cal = Calendar()
    classes = get_schedule(path)

    for course in classes:
        event = create_event(course)
        cal.add_component(event)

    write_calendar(cal, academic_term)
