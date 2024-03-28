import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import cv2
import numpy as np
from PIL import Image, ImageTk
import matplotlib.pyplot as plt

root = tk.Tk()
root.title("Advanced Image Filtering")
content_frame = tk.Frame(root)
content_frame.pack(fill="both", expand=True)
frame = tk.Frame(root)
frame.pack()

image_canvas = tk.Canvas(content_frame, width=500, height=500)
image_scrollbar = tk.Scrollbar(content_frame, orient="vertical", command=image_canvas.yview)
image_canvas.configure(yscrollcommand=image_scrollbar.set)
image_canvas.pack(side="left", fill="both", expand=True)
image_scrollbar.pack(side="right", fill="y")

filtered_image_canvas = tk.Canvas(content_frame, width=500, height=500)
filtered_image_scrollbar = tk.Scrollbar(content_frame, orient="vertical", command=filtered_image_canvas.yview)
filtered_image_canvas.configure(yscrollcommand=filtered_image_scrollbar.set)
filtered_image_canvas.pack(side="right", fill="both", expand=True)
filtered_image_scrollbar.pack(side="right", fill="y")

file_path = ''
magnitude_spectrum = ''

def open_image():
        global file_path
        file_path = filedialog.askopenfilename()
        if file_path:
                display_image(file_path, image_canvas)

def update_image():
    global file_path
    file_path = filedialog.askopenfilename()
    if file_path:
        display_image(file_path, image_canvas)
        

def display_image(image_data, canvas):
    if isinstance(image_data, str):
        image = Image.open(image_data)
    else:
        image = Image.fromarray(image_data)
    canvas_width = canvas.winfo_width()
    if canvas_width > 0:  
        aspect_ratio = image.width / image.height
        new_height = int(canvas_width / aspect_ratio)
        if new_height > canvas.winfo_height():
            new_height = canvas.winfo_height()
            new_width = int(new_height * aspect_ratio)
        else:
            new_width = canvas_width
        image = image.resize((new_width, new_height), Image.LANCZOS)
    else:
        pass
    photo = ImageTk.PhotoImage(image)
    canvas.create_image(0, 0, anchor="nw", image=photo)
    canvas.image = photo  

def frequency_domain_analysis():
        global file_path
        if not file_path:
                return
        image = Image.open(file_path)
        image = np.array(image.convert('L'))
        dft = cv2.dft(np.float32(image), flags=cv2.DFT_COMPLEX_OUTPUT)
        dft_shift = np.fft.fftshift(dft)
        magnitude_spectrum = 20 * np.log(cv2.magnitude(dft_shift[:,:,0], dft_shift[:,:,1]))
        display_image(magnitude_spectrum, filtered_image_canvas)

def image_reconstruction():
        global file_path
        if not file_path:
                return
        image = Image.open(file_path)
        image = np.array(image.convert('L'))
        dft = cv2.dft(np.float32(image), flags=cv2.DFT_COMPLEX_OUTPUT)
        dft_shift = np.fft.fftshift(dft)
        low_mask = np.zeros((image.shape[0], image.shape[1]), np.uint8)
        low_mask[image.shape[0]//2-30:image.shape[0]//2+30, image.shape[1]//2-30:image.shape[1]//2+30] = 1
        mid_mask = np.zeros((image.shape[0], image.shape[1]), np.uint8)
        mid_mask[image.shape[0]//2-60:image.shape[0]//2+60, image.shape[1]//2-60:image.shape[1]//2+60] = 1
        mid_mask -= low_mask
        high_mask = np.ones((image.shape[0], image.shape[1]), np.uint8)
        high_mask -= mid_mask + low_mask
        for mask in [low_mask, mid_mask, high_mask]:
                mask = np.expand_dims(mask, axis=-1)
                fshift = dft_shift * mask
                f_ishift = np.fft.ifftshift(fshift)
                img_back = cv2.idft(f_ishift)
                img_back = cv2.magnitude(img_back[:,:,0], img_back[:,:,1])
                display_image(img_back, filtered_image_canvas)

def add_noise(image):
        mean = 0
        var = 0.1
        sigma = var**0.5
        gaussian = np.random.normal(mean, sigma, image.shape)
        noisy_image = np.clip(image + gaussian * 255, 0, 255).astype(np.uint8)
        return noisy_image

def noise_reduction():
        global file_path
        if not file_path:
                return
        image = Image.open(file_path)
        image = np.array(image.convert('L'))
        noisy_image = add_noise(image)
        dft = cv2.dft(np.float32(noisy_image), flags=cv2.DFT_COMPLEX_OUTPUT)
        dft_shift = np.fft.fftshift(dft)
        mask = np.zeros((noisy_image.shape[0], noisy_image.shape[1]), np.uint8)
        mask[noisy_image.shape[0]//2-30:noisy_image.shape[0]//2+30, noisy_image.shape[1]//2-30:noisy_image.shape[1]//2+30] = 1
        mask = np.expand_dims(mask, axis=-1)
        fshift = dft_shift * mask
        f_ishift = np.fft.ifftshift(fshift)
        img_back = cv2.idft(f_ishift)
        img_back = cv2.magnitude(img_back[:,:,0], img_back[:,:,1])
        img_back_pil = Image.fromarray(img_back.astype(np.uint8))
        img_back_tk = ImageTk.PhotoImage(img_back_pil)
        label = tk.Label(frame, image=img_back_tk)
        label.image = img_back_tk  
        display_image(img_back, filtered_image_canvas)
        label.pack()

def edge_enhancement():
        global file_path
        if not file_path:
                return
        image = Image.open(file_path)
        image = np.array(image.convert('L'))
        dft = cv2.dft(np.float32(image), flags=cv2.DFT_COMPLEX_OUTPUT)
        dft_shift = np.fft.fftshift(dft)
        mask = np.ones((image.shape[0], image.shape[1]), np.uint8)
        mask[image.shape[0]//2-30:image.shape[0]//2+30, image.shape[1]//2-30:image.shape[1]//2+30] = 0
        mask = np.expand_dims(mask, axis=-1)
        fshift = dft_shift * mask
        f_ishift = np.fft.ifftshift(fshift)
        img_back = cv2.idft(f_ishift)
        img_back = cv2.magnitude(img_back[:,:,0], img_back[:,:,1])
        display_image(img_back, filtered_image_canvas)




button_frame = tk.Frame(content_frame)
button_frame.pack(side="bottom")

update_button = tk.Button(button_frame, text="Update Image", command=update_image)
update_button.pack(side="left", padx=5, pady=5)

upload_button = tk.Button(button_frame, text="Upload Image", command=open_image)
upload_button.pack(side="left", padx=5, pady=5)

frequency_domain_button = tk.Button(button_frame, text="Frequency Domain", command=frequency_domain_analysis)
frequency_domain_button.pack(side="left", padx=5, pady=5)

image_reconstruction_button = tk.Button(button_frame, text="Reconstruct Image", command=image_reconstruction)
image_reconstruction_button.pack(side="left", padx=5, pady=5)

noise_reduction_button = tk.Button(button_frame, text="Noise Reduction", command=noise_reduction)
noise_reduction_button.pack(side="left", padx=5, pady=5)

edge_enhancement_button = tk.Button(button_frame, text="Edge Enhancement", command=edge_enhancement)
edge_enhancement_button.pack(side="left", padx=5, pady=5)

root.mainloop()