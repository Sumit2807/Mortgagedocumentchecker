import cv2
import pytesseract
from PIL import Image
import numpy as np

# Set the path to the Tesseract executable (if needed)
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
# Adjust this path to your Tesseract installation if it's not in your PATH.

# Function to preprocess the image
def preprocess_image(image_path):
    # Read the image
    img = cv2.imread(image_path)

    # Convert the image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian blur to reduce noise (you can adjust the kernel size)
    # blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Apply thresholding to convert the image to binary
    # You might need to adjust the threshold value based on your documents
    _, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # You can also try adaptive thresholding if the above doesn't give good results
    # thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
    #                                cv2.THRESH_BINARY, 11, 2)

    return thresh

# Function to extract text using OCR
def extract_text_from_image(image_path):
    # Preprocess the image (play around with preprocessing steps here)
    preprocessed_image = preprocess_image(image_path)

    # Debug: Save the preprocessed image (for visualization)
    cv2.imwrite('preprocessed_image.png', preprocessed_image)

    # Use pytesseract to extract text
    # You can adjust language, page segmentation mode (psm), and OCR engine mode (oem)
    # text = pytesseract.image_to_string(preprocessed_image, lang='eng', config='--psm 6 --oem 1')
    text = pytesseract.image_to_string(image_path, lang='eng', config='--psm 6 --oem 1')

    return text

# Example usage
image_path = 'ScannedSampleDocs/ChaseBankStatement.png'
extracted_text = extract_text_from_image(image_path)
print(extracted_text)
