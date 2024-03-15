
## Before running, ensure the image is in the same directory as this script.

import cv2
from tkinter import Tk, Label, Entry, Button, Scale

def analyze_image():

  image_path = image_path_entry.get()
  new_width = int(width_scale.get())
  new_height = int(height_scale.get())
  threshold = int(threshold_scale.get())

  try:
    img, thresh = process_image(image_path, new_width, new_height, threshold)
    cv2.imshow("Original Image", img)
    cv2.imshow("Resized & Thresholded Image", thresh)
  except (FileNotFoundError, ValueError) as e:
    error_label.config(text=f"Error: {str(e)}")

def process_image(image_path, new_width, new_height, threshold):
  img = cv2.imread(image_path)

  if img is None:
    raise FileNotFoundError(f"Could not open or find the image: {image_path}")

  if len(img.shape) > 2:
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

  img = cv2.resize(img, (new_width, new_height), interpolation=cv2.INTER_AREA)

  ret, thresh = cv2.threshold(img, threshold, 255, cv2.THRESH_BINARY)

  return img, thresh

root = Tk()
root.title("Image Resizing & Binary Thresholding")

image_path_label = Label(root, text="Image Path:")
image_path_label.pack()
image_path_entry = Entry(root)
image_path_entry.pack()

width_label = Label(root, text="Entering image width:")
width_label.pack()
width_scale = Scale(root, from_=1, to=1000, orient="horizontal")
width_scale.pack()
height_label = Label(root, text="Entering image height:")
height_label.pack()
height_scale = Scale(root, from_=1, to=1000, orient="horizontal")
height_scale.pack()

threshold_label = Label(root, text="Threshold:")
threshold_label.pack()
threshold_scale = Scale(root, from_=0, to=255, orient="horizontal")
threshold_scale.pack()

analyze_button = Button(root, text="Analyze", command=analyze_image)
analyze_button.pack()

error_label = Label(root, text="")
error_label.pack()

root.mainloop()