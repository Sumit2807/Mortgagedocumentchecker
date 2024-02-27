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


def call_updatedpromptgpt4preview(pages_data):
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
        3. Ensure you convert all the <Start Date> and <End Date> in dd/mmm/yyyy format in JSON output.
        4  Extract the relevant information from the statement text based on the document type.
        5. If only one date is present then use that date month and year to create start date and end date.
        6. Classify statement as SA302 if "Self Assessment" text is followed by "Unique Taxpayer Reference (UTR):".
        7. Classify statement as TaxOverviewStatement if "Tax year overview" text is followed by "Tax year ending". 
        8. Classify statement as TaxReturnStatement look for text "Tax Return <YYYY>" where <YYYY> is the financial year.
        9. Classify statement as TaxCalculationStatement if "Tax calculation summary" text is followed by "Tax year".
        10. Generate the output in the JSON structure mentioned above.
        11.Ensure that the output structure is consistent for every call to maintain compatibility with the user's expectations.
        12.Replace the placeholders <firstname>,<lastname><DocumentType>, <Start Date>, and <End Date> with the appropriate values in the output.
        13.Return the output in the JSON format.
        14.After generating the JSON output, review it against the provided text to ensure all document types have been captured and correctly classified.

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






# """
# #### 1. **Bank Statement**
# - Not applicable for tax-specific documents but ensure to capture transaction periods and relevant financial information.

# #### 2. **PaySlip**
# - Identify payslips by looking for keywords such as "Gross Pay," "Net Pay," and "Tax Deducted." Capture the pay period and amounts.

# #### 3. **SA302**
# - **Keyword:** "Self Assessment Unique Taxpayer Reference (UTR):"
# - **Action:** Classify the document as an SA302 statement upon finding this keyword, capturing the tax year and any financial figures mentioned.

# #### 4. **Tax Overview Statement**
# - **Keyword:** "Tax year overview" along with "Tax year ending <dd mmm yyyy>"
# - **Action:** Classify the document as a Tax Overview Statement, capturing the tax year and summarizing the tax details provided.

# #### 5. **Tax Return Statement**
# - **Keyword:** "Tax Return <YYYY>"
# - **Action:** Identify the document as a Tax Return Statement based on the presence of this phrase, capturing the financial year and detailed income and tax information.

# #### 6. **Tax Calculation Statement**
# - **Keyword:** "Tax calculation summary" along with "Tax year <d mmmm yyyy> to <d mmmm yyyy> (<yyyy-yy>)"
# - **Action:** Classify the document as a Tax Calculation Statement, capturing the tax year, calculated tax, and any deductions or contributions."""