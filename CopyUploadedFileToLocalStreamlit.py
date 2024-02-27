import os
import shutil
import streamlit as st

def save_uploaded_file(uploaded_file, destination_folder):
    """
    Copies an uploaded file to a destination folder.

    :param uploaded_file: The UploadedFile object from Streamlit.
    :param destination_folder: The path to the folder where the file will be saved.
    :return: The path to the saved file or None if an error occurred.
    """
    # Ensure the destination folder exists
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)
    
    # Construct the full path for the destination file
    destination_path = os.path.join(destination_folder, uploaded_file.name)

    try:
        # Write the uploaded file's contents to the destination file
        with open(destination_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # Check if the file was copied successfully by comparing file sizes
        if os.path.getsize(destination_path) == uploaded_file.size:
            print(f"File '{uploaded_file.name}' copied successfully to '{destination_path}'")
            return destination_path
        else:
            print(f"File '{uploaded_file.name}' could not be copied successfully.")
            return None
    except Exception as e:
        # Handle any exception that occurs during the file write process
        print(f"An error occurred while copying the file: {e}")
        return None

# Example usage in a Streamlit app
# st.title("File Upload and Copy")

# # Allow the user to upload a file
# uploaded_file = st.file_uploader("Choose a file")

# if uploaded_file is not None:
#     # The path to the local repository where files should be copied
#     local_repository_path = "path/to/local/repository"

#     # Call the function to copy the uploaded file to the local repository
#     saved_file_path = save_uploaded_file(uploaded_file, local_repository_path)

#     if saved_file_path:
#         st.success(f"File '{uploaded_file.name}' has been copied successfully.")
#     else:
#         st.error("File copy failed.")

