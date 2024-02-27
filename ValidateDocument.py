import json
from datetime import datetime, timedelta

# Sample JSON data
json_data = '''{
    "IsBankStatement": false,
    "IsPaySlip": false,
    "IsSA302Statement": false,
    "IsTaxOverviewStatement": true,
    "IsFullAccountsStatement": false,
    "FirstName": "Betty",
    "LastName": "Downing",
    "MultipleStatement": false,
    "StatementPeriod": {
        "1": {
            "Start": "01/08/2023",
            "End": "31/08/2023"
        }
    }
}
'''

def is_valid_document(document):
    required_keys = ["FirstName", "LastName", "MultipleStatement", "StatementPeriod"]
    doc_type_keys = ["IsBankStatement", "IsPaySlip", "IsSA302Statement", "IsTaxOverviewStatement", "IsFullAccountsStatement"]
    
    # Check for required keys
    if not all(key in document for key in required_keys):
        return False
    
    # Check for at least one document type key
    if not any(key in document for key in doc_type_keys):
        return False

    # Check StatementPeriod structure
    statement_period = document["StatementPeriod"]
    if document["MultipleStatement"]:
        # For multiple statements, StatementPeriod should have nested dictionaries
        if not isinstance(statement_period, dict) or not all(isinstance(period, dict) and 'Start' in period and 'End' in period for period in statement_period.values()):
            return False
    else:
        # For a single statement, StatementPeriod can be either a dictionary with "Start" and "End", or have a nested structure like in multiple statements
        if not isinstance(statement_period, dict) or (not ('Start' in statement_period and 'End' in statement_period) and not all(isinstance(period, dict) and 'Start' in period and 'End' in period for period in statement_period.values())):
            return False

    return True


def determine_financial_year(cutoff_date):
    if cutoff_date.month > 3:  # April or later
        start_year = cutoff_date.year - 1
    else:  # January to March
        start_year = cutoff_date.year - 2
    return f"April {start_year}", f"March {start_year + 1}"

def process_statement_period(document, user_first_name, user_last_name, expected_months, financial_year):
    first_name = document["FirstName"]
    last_name = document["LastName"]
    multiple_statement = document["MultipleStatement"]
    statement_periods = []

    # Extract document types
    doc_types = [key.replace('Is', '').replace('BankStatement', 'Bank Statement').replace('PaySlip', 'Pay Slip').replace('SA302Statement', 'SA302 Statement').replace('TaxOverviewStatement', 'Tax Overview Statement').replace('FullAccountsStatement', 'Full Accounts Statement') for key, value in document.items() if key.startswith('Is') and value]

    if multiple_statement or ('1' in document["StatementPeriod"]):
        for period in document["StatementPeriod"].values():
            statement_periods.append(period)
    else:
        statement_periods.append(document["StatementPeriod"])

    valid_periods = []
    for period in statement_periods:
        start_month_year = datetime.strptime(period["Start"], '%d/%m/%Y').strftime('%B %Y')
        end_month_year = datetime.strptime(period["End"], '%d/%m/%Y').strftime('%B %Y')

        name_valid = (first_name == user_first_name) and (last_name == user_last_name)
        type_valid = any(doc_type in doc_types for doc_type in doc_types_for_validation)
        
        period_valid = False
        if any(document.get(key) for key in ["IsPaySlip", "IsBankStatement"]):
            period_valid = start_month_year in expected_months or end_month_year in expected_months
        elif any(document.get(key) for key in ["IsSA302Statement", "IsTaxOverviewStatement"]):
            fy_start, fy_end = financial_year
            period_valid = fy_start in start_month_year or fy_end in end_month_year

        valid = name_valid and type_valid and period_valid
        valid_periods.append(valid)

    return name_valid,type_valid,period_valid, valid_periods, ', '.join(doc_types)


# List of document types for final validation
doc_types_for_validation = ["Bank Statement", "Pay Slip"]  # Add more types as needed

# Main code
user_first_name = "Betty"
user_last_name = "Downing"
cutoff_date = datetime.today()
expected_months = [(cutoff_date - timedelta(days=30*i)).strftime('%B %Y') for i in range(3)]
financial_year = determine_financial_year(cutoff_date)
try:
    doc = json.loads(json_data)
    documents=[doc]
except json.JSONDecodeError:
    print("Invalid document format provided, please check.")
    documents = []
doc_summary = {doc_type: {'valid_months': set(), 'invalid_months': set()} for doc_type in doc_types_for_validation}
if not is_valid_document(documents):
        print("1. Invalid document format provided, please check.")
        # move to next document
for document in documents:
    namevalid,doctypevalid,statementperiodvalid,valid_periods, document_types = process_statement_period(document, user_first_name, user_last_name, expected_months, financial_year)
    all_valid = all(valid_periods)
    print(f"Document: {document}")
    print(f"Document Type: {document_types}")
    print(f"Document Type: {'Valid' if doctypevalid else 'Invalid'}")
    print(f"Name Check: {'Valid' if namevalid else 'No'}")
    print(f"Statement Period: {'Valid' if statementperiodvalid else 'Statement is not within required timeframe'}")

    for doc_type in doc_types_for_validation:
        if all_valid:
            doc_summary[doc_type]['valid_months'].update(
                [datetime.strptime(period["Start"], '%d/%m/%Y').strftime('%B %Y') for period in document["StatementPeriod"].values()]
            )

# Summarize document validation
for doc_type in doc_types_for_validation:
    summary = doc_summary[doc_type]
    if 'Pay Slip' == doc_type or 'Bank Statement' == doc_type:
        missing = set(expected_months) - summary['valid_months']
    else:  # SA302 or Tax Overview
        missing = {financial_year[0], financial_year[1]} - summary['valid_months']
    if missing:
        print(f"{doc_type} missing for: {', '.join(missing)}")
    else:
        print(f"{doc_type} provided for all required periods.")
