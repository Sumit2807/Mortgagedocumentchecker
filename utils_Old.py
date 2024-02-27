# from langchain.llms import OpenAI
from pypdf import PdfReader
# from langchain.llms.openai import OpenAI
import pandas as pd
import re
#import replicate
import json
# from langchain.prompts import PromptTemplate
# from langchain.chat_models import ChatOpenAI
# from langchain.chains import LLMChain
from openai import OpenAI

#Extract Information from PDF file
def get_pdf_text(pdf_doc):
    text = ""
    pdf_reader = PdfReader(pdf_doc)
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text



#Function to extract data from text
def extracted_data(pages_data):
    client = OpenAI()


    template = """
    Please analyse the provided bank statement text and extract the relevant data as per below instructions. Determine the following details: IsBankStatement (TrueorFalse),IsPayslip (TrueorFalse),ISSA302Form (TrueorFalse),IsTaxOverviewStatement (TrueorFalse), IsFullAccountsStatement (TrueorFalse), The first name of the account holder. The last name of the account holder. Whether the text contains multiple statements (True/False). The statement period(s) with specific dates in 'dd/mm/yyyy' format. Summarize the extracted data in a clear and structured JSON format. Make sure the JSON output includes following keys: 'IsBankStatement','IsPaySlip','IsSA302Statement', 'IsTaxOverviewStatement','FirstName', 'LastName', 'MultipleStatement', and 'StatementPeriod', with nested keys for each statement period if there are multiple. Ensure accuracy and clarity in the presentation of the data. Here is sample JSON output for a bankstatement with multiple period. This is just for reference purpose only. To create the output you should analyse the text provided :
    [
    "IsBankStatement": true,
    "IsPaySlip": false,
    "IsSA302Statement": false,
    "IsTaxOverviewStatement": false,
    "IsFullAccountsStatement": false,
    "FirstName": "John",
    "LastName": "Doe",
    "MultipleStatement": true,
    "StatementPeriods": [
    [
      "Period": "01/01/2023 - 31/01/2023"
    ],
    [
      "Period": "01/02/2023 - 28/02/2023"
    ],
    ]
      "Period": "01/03/2023 - 31/03/2023"
    ]
    ]
    ]
        """
    print(template)
    print(pages_data)
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        response_format={ "type": "json_object" },
        messages=[
        {"role": "system", "content": template},
        {"role": "user", "content": pages_data}
        ]
        )
    full_response=response.choices[0].message.content

    
    return full_response


# iterate over files in
# that user uploaded PDF files, one by one
def create_docs(user_pdf_list):
    
    for filename in user_pdf_list:
        
        print(filename)
        raw_data=get_pdf_text(filename)
        # print(raw_data)
        # #print("extracted raw data")

        llm_extracted_data=extracted_data(raw_data)
        print(llm_extracted_data)
        #Adding items to our list - Adding data & its metadata
        data = llm_extracted_data
        data=json.loads(llm_extracted_data)
        print("Assigned llm data to data variable")
        
  

        try:
            # Create a DataFrame from the JSON data
            
            df=pd.json_normalize(data)
            
            print (df)
            return df

            # Print the DataFrame in tabular format

        except Exception as e:
            print("Error:", str(e))
            return e
        
        
        
pdffiles=["/Users/sugupta/Downloads/John Wick - October 2023.pdf"]
create_docs(pdffiles)

        
if __name__ == "__main__":
    {}    

        
    