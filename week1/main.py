from PIL import ImageFilter, Image, ImageEnhance
import matplotlib.pyplot as plt

# Load the image.jpg file
image = Image.open('week1\image.jpg')

# Display the image
def load_and_display_image(image):    
    plt.imshow(image)
    plt.axis('off')
    plt.show()

def convert_to_grayscale(image):
    gray_image = image.convert('L')
    gray_image.show()

def resize_image(image, new_width, new_height):
    new_resolution = (new_width, new_height)
    resized_image = image.resize(new_resolution)
    resized_image.show()

def crop_image(image, left, upper, right, lower):
    cropped_image = image.crop((left, upper, right, lower))
    cropped_image.show()

def increase_brightness(image, factor):
    enhancer = ImageEnhance.Brightness(image)
    enhanced_image = enhancer.enhance(factor)
    enhanced_image.show()

def increase_contrast(image, factor):
    enhancer = ImageEnhance.Contrast(image)
    enhanced_image = enhancer.enhance(factor)
    enhanced_image.show()

def rotate_image(image, angle, expand):
    rotated_image = image.rotate(angle, expand=expand)
    rotated_image.show()

def flip_image(image, axis):
    flipped_image = image.transpose(axis)
    flipped_image.show()

def apply_blur_filter(image):
    blurred_image = image.filter(ImageFilter.BLUR)
    blurred_image.show()

def apply_sharpen_filter(image):
    sharpened_image = image.filter(ImageFilter.SHARPEN)
    sharpened_image.show()

# load_and_display_image(image)
convert_to_grayscale(image)
resize_image(image, 800, 600)
crop_image(image, 100, 100, 400, 400)  
increase_brightness(image, 1.5) 
increase_contrast(image, 1.5)  
rotate_image(image, 90, expand=True)
flip_image(image, Image.FLIP_LEFT_RIGHT) 
apply_blur_filter(image)
apply_sharpen_filter(image)

