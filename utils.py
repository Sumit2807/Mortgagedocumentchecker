import PyPDF2
from openai import OpenAI
from pypdf import PdfReader
import json
from datetime import datetime, timedelta
import tkinter as tk
from tkinter import filedialog
from dotenv import load_dotenv
import streamlit as st
from dateutil.relativedelta import relativedelta
import re
from typing import Dict, Any
import base64
import calendar
load_dotenv()


# Define a function to reset the app
def reset_app():
    for key in st.session_state.keys():
        del st.session_state[key]
    st.rerun()
# Function to convert image file to base64
def get_image_base64(path):
    with open(path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()


def format_status(doctypevalid, statusvalidtext, statusinvalidtext, additional_text):
    icon = "✅" if doctypevalid else "❌"
    status = statusvalidtext if doctypevalid else statusinvalidtext
    return f"""
        <style>
        .formatted-text {{
            font-size: 14px;
            color:black;
        }}
        .bold-text {{
            font-weight: bold;
        }}
        </style>
        <p class='formatted-text'>{icon} <span class='bold-text'>{additional_text}:</span> {status}</p>
        """
def format_text_color(text, flag):
    color = "#542B79" if flag else "#542B79"
    return f"""
        <style>
        .colored-text {{
            font-size: 16px;
            color: {color};
            font-weight: bold;
        }}
        </style>
        <span class='colored-text'>{text}</span>
        """
def format_text_color_black(text, flag):
    color = "#000000" if flag else "#000000"
    return f"""
        <style>
        .colored-text {{
            font-size: 14px;
            color: {color};
            font-weight: bold;
        }}
        </style>
        <span class='colored-text'>{text}</span>
        """

def is_digital_pdf(file_path):
    """
    Check if a PDF is digital (contains text) or scanned.
    Returns True if the PDF is digital, False otherwise.
    """
    try:
        text = ""
        pdf_reader = PdfReader(file_path)
        for page in pdf_reader.pages:
            text += page.extract_text()
        text.strip()
        cleantext=text.replace(' ', '').replace('\n', '')
        if cleantext:
            # print(text)
            return True  # Text found, it's a digital PDF
        else:
            return False  # No text found, it's likely a scanned image PDF
    except:
        return False  # Error occurred, potentially not a valid PDF
    
    
#Extract Information from PDF file
def get_pdf_text(pdf_doc):
    text = ""
    pdf_reader = PdfReader(pdf_doc)
    for page in pdf_reader.pages:
        text += page.extract_text()  
    
    Json_data= extract_data_from_document(text)
    print(f"Resonse from API:-  {Json_data}")
    return Json_data

def extract_data_from_document(pages_data):
    print(f"STATEMENT DATA RECEIVED BY OPENAI FUNCTION{pages_data}")
    client = OpenAI()
    template = """
        Objective: The objective of this task is to process statement data for a mortgage application. The statement data may be provided in multiple documents or merged into a single document. The goal is to extract relevant information from the statements and generate an output in a consistent JSON structure.

        Input:

        Statement Text: The user will provide the statement text for processing. The statement text may contain information related to bank statements, payslips, SA302 statements, tax overview statements, tax calculation statements, or tax return statements.
        Document Type: The user will specify the type of document being processed (e.g., bank statement, payslip, SA302, tax overview statement, tax calculation statement, or tax return statement).
        Output: The output will be generated in the following JSON structure:

        [
        {
            
            "<DocumentType>": {
            "Is<DocumentType>": true,
            "FirstName": "<firstname>",
            "LastName": "<lastname>",
            "<DocumentType>Periods": {
                "1": {
                "Start": "<Start Date>",
                "End": "<End Date>"
                },
                "2": {
                "Start": "<Start Date>",
                "End": "<End Date>"
                },
                ...
            }
            },
            ...
        }
        ]
            • <DocumentType>: Replace with the specific document type being processed (e.g., BankStatement, PaySlip, SA302, TaxOverviewStatement, TaxCalculationStatement, or TaxReturnStatement).
            • <Start Date>: Replace with the start date of the statement period.
            • <End Date>: Replace with the end date of the statement period.

        Instructions:

            1. Receive the statement text 
            2.Most important thing is to look for each doc type periods and capture it in the output. Ensure to capture each period in the output irrespective whether it makes sense or not.
            3. Statement Periods should be in dd/mmm/yyyy format.
            4 Extract the relevant information from the statement text based on the document type.
            5. Generate the output in the JSON structure mentioned above.
            6. Ensure that the output structure is consistent for every call to maintain compatibility with the user's expectations.
            7. Replace the placeholders <firstname>,<lastname><DocumentType>, <Start Date>, and <End Date> with the appropriate values in the output.
            8. Return the output in the JSON format.

        """

    response = client.chat.completions.create(
    model="gpt-4-turbo-preview",temperature=0,
    top_p=1,frequency_penalty=0,presence_penalty=0,
    response_format={ "type": "json_object" },
    messages=[
    {"role": "system", "content": template},
    {"role": "user", "content": pages_data}
    ]
    )
    print(f"This is the response from OpenAIAPI function: {response.choices[0].message.content}")
    return response.choices[0].message.content




def is_valid_date(date_str: str) -> bool:
    """
    Validates if the date string matches the dd/mmm/yyyy format.
    """
    return bool(re.match(r'\d{2}/[a-z]{3}/\d{4}', date_str, re.IGNORECASE))


def validate_document_format_new(json_obj: Any) -> bool:
    """
    Validates if the given JSON object adheres to the specified format.
    """
    valid_document_types = {
        "BankStatement", 
        "PaySlip", 
        "SA302", 
        "TaxOverviewStatement", 
        "TaxCalculationStatement", 
        "TaxReturnStatement"
    }
    if not isinstance(json_obj, list):
        return False
    
    for item in json_obj:
        if not isinstance(item, dict):
            return False

        document_type = list(item.keys())[0]
        # Check if document type is valid
        if document_type not in valid_document_types:
            return False
            
        details = item[document_type]
        
        # Checking if 'Is<DocumentType>' is True
        is_doc_type = f'Is{document_type}'
        if not details.get(is_doc_type, False) is True:
            return False

        # Validate FirstName and LastName
        if not all(key in details for key in ('FirstName', 'LastName')):
            return False

        # Validate periods
        periods_prefix = f'{document_type}Periods'
        periods = details.get(periods_prefix, {})
        if not isinstance(periods, dict):
            return False

        for period in periods.values():
            start_date = period.get('Start', '')
            end_date = period.get('End', '')
            if not (is_valid_date(start_date) and is_valid_date(end_date)):
                return False
    return True


# def determine_financial_year(cutoff_date):
#     if cutoff_date.month > 3:  # April or later
#         start_year = cutoff_date.year - 1
#     else:  # January to March
#         start_year = cutoff_date.year - 2
#     return f"Mar{start_year + 1}",f"Apr{start_year}"

def determine_financial_year(cutoff_date):
    if cutoff_date.month > 3:  # April or later
        start_year = cutoff_date.year - 1
    else:  # January to March
        start_year = cutoff_date.year - 2
    
    financial_year = []
    for month in range(4, 13):
        financial_year.append(f"{calendar.month_abbr[month]}{start_year}")
    for month in range(1, 4):
        financial_year.append(f"{calendar.month_abbr[month]}{start_year + 1}")
    
    return financial_year

from datetime import datetime


def extract_statement_months(document, doc_type):
    try:
        statement_periods = document.get(doc_type, {}).get(f"{doc_type}Periods", {})
        months = []

        for period in statement_periods.values():
            start_date = datetime.strptime(period["Start"], "%d/%b/%Y")
            end_date = datetime.strptime(period["End"], "%d/%b/%Y")

            current_date = start_date
            while current_date <= end_date:
                month_year = current_date.strftime("%b%Y")
                months.append(month_year)
                current_date += relativedelta(months=1)

        return months
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return []


# List of document types for final validation
doc_types_for_validation = ["Bank Statement", "Pay Slip"]  # Add more types as needed
