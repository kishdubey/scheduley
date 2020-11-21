"""
generating ICS file calendar with course contents
"""

from ics import Calendar, Event
from extract_course_data import get_schedule

PATH = 'data/schedule1.png'

classes = get_schedule(PATH)
ACADEMIC_TERMS = {"Summer": "01/05 - 31/08", "Fall": "01/09 - 31/12", "Winter": "01/01 - 30/04"}

def get_academic_term(academic_term):
    """
    (string) -> tuple
    returns the start and end dates of the given academic term
    """
    term = ACADEMIC_TERMS[academic_term]
    start = term[0:5]
    end = term[8:]

    return start, end

# self.title = title
# self.type = type
# self.start_time = start_time
# self.end_time = end_time
# self.location = location
# self.day = day
def calendar(academic_term, year, classes):
    cal = Calendar()
    term_start, term_end = get_academic_term(academic_term)

    for class in classes:
        evet = Event()
        event.add('summary', f"{class.title} - {class.type}")
        e.begin = f"{year}-{term_start}-{term_end} {class.start_time}"
