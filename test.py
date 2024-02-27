from datetime import datetime
from dateutil.relativedelta import relativedelta
import json
import re
from typing import Dict, Any
import calendar


import base64
import streamlit as st

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

extracted_data="""{ "PaySlip": { "IsPaySlip": true, "FirstName": "Jane", "LastName": "Smith", "PaySlipPeriods": { "1": { "Start": "30/11/2023", "End": "30/11/2023" }, "2": { "Start": "31/01/2024", "End": "31/01/2024" } } }, "BankStatement": { "IsBankStatement": true, "FirstName": "Jane", "LastName": "Smith", "BankStatementPeriods": { "1": { "Start": "01/Oct/2023", "End": "31/Oct/2023" }, "2": { "Start": "01/Nov/2023", "End": "30/Nov/2023" }, "3": { "Start": "01/Dec/2023", "End": "31/Dec/2023" }, "4": { "Start": "01/Jan/2024", "End": "31/Jan/2024" } } } }"""
doc = json.loads(extracted_data)
documents=[doc] 

validate_document_format_new(documents)




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

FYList=determine_financial_year(datetime.today())
print(FYList)


cutoff_date=datetime.today()


extracted_data="""{ "BankStatement": { "IsBankStatement": true, "FirstName": "Jane", "LastName": "Smith", "BankStatementPeriods": { "1": { "Start": "01/Jan/2024", "End": "31/Jan/2024" } } } }"""
doc = json.loads(extracted_data)
documents=[doc]
validate_document_format_new(documents)

missing_periods=[]
expected_months=["Jan2024","Dec2023","Nov2023"]
Overall_PayslipPeriods=["Nov2023","Dec2023","Jan2024"]






response= {'id': 'chatcmpl-8nA3t4VjNkzvURqUACoWumjx0zZUL', 'object': 'chat.completion', 'created': 1706727441, 'model': 'gpt-4-1106-vision-preview', 'usage': {'prompt_tokens': 778, 'completion_tokens': 108, 'total_tokens': 886}, 'choices': [{'message': {'role': 'assistant', 'content': "The image depicts a bank statement from JPMorgan Chase Bank, featuring customer service information, account holder details, and transaction records—the latter including a checking summary and individual transaction details with dates, descriptions, amounts, and balances.\n\nThe document outlines a financial accounting for a certain period, listing starting and ending balances, deposits, withdrawals, and individual line items for financial activity such as bill payments, check deposits, card payments, and other transactions. It's a typical format for a bank statement used to keep account holders informed of their account activity."}, 'finish_reason': 'stop', 'index': 0}]}
content = response['choices'][0]['message']['content']


# Define a function to reset the app
def reset_app():
    for key in st.session_state.keys():
        del st.session_state[key]
    st.experimental_rerun()

# Your app logic here
# ...

# Button to reset the app
if st.button('Reset App'):
    reset_app()


cutoff_date = datetime(2024, 2, 1)
expected_months = []

for i in range(1, 4):
    # Adjust the year if the month is January
    year = cutoff_date.year if cutoff_date.month > 1 else cutoff_date.year - 1
    # Adjust the month, wrap to December if current month is January
    month = cutoff_date.month - 1 if cutoff_date.month > 1 else 12
    # Get the first day of the previous month
    previous_month_date = datetime(year, month, 1)
    expected_months.append(previous_month_date.strftime('%b%Y'))
    # Update the cutoff_date for the next iteration
    cutoff_date = previous_month_date
    
    print(expected_months)

# Function to convert image file to base64
def get_image_base64(path):
    with open(path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Convert your PNG file to Base64
icon_base64 = get_image_base64("/Users/sugupta/Downloads/attention.png")

# Create HTML string with embedded Base64 encoded image

success_icon=get_image_base64("/Users/sugupta/Downloads/thumbs-up.png")

html_str = f"""
    <div style="margin: 10px 0; padding: 10px; background-color: #ffcccb; color: black; border-left: 6px solid #f44336; display: flex; align-items: center;">
        <img src="data:image/png;base64,{icon_base64}" style="width: 40px; height: 40px; margin-right: 10px;">
        <div>
            <h5 style="margin: 0;">Attention Required</h5>
            <p>Please review the errors under summary section and upload required statements.</p>
        </div>
    </div>
"""

icon_base64 = "your_base64_encoded_icon"  # Replace with your actual Base64 encoded icon string

Success_msg = f"""
    <div style="margin: 10px 0; padding: 10px; background-color: #d4edda; color: #155724; border-left: 6px solid #28a745; display: flex; align-items: center;">
        <img src="data:image/png;base64,{success_icon}" style="width: 40px; height: 40px; margin-right: 10px;">
        <div>
            <h5 style="margin: 0;">All Set!</h4>
            <p>Everything looks good. No further action is required.</p>
        </div>
    </div>
"""
st.markdown(Success_msg, unsafe_allow_html=True)
# Use this html_str in your Streamlit app
import streamlit as st
st.markdown(html_str, unsafe_allow_html=True)


st.markdown(html_str, unsafe_allow_html=True)
# html_str = f"""
#     <div style='display:flex;align-items:center;'>
#         <img src='data:image/png;base64,{icon_base64}' style='width:40px;height:40px;'>
#         <p></p>
#     </div>
#     """
st.markdown(format_text_color("This is a test message",False),unsafe_allow_html=True)
# Display in Streamlit


# Example usage with st.error
st.error("This is an error message with your custom icon: " + html_str)





def validate_document_format(json_obj: Any) -> bool:
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
        for document_type, details in item.items():
            # Check if document type is valid
            if document_type not in valid_document_types:
                return False
            # Checking if 'Is<DocumentType>' is True
            if not details.get(f'Is{document_type}', False) is True:
                return False
            # Validate FirstName and LastName
            if 'FirstName' not in details or 'LastName' not in details:
                return False
            # Validate periods
            periods_prefix = f'{document_type}Periods'
            periods = details.get(periods_prefix, {})
            for period in periods.values():
                start_date = period.get('Start', '')
                end_date = period.get('End', '')
                if not (is_valid_date(start_date) and is_valid_date(end_date)):
                    return False
    return True

documents="""{
  "PaySlip": {
    "IsPaySlip": true,
    "FirstName": "Jeffrey",
    "LastName": "Rosal",
    "PaySlipPeriods": {
      "1": {
        "Start": "01/Oct/2022",
        "End": "31/Oct/2022"
      }
    }
  }}"""
doc=json.loads(documents)
doc=[]
print(validate_document_format(doc))

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

print(validate_document_format_new(json.loads(doc)))




documents=json.loads(documents)
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
def determine_financial_year(cutoff_date):
    if cutoff_date.month > 3:  # April or later
        start_year = cutoff_date.year - 1
    else:  # January to March
        start_year = cutoff_date.year - 2
    return f"Mar{start_year + 1}",f"Apr{start_year}"


for document in documents:
    extractmonths=extract_statement_months(document,"SA302")
    print(extractmonths)
    
    
    


output=determine_financial_year(datetime.today())
print(output)

missingmonths=set(output)-set(extractmonths)
print(f"missing_months:{missingmonths}")


output=[]
doctype=["A","B","C","D"]
testdoc=["A","B","C","D"]

output=set(testdoc)-set(doctype)
if output:
    print("No Missing Values")
else:
    print(output)



for documenttype in doctype:
    if(documenttype=="A"):
        print("Yes")
    else:
        print("No")

if doctype.__contains__("A"):
    print("Yes")
else:
    print("No")