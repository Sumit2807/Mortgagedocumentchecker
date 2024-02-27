from pdf2image import convert_from_bytes
import datetime
import os
import streamlit as st

def convert_pdf_to_images_streamlit(uploaded_pdf, output_folder, output_format='jpeg'):
    """
    Convert a PDF into images from an uploaded PDF file object in Streamlit.

    :param uploaded_pdf: UploadedFile object from Streamlit's file uploader.
    :param output_folder: Folder where the output images will be saved.
    :param output_format: Format of the output images ('jpeg', 'png').
    :return: List of file paths of the saved images.
    """
    # Read the PDF content as bytes from the UploadedFile object
    pdf_bytes = uploaded_pdf.read()

    # Extract the actual filename without the extension
    actual_filename = os.path.splitext(uploaded_pdf.name)[0]

    # Convert PDF bytes to a list of images
    images = convert_from_bytes(pdf_bytes, fmt=output_format)

    # Get today's date in mmddyyyy format
    today_date = datetime.datetime.now().strftime("%m%d%Y")

    # Check if output directory exists, if not create it
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Save each page as an image with the desired filename format
    saved_files = []
    for i, image in enumerate(images):
        # Correct the filename by removing the extension before appending date and page number
        filename = f'{actual_filename}_{today_date}_{i + 1}.{output_format}'
        full_path = os.path.join(output_folder, filename)
        image.save(full_path, output_format.upper())
        saved_files.append(full_path)
        print(f'Saved {full_path}')

    return saved_files

# Streamlit usage example
# uploaded_pdf = st.file_uploader("Upload a PDF", type=["pdf"])
# if uploaded_pdf is not None:
#     output_folder = '/Users/sugupta/Natwest_Document_Checker_Updated/ScannedSampleDocs'  # Make sure this directory exists or is created
#     saved_image_files = convert_pdf_to_images_streamlit(uploaded_pdf, output_folder, 'jpeg')  # Change 'jpeg' to 'png' if you prefer PNG format
#     # Provide download links for the saved images
#     for image_path in saved_image_files:
#         with open(image_path, "rb") as file:
#             st.download_button(
#                 label=f"Download {os.path.basename(image_path)}",
#                 data=file,
#                 file_name=os.path.basename(image_path),
#                 mime="image/jpeg"
#             )
