"""
generating ICS file calendar with course contents
"""

from icalendar import Calendar, Event, vText
import datetime
from extract_course_data import get_schedule
from datetime import time

PATH = 'data/schedule1.png'

classes = get_schedule(PATH)
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
    days_ahead = weekday - d.weekday()
    if days_ahead <= 0: # Target day already happened this week
        days_ahead += 7
    return d + datetime.timedelta(days_ahead)

def calendar(academic_term, year, classes):
    cal = Calendar()
    academic_term = academic_term.lower()
    term_start, term_end = get_academic_term(academic_term)
    term_start_date = datetime.date(year, int(term_start[3:]), int(term_start[0:2]))

    for course in classes:
        event = Event()
        event.add('summary', f"{course.title} - {course.type}".strip().replace("  ", " "))

        first_start_date = next_weekday(term_start_date, WEEKDAYS[course.day.lower()])
        hour, minute = int(course.start_time[:2]), int(course.start_time[3:])
        start_time = time(hour, minute, 0)

        start_date = datetime.datetime.combine(first_start_date, start_time)
        event.add('dtstart', start_date)

        hour, minute = int(course.end_time[:2]), int(course.end_time[3:])
        end_time = time(hour, minute, 0)

        end_date = datetime.datetime.combine(first_start_date, end_time)
        event.add('dtend', end_date)

        last_date = datetime.date(year, int(term_end[3:]), int(term_end[0:2]))
        course_end = datetime.datetime.combine(last_date, end_time)

        event.add('rrule', {'freq': 'weekly', 'interval': 1, 'byday': f'{course.day[:2]}', 'until': course_end})
        event['location'] = vText(course.location)

        cal.add_component(event)

        with open(f'ex.ics', 'wb') as ics:
            ics.write(cal.to_ical())

calendar('Summer', 2020, classes)
