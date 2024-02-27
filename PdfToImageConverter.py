from pdf2image import convert_from_path
import datetime
import os

def convert_pdf_to_images(pdf_path, output_folder, output_format='jpeg'):
    """
    Convert a PDF into images.

    :param pdf_path: Path to the PDF file.
    :param output_folder: Folder where the output images will be saved.
    :param output_format: Format of the output images ('jpeg', 'png').
    :return: List of file paths of the saved images.
    """
    # Extract the actual filename without the extension
    actual_filename = os.path.splitext(os.path.basename(pdf_path))[0]

    # Convert PDF to a list of images
    images = convert_from_path(pdf_path, fmt=output_format)

    # Get today's date in mmddyyyy format
    today_date = datetime.datetime.now().strftime("%m%d%Y")

    # Save each page as an image with the desired filename format
    saved_files = []
    for i, image in enumerate(images):
        filename = f'{output_folder}/{actual_filename}_{today_date}_{i + 1}.{output_format}'
        image.save(filename, output_format.upper())
        saved_files.append(filename)
        print(f'Saved {filename}')

    return saved_files

# Example usage
# pdf_path = 'ScannedSampleDocs/MultipleTestScenarioScan.pdf'
# output_folder = 'ScannedSampleDocs'
# saved_image_files = convert_pdf_to_images(pdf_path, output_folder, 'png')  # Change 'jpeg' to 'png' if you prefer PNG format

# # Print the list of saved image file paths
# print(saved_image_files)