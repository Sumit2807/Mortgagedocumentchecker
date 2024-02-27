import streamlit as st
from dotenv import load_dotenv
from utils import *
import os
import json
from datetime import datetime, timedelta
from dotenv import load_dotenv


# Set up the page configuration with a title and favicon
st.set_page_config(page_title="NatWest Mortgage Services", page_icon=":bank:", layout="wide")



# Define the NatWest color scheme
primary_color = "#542B79"   # NatWest dark blue
secondary_color = "#FFFFFF" # White
text_color = "#CCCCD3"      # Black
background_color = "#CCCCD3" # Light Grey

# Display the image at the top of the page
st.image("/Users/sugupta/Natwest_Document_Checker/NatwestIcon/NatwestLogo.png", 
         use_column_width=True, output_format='auto', caption=None)

# Custom CSS for the submit button
st.markdown("""
    <style>
        div.stButton > button:first-child {
            background-color: #542B79;
            color: white;
            border-radius: 20px;
            border: none;
            padding: 10px 24px;
            font-size: 16px;
        }
    </style>""", unsafe_allow_html=True)

# Custom CSS
st.markdown(f"""
    <style>
        div.stButton > button:first-child {{
            background-color: #542B79;
            color: white;
            border-radius: 20px;
            border: none;
            padding: 10px 24px;
            font-size: 16px;
        }}

        .reportview-container, .reportview-container .markdown-text {{
            background-color: {background_color};
            color: #CCCCD3; /* Grey text color */
        }}

        .sidebar .sidebar-content {{
            background-color: {secondary_color};
        }}

        header .css-1py0x6l {{
            background-color: {primary_color};
        }}

        .css-1aumxhk {{
            background-color: {primary_color};
            color: {secondary_color};
        }}
        
        h1,h2,h3  {{
            color: #542B79 !important; /* Change the title and heading colors */
        }}

        # label, .stTextInput label, .stFileUploader label  {{
        #     color: #CCCCD3 !important; /* Change the title and heading colors */
        # }}
    </style>
""", unsafe_allow_html=True)

# NatWest logo (replace 'path_to_natwest_logo.png' with the path to the actual logo)
# st.image("/Users/sugupta/Natwest_Document_Checker/NatwestIcon/NatwestLogo.png", width=100)


# Main content of your app
st.title("Mortgage Services")
st.subheader("Welcome to NatWest Mortgage Services. [Include more detailed content here]")

# Inserting the form
with st.form(key='mortgage_form'):
    first_name = st.text_input("First Name")
    last_name = st.text_input("Last Name")
    dob = st.text_input("Date of Birth (DD-MM-YYYY)")
    # Uncomment and use the following fields as needed
    # current_address = st.text_area("Current Address")
    # purchase_property_address = st.text_area("Purchase Property Address")
    # purchase_property_price = st.text_input("Purchase Property Price(£)")
    # deposit_amount = st.text_input("Deposit Amount(£)")
    # term = st.number_input("Term (in years)", min_value=1, step=1)
    # property_valuation = st.text_input("Property valuation (£)")
    uploaded_files = st.file_uploader("Upload Supporting Documents", accept_multiple_files=True, type=["pdf", "jpeg", "png"])
    submit_button = st.form_submit_button("Submit")

# Placeholder for additional content
# st.write(format_text_color("Sumit_Aug_BankStatement.pdf",True),unsafe_allow_html=True)
st.error('Sumit_Aug_BankStatement.pdf', icon="🚨")
st.write(format_status(False,"Valid","Invalid","Documet Type" ),unsafe_allow_html=True)
st.write(format_status(True,"Valid","Statement date is not within 90 days","Statement Period" ),unsafe_allow_html=True)
st.write(format_status(False,"Passed","Name provided on form does not match with name on the file uploaded","Name Check" ),unsafe_allow_html=True)

doc_type="Testing"
st.error(f"🚨 {doc_type}s missing for: {', '.join(missing)}")


st.write(format_text_color("Sumit_Dec_BankStatement.pdf",True),unsafe_allow_html=True)
st.write(format_status(True,"Valid","Invalid","Documet Type" ),unsafe_allow_html=True)
st.write(format_status(True,"Valid","Statement date is not within 90 days","Statement Period" ),unsafe_allow_html=True)
st.write(format_status(True,"Passed","Name provided on form does not match with name on the file uploaded","Name Check" ),unsafe_allow_html=True)


# Add placeholders for any images or additional content you want to include
# st.image("path_to_image.png", caption="Image Caption")

# Footer

# st.markdown("---")

# st.subheader("Our Services")
# st.write("[Include description of services here]")

# st.subheader("Contact Us")
# st.write("[Include contact information here]")
# st.write("© 2024 NatWest Bank. All rights reserved.")

# Run this script with Streamlit to see the layout.
