import streamlit as st
from dotenv import load_dotenv
from utils import *
import os
import json
from datetime import datetime, timedelta
from dotenv import load_dotenv
from Test_OpenAIAPIDirectCall import *


load_dotenv()

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
employment_options = ["Salaried", "Self Employed"]
with st.form(key='mortgage_form'):
    first_name = st.text_input("First Name")
    last_name = st.text_input("Last Name")
    Employer = st.text_input("Employer Name or Self-Employed Business Name")
    employment_type = st.radio("Employment Type?", employment_options)
    # dob = st.text_input("Date of Birth (DD-MM-YYYY)")
    # Uncomment and use the following fields as needed
    # current_address = st.text_area("Current Address")
    # purchase_property_address = st.text_area("Purchase Property Address")
    # purchase_property_price = st.text_input("Purchase Property Price(£)")
    # deposit_amount = st.text_input("Deposit Amount(£)")
    # term = st.number_input("Term (in years)", min_value=1, step=1)
    # property_valuation = st.text_input("Property valuation (£)")
    uploaded_files = st.file_uploader("Upload Supporting Documents", accept_multiple_files=True, type=["pdf", "jpeg", "png"])
    submit_button = st.form_submit_button("Submit")

# Place the Reset button outside the form
# if st.button('Reset App'):
#     reset_app()



# Process files upon form submission
# uploaded_files=[]
# first_name="Bob"
# last_name="Johnson"

Overall_DocumentTypes=[]
Overall_BankStatementPeriods=[]
Overall_PayslipPeriods=[]
Overall_SA302Periods=[]
Overall_TaxOverviewStatementPeriods=[]
Overall_TaxCalculationStatementPeriods=[]
Overall_TaxReturnStatementPeriods=[]
if submit_button and uploaded_files:
    for uploaded_file in uploaded_files:
        print(f"Processing file- {uploaded_file.name}")
        # Check file type and process accordingly
        # print("UploadedFile Value- {uploaded_file}")
        
        if is_digital_pdf(uploaded_file):
            # List of document types for final validation
            if employment_type=="Salaried":
                doc_types_for_validation = ["BankStatement", "PaySlip"]  # Add more types as needed
            else:
                doc_types_for_validation = ["SA302", "BankStatement","TaxOverviewStatement","TaxCalculationStatement","TaxReturnStatement"]  # Add more types as needed
            
            
            # extracted_data =   get_pdf_text(uploaded_file)
            Statement_data=get_statement_text(uploaded_file)
            extracted_data=call_gpt4preview(Statement_data)
            user_first_name = first_name
            user_last_name = last_name
            # cutoff_date = datetime.today()
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
                financial_year = determine_financial_year(cutoff_date)
            try:
                    doc = json.loads(extracted_data)
                    documents=[doc] # This may not be required as output from GPT4 should be a JSON object 
            except json.JSONDecodeError:
                    file_name = f"File Name- {uploaded_file.name.strip()}"        
                    st.error(file_name)
                    st.markdown(format_status(False, "Invalid document format provided, please check.", "Invalid document format provided, please check.", "Error"), unsafe_allow_html=True)
                    print("Document Type: Invalid")
                    st.markdown("\n")
                    st.markdown("\n")
                    st.markdown("\n")
                    st.markdown("\n")
                    st.markdown("\n")
                    documents = []
                    continue
            # doc_summary = {doc_type: {'valid_months': set(), 'invalid_months': set()} for doc_type in doc_types_for_validation}
            if not validate_document_format_new(documents):
                        file_name = f"File Name- {uploaded_file.name.strip()}"        
                        st.error(file_name)
                        st.markdown(format_status(False, "Invalid document format provided, please check.", "Invalid document format provided, please check.", "Error"), unsafe_allow_html=True)
                        print("Document Type: Invalid")
                        st.markdown("\n")
                        st.markdown("\n")
                        st.markdown("\n")
                        st.markdown("\n")
                        st.markdown("\n")
                        # st.error("Invalid document format provided, please check.",icon="🚨")
                        continue
            else:
                Current_DocumentTypes=[]
                Current_BankStatementPeriods=[]
                Current_PayslipPeriods=[]
                Current_SA302Periods=[]
                Current_TaxOverviewStatementPeriods=[]
                Current_TaxCalculationStatementPeriods=[]
                Current_TaxReturnStatementPeriods=[]
                
                for document in documents:
                        for doc_type, doc_data in document.items():
                            if doc_type in doc_types_for_validation and doc_data.get("FirstName", "").strip().lower() == user_first_name.strip().lower() and doc_data.get("LastName", "").strip().lower() == user_last_name.strip().lower():
                            # Perform further actions or processing for the matching document
                                print(f"Processing {doc_type} for {user_first_name} {user_last_name}")
                                print("Document data:", doc_data)
                                Current_DocumentTypes.append(doc_type)
                                months = extract_statement_months(document, doc_type)
                                print(f"Months Returned by Function: {months}")
                                if doc_type=="BankStatement":
                                    Current_BankStatementPeriods.extend(months)
                                elif doc_type=="PaySlip":
                                    Current_PayslipPeriods.extend(months)
                                elif doc_type=="SA302":
                                    Current_SA302Periods.extend(months)
                                elif doc_type=="TaxOverviewStatement":
                                    Current_TaxOverviewStatementPeriods.extend(months)
                                elif doc_type=="TaxCalculationStatement":
                                    Current_TaxCalculationStatementPeriods.extend(months)
                                elif doc_type=="TaxReturnStatement":
                                    Current_TaxReturnStatementPeriods.extend(months)        
                            else:
                                continue
                if Current_DocumentTypes==[]:
                    file_name = f"File Name- {uploaded_file.name.strip()}"
                    st.error(file_name)
                    print(f"FileName-{file_name}  ")
                    st.markdown(format_status(False, "Valid", "Invalid", "Document Type"), unsafe_allow_html=True)
                    print("Document Type: Invalid")
                    print("Name Check: Name on statement does not match with name provided on mortgage application form")
                    st.markdown(format_status(False, "Valid", "Name on statement does not match with name provided on mortgage application form", "Name Check"), unsafe_allow_html=True)
                    st.markdown("\n")
                    st.markdown("\n")
                    st.markdown("\n")
                    st.markdown("\n")
                    st.markdown("\n")
                else:
                    file_name = f"File Name- {uploaded_file.name.strip()}"
                    print(f"FileName-{file_name}  ")
                    st.markdown(format_text_color(file_name,True), unsafe_allow_html=True) 
                    print(f"Name Check:Valid")
                    st.markdown(format_status(True, "Valid", "Name on statement does not match with name provided on mortgage application form", "Name Check"), unsafe_allow_html=True)
                    print(f"Document Type:{Current_DocumentTypes}")
                    st.markdown(format_status(True, Current_DocumentTypes, Current_DocumentTypes, "Document Type"), unsafe_allow_html=True)
                    Overall_DocumentTypes.append(Current_DocumentTypes)
                    if Current_BankStatementPeriods!=[]:
                        output=f"Bank Statement Periods:{Current_BankStatementPeriods}"
                        print(output)
                        Overall_BankStatementPeriods.extend(Current_BankStatementPeriods)
                        st.markdown(format_status(True, Current_BankStatementPeriods, Current_BankStatementPeriods, "Bank Statement Periods"), unsafe_allow_html=True)
                    if Current_PayslipPeriods!=[]:
                        output=f"PaySlip Periods:{Current_PayslipPeriods}"
                        print(output)
                        st.markdown(format_status(True, Current_PayslipPeriods, Current_PayslipPeriods, "PaySlip Periods"), unsafe_allow_html=True)
                        Overall_PayslipPeriods.extend(Current_PayslipPeriods)
                    if Current_SA302Periods!=[]:
                        output=f"SA302 Statement Periods:{Current_SA302Periods}"
                        print(output)
                        st.markdown(format_status(True, Current_SA302Periods, Current_SA302Periods, "PaySlip Periods"), unsafe_allow_html=True)
                        Overall_SA302Periods.extend(Current_SA302Periods)
                    if Current_TaxOverviewStatementPeriods!=[]:
                        output=f"Tax Overview Statement Periods:{Current_TaxOverviewStatementPeriods}"
                        print(output)
                        st.markdown(format_status(True, Current_TaxOverviewStatementPeriods, Current_TaxOverviewStatementPeriods, "Tax Overview Statement Periods"), unsafe_allow_html=True)
                        Overall_TaxOverviewStatementPeriods.extend(Current_TaxOverviewStatementPeriods)
                    if Current_TaxCalculationStatementPeriods!=[]:
                        output=f"Tax Calculation Statement Periods:{Current_TaxCalculationStatementPeriods}"
                        print(output)
                        st.markdown(format_status(True, Current_TaxCalculationStatementPeriods, Current_TaxCalculationStatementPeriods, "Tax Calculation Statement Periods"), unsafe_allow_html=True)
                        Overall_TaxCalculationStatementPeriods.extend(Current_TaxCalculationStatementPeriods)
                    if Current_TaxReturnStatementPeriods!=[]:
                        output=f"Tax Return Statement Periods:{Current_TaxReturnStatementPeriods}"
                        print(output)
                        st.markdown(format_status(True, Current_TaxReturnStatementPeriods, Current_TaxReturnStatementPeriods, "Tax Return Statement Periods"), unsafe_allow_html=True)
                        Overall_TaxReturnStatementPeriods.extend(Current_TaxReturnStatementPeriods)
                    print("\n")
                    print("\n")
                    print("\n")
                    print("\n")
                    st.markdown("\n")
                    st.markdown("\n")
                    st.markdown("\n")
                    st.markdown("\n")
                    st.markdown("\n")
        else:
            file_name = f"File Name- {uploaded_file.name.strip()}"        
            st.error(f"{file_name}")
            st.markdown(format_status(False, "Invalid picture or document provided", "Invalid picture or document provided", "Error"), unsafe_allow_html=True)
            st.markdown("\n")
            st.markdown("\n")
            st.markdown("\n")
            st.markdown("\n")
            st.markdown("\n")
    
    
    st.markdown("\n")
    st.markdown("\n")
    st.markdown("\n")
    st.markdown("\n")
    st.markdown("\n")
    print("Final Summary-")
    all_checks_passed=""
    st.markdown(format_text_color("Final Summary",True), unsafe_allow_html=True)
    for documenttype in doc_types_for_validation:
        if(documenttype=="BankStatement"):
            missing_periods=[]
            missing_periods=set(expected_months)-set(Overall_BankStatementPeriods)
            if missing_periods:
                all_checks_passed=False
                error_msg=f"Bank Statements: Please upload for the following periods:{missing_periods}"
                print(error_msg)
                st.markdown(format_status(False,f"Please upload for the following periods:{missing_periods}" ,f"Please upload for the following periods:{missing_periods}", "Bank Statements"), unsafe_allow_html=True)
            else:
                print("Bank Statements: Received successfully")
                if all_checks_passed=="" or all_checks_passed==True:
                    all_checks_passed=True
                st.markdown(format_status(True,"Received successfully" ,"Received successfully", "Bank Statements"), unsafe_allow_html=True)
        if(documenttype=="PaySlip"):
            missing_periods=[]
            missing_periods=set(expected_months)-set(Overall_PayslipPeriods)
            if missing_periods:
                all_checks_passed=False
                print(f"PaySlip: Please upload for the following periods:{missing_periods}")
                st.markdown(format_status(False,f"Please upload for the following periods:{missing_periods}" ,f"Please upload for the following periods:{missing_periods}", "PaySlips"), unsafe_allow_html=True)
            else:
                if all_checks_passed=="" or all_checks_passed==True:
                    all_checks_passed=True
                print("Payslips: Received successfully")
                st.markdown(format_status(True,"Received successfully" ,"Received successfully", "PaySlips"), unsafe_allow_html=True)
        if(documenttype=="SA302"):
            missing_periods=[]
            missing_periods=set(financial_year)-set(Overall_SA302Periods)
            if missing_periods:
                all_checks_passed=False
                print(f"SA302: Please upload for the following periods:{missing_periods}")
                st.markdown(format_status(False,f"Please upload for the following periods:{missing_periods}" ,f"Please upload for the following periods:{missing_periods}", "SA302 Statement"), unsafe_allow_html=True)
            else:
                if all_checks_passed=="" or all_checks_passed==True:
                    all_checks_passed=True
                print("SA302: Received successfully")
                st.markdown(format_status(True,"Received successfully" ,"Received successfully", "SA302 Statements"), unsafe_allow_html=True)
        if(documenttype=="TaxOverviewStatement"):
            missing_periods=[]
            missing_periods=set(financial_year)-set(Overall_TaxOverviewStatementPeriods)
            if missing_periods:
                all_checks_passed=False
                print(f"Tax Overview Statement: Please upload for the following periods:{missing_periods}")
                st.markdown(format_status(False,f"Please upload for the following periods:{missing_periods}" ,f"Please upload for the following periods:{missing_periods}", "Tax Overview Statement"), unsafe_allow_html=True)
            else:
                if all_checks_passed=="" or all_checks_passed==True:
                    all_checks_passed=True
                print("Tax Overview Statement: Received successfully")
                st.markdown(format_status(True,"Received successfully" ,"Received successfully", "Tax Overview Statement"), unsafe_allow_html=True)
        if(documenttype=="TaxCalculationStatement"):
            missing_periods=[]
            missing_periods=set(financial_year)-set(Overall_TaxCalculationStatementPeriods)
            if missing_periods:
                all_checks_passed=False
                print(f"Tax Calculation Statement: Please upload for the following periods:{missing_periods}")
                st.markdown(format_status(False,f"Please upload for the following periods:{missing_periods}" ,f"Please upload for the following periods:{missing_periods}", "Tax Calculation Statement"), unsafe_allow_html=True)
            else:
                if all_checks_passed=="" or all_checks_passed==True:
                    all_checks_passed=True
                print("Tax Calculation Statement: Received successfully")
                st.markdown(format_status(True,"Received successfully" ,"Received successfully", "Tax Calculation Statement"), unsafe_allow_html=True)
        if(documenttype=="TaxReturnStatement"):
            missing_periods=[]
            missing_periods=set(financial_year)-set(Overall_TaxReturnStatementPeriods)
            if missing_periods:
                all_checks_passed=False
                print(f"Tax Return Statement: Please upload for the following periods:{missing_periods}")
                st.markdown(format_status(False,f"Please upload for the following periods:{missing_periods}" ,f"Please upload for the following periods:{missing_periods}", "Tax Return Statement"), unsafe_allow_html=True)
            else:
                if all_checks_passed=="" or all_checks_passed==True:
                    all_checks_passed=True
                print("Tax Return Statement: Received successfully")
                st.markdown(format_status(True,"Received successfully" ,"Received successfully", "Tax Return Statement"), unsafe_allow_html=True)
                
    st.markdown("\n")
    st.markdown("\n")
    st.markdown("\n")
    st.markdown("\n")
    
    if all_checks_passed:
        success_icon=get_image_base64("Icons/thumbs-up.png")
        Success_msg = f"""
        <div style="margin: 10px 0; padding: 10px; background-color: #d4edda; color: #155724; border-left: 6px solid #28a745; display: flex; align-items: center;">
            <img src="data:image/png;base64,{success_icon}" style="width: 40px; height: 40px; margin-right: 10px;">
            <div>
                <h5 style="margin: 0;">All Set!</h5>
                <p>Everything looks good. No further action is required.</p>
            </div>
        </div>
        """
        st.markdown(Success_msg, unsafe_allow_html=True)  
    else:
        # Convert your PNG file to Base64
        attention_icon = get_image_base64("Icons/attention.png")

        # Create HTML string with embedded Base64 encoded image



        Error_msg = f"""
            <div style="margin: 10px 0; padding: 10px; background-color: #ffcccb; color: black; border-left: 6px solid #f44336; display: flex; align-items: center;">
                <img src="data:image/png;base64,{attention_icon}" style="width: 40px; height: 40px; margin-right: 10px;">
                <div>
                    <h5 style="margin: 0;">Attention Required</h5>
                    <p>Please review the errors under summary section and upload required statements.</p>
                </div>
            </div>
        """

        st.markdown(Error_msg, unsafe_allow_html=True)         