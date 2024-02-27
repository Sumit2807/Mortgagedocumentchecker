from PIL import Image, ImageEnhance, ImageStat
import cv2
import numpy as np
import os

def analyze_image_quality(image_path):
    # Load the image
    image = Image.open(image_path)
    cv_image = cv2.imread(image_path)

    # Basic metadata
    metadata = {
        'resolution': image.size,
        'format': image.format,
        'mode': image.mode
    }

    # Brightness and Contrast
    stat = ImageStat.Stat(image)
    brightness = sum(stat.mean) / len(stat.mean)
    contrast = sum(stat.stddev) / len(stat.stddev)
    metadata['brightness'] = brightness
    metadata['contrast'] = contrast

    # Noise (Estimate using variance of the Laplacian)
    gray_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
    laplacian_var = cv2.Laplacian(gray_image, cv2.CV_64F).var()
    metadata['noise'] = laplacian_var

    # Sharpness (Estimate using variance of the Laplacian)
    metadata['sharpness'] = laplacian_var

    # Evaluate quality based on thresholds (example)
    # These thresholds are arbitrary; adjust based on your requirements
    if laplacian_var < 100:
        metadata['sharpness_evaluation'] = 'possibly blurry'
    else:
        metadata['sharpness_evaluation'] = 'sharp'

    if brightness < 50 or brightness > 200:
        metadata['brightness_evaluation'] = 'may need adjustment'
    else:
        metadata['brightness_evaluation'] = 'acceptable'

    if contrast < 40:
        metadata['contrast_evaluation'] = 'low contrast'
    else:
        metadata['contrast_evaluation'] = 'acceptable'

    return metadata

def adjust_brightness_contrast(image, brightness=0, contrast=0):
    """
    Adjust the brightness and contrast of an image.
    Brightness and contrast adjustments are based on deviations from 'ideal' values.
    """
    enhancer = ImageEnhance.Brightness(image)
    image = enhancer.enhance(brightness)

    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(contrast)

    return image

def reduce_noise(image):
    """
    Apply noise reduction to the image.
    """
    return cv2.fastNlMeansDenoisingColored(image, None, 10, 10, 7, 21)

def sharpen_image(image):
    """
    Apply sharpening to the image using a Gaussian blur and then adding the
    detail back to the original image.
    """
    gaussian_blur = cv2.GaussianBlur(image, (0, 0), 3)
    sharp_image = cv2.addWeighted(image, 1.5, gaussian_blur, -0.5, 0)
    return sharp_image

def apply_corrections(image_path, metadata):
    # Load image with Pillow and OpenCV
    image_pil = Image.open(image_path)
    image_cv = cv2.imread(image_path)

    # Adjust brightness and contrast if needed
    if 'brightness_evaluation' in metadata and metadata['brightness_evaluation'] == 'may need adjustment':
        image_pil = adjust_brightness_contrast(image_pil, brightness=1.1, contrast=1.1)

    # Reduce noise if detected as high
    if 'noise' in metadata and metadata['noise'] > 100:  # Example threshold
        image_cv = reduce_noise(image_cv)

    # Sharpen if detected as blurry
    if 'sharpness_evaluation' in metadata and metadata['sharpness_evaluation'] == 'possibly blurry':
        image_cv = sharpen_image(image_cv)

    # Convert OpenCV image back to PIL to save or display
    corrected_image = cv2.cvtColor(image_cv, cv2.COLOR_BGR2RGB)
    corrected_image_pil = Image.fromarray(corrected_image)

    return corrected_image_pil

# Example usage
image_path = '/Users/sugupta/Downloads/NWG Test Scenarios Data/Test Case 07/Jane Smith - Tesco-Payslip-January.jpg'
metadata = analyze_image_quality(image_path) # Assume this function is defined as per the previous script
print(metadata)
# corrected_image = apply_corrections(image_path, metadata)

# To display the corrected image (if using Jupyter Notebook or similar environment)
# corrected_image.show()

# To save the corrected image
# newfilename=f"Enhanced_{os.path.basename(image_path)}"
# corrected_image.save(f"EnhancedImage/{newfilename}")
