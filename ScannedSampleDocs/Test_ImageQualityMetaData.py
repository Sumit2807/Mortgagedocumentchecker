import cv2
import numpy as np
from PIL import Image, ImageStat

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

# Example usage
image_path = 'path_to_your_image.jpg'
quality_metadata = analyze_image_quality("ScannedSampleDocs/Barclays_high_resolution_BankStatement.jpg")
print(quality_metadata)
