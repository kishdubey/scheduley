"""
generating ICS file calendar with course contents
"""

from icalendar import Calendar, Event
import recurring_ical_events
from datetime import datetime
from extract_course_data import get_schedule

PATH = 'data/schedule1.png'

classes = get_schedule(PATH)
ACADEMIC_TERMS = {"Summer": "01/05 - 31/08", "Fall": "01/09 - 31/12", "Winter": "01/01 - 30/04"}
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
    term_start, term_end = get_academic_term(academic_term)
    term_start_date = datetime.date(year, term_start[3:], term_start[0:2])
    first_start_date = next_weekday(term_start_date, WEEKDAYS[class.day])

    for class in classes:
        event = Event()
        event.add('summary', f"{class.title} - {class.type}")

        start_date = datetime(year, first_start_date, class.start_time, class.end_time)
        event.add('dtstart', date =
