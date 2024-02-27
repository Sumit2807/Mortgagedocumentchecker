from openai import OpenAI
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

load_dotenv()

client = OpenAI()


def get_statement_text(pdf_doc):
    text = ""
    pdf_reader = PdfReader(pdf_doc)
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text


def call_gpt4preview(pages_data):
    # pages_data= get_pdf_text("/Users/sugupta/Downloads/Bob Johnson - merged.pdf")
    
    
    print(pages_data)
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
        • <Start Date>: Replace with the start date of the statement period in dd/mmm/yyyy format.
        • <End Date>: Replace with the end date of the statement period in dd/mmm/yyyy format.

    Instructions:

        1. Receive the statement text 
        2. Most important thing is to look for each doc type periods and capture it in the output. Ensure to capture each period in the output irrespective whether it makes sense or not.
        3. Ensure you convert the <Start Date> and <End Date> in dd/mmm/yyyy format in JSON output.
        4  Extract the relevant information from the statement text based on the document type.
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
    print(response.choices[0].message.content)
    return (response.choices[0].message.content)