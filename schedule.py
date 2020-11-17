import cv2
import pytesseract

img = cv2.imread('data/schedule.png')
text = pytesseract.image_to_string(img)
