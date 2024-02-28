import cv2

def analyze_image(image_path, resize_dim=(None, None), threshold=127):
  
  img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

  if resize_dim[0] is not None and resize_dim[1] is not None:
    img = cv2.resize(img, resize_dim, interpolation=cv2.INTER_AREA)

  ret, thresh = cv2.threshold(img, threshold, 255, cv2.THRESH_BINARY)

  return thresh


image_path = "assignment1\image.jpg"
resized_thresholded_image = analyze_image(image_path, resize_dim=(600, 600))


cv2.imshow("Resized and Thresholded Image", resized_thresholded_image)
cv2.waitKey(0)
cv2.destroyAllWindows()