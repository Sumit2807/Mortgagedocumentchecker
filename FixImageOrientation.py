from PIL import Image
import pytesseract
import re

def rotate_image_for_text_readability(image_path):
    # Load the image
    img = Image.open(image_path)

    # Use pytesseract to detect orientation
    ocr_data = pytesseract.image_to_osd(img)
    rotation_angle = int(re.search(r'(?<=Rotate: )\d+', ocr_data).group(0))

    # Determine the closest cardinal rotation
    if rotation_angle != 0:
        # Map the rotation angle to one of the cardinal directions (0, 90, 180, 270)
        if rotation_angle <= 45 or rotation_angle > 315:
            cardinal_rotation = 0  # No rotation needed
        elif 45 < rotation_angle <= 135:
            cardinal_rotation = 270  # Rotate left
        elif 135 < rotation_angle <= 225:
            cardinal_rotation = 180  # Rotate upside down
        else:
            cardinal_rotation = 90  # Rotate right

        # Apply the rotation if needed
        if cardinal_rotation != 0:
            rotated_img = img.rotate(cardinal_rotation, expand=True)
            rotated_img.save(image_path)  # Overwrite the original image
            print(f"Image rotated by {cardinal_rotation} degrees.")
        else:
            print("No rotation needed.")
    else:
        print("No rotation needed.")

# Example usage
rotate_image_for_text_readability("ScannedSampleDocs/page_3.png")
