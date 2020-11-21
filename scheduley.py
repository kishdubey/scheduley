"""
extracting classes data from an image of a class schedule
"""

import cv2
import pytesseract

PATH = 'data/schedule1.png'

class Class:
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

def get_classes(info_list):
    """
    (list) -> list
    returns list of classes of type Class from given list of raw extracted text
    """
    WEEKDAYS = set(["monday", "tuesday", "wednesday", "thursday", "friday"])
    classes = []
    day = 'Monday'
    i = 0

    while i < len(info_list):
        current = info_list[i]
        if current.lower() in WEEKDAYS:
            day = current

            class_title = info_list[i+2].strip()
            class_type = info_list[i+3]
            time = info_list[i+4]
            class_start_time = time[:6]
            class_end_time = time[8:]
            class_location = info_list[i+5].replace("Location: ", "")

            this_class = Class(helper_capitalize(class_title), class_type, class_start_time, class_end_time, class_location, day)
            classes.append(this_class)
            i += 6

        else:
            class_title = info_list[i].strip()
            class_type = info_list[i+1]
            time = info_list[i+2]
            class_start_time = time[:6]
            class_end_time = time[8:]
            class_location = info_list[i+3].replace("Location: ", "")

            this_class = Class(helper_capitalize(class_title), class_type, class_start_time, class_end_time, class_location, day)
            classes.append(this_class)
            i += 4

    return classes

def main(path):
    img = get_image(path)
    info_list = extract_information(img)
    classes = get_classes(info_list)

    return classes

print(main(PATH))
