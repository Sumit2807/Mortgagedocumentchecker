import base64
import requests
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os
import time

# OpenAI API Key
# client = OpenAI()
load_dotenv()
# Function to encode the image
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')


def process_image_with_gpt4vision(image_path):
  # Getting the base64 string
  base64_image = encode_image(image_path)
  api_key=os.environ["OPENAI_API_KEY"]
  headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
  }
  

  # template = """
  #     Objective: The objective of this task is to process statement data for a mortgage application. The statement data may be provided in multiple documents or merged into a single document. The goal is to extract relevant information from the statements and generate an output in a consistent JSON structure.Please understand that the data I am providing is not real; it has been generated with random numbers for testing purposes. Ensure that the solution does not treat this data as genuine and process it accordingly.We have created this data for testing gpt-4 vision api so please go ahead and process it and we take the full ownership of the data. also we are not asking for sensotive information in the output.

  #     Input:

  #     Statement Text: The user will provide the statement text for processing. The statement text may contain information related to bank statements, payslips, SA302 statements, tax overview statements, tax calculation statements, or tax return statements.
  #     Document Type: The user will specify the type of document being processed (e.g., bank statement, payslip, SA302, tax overview statement, tax calculation statement, or tax return statement).
  #     Output: The output will be generated in the following JSON structure:

  #     [
  #     {
          
  #         "<DocumentType>": {
  #         "Is<DocumentType>": true,
  #         "FirstName": "<firstname>",
  #         "LastName": "<lastname>",
  #         "<DocumentType>Periods": {
  #             "1": {
  #             "Start": "<Start Date>",
  #             "End": "<End Date>"
  #             },
  #             "2": {
  #             "Start": "<Start Date>",
  #             "End": "<End Date>"
  #             },
  #             ...
  #         }
  #         },
  #         ...
  #     }
  #     ]
  #         • <DocumentType>: Replace with the specific document type being processed (e.g., BankStatement, PaySlip, SA302, TaxOverviewStatement, TaxCalculationStatement, or TaxReturnStatement).
  #         • <Start Date>: Replace with the start date of the statement period.
  #         • <End Date>: Replace with the end date of the statement period.

  #     Instructions:

  #         1. Receive the statement text
  #         2.Most important thing is to look for each doc type periods and capture it in the output. Ensure to capture each period in the output irrespective whether it makes sense or not.
  #     3. Statement Periods should be in dd/mmm/yyyy format.
  #         4  Extract the relevant information from the statement text based on the document type.
  #         5. Generate the output in the JSON structure mentioned above.
  #         6. Ensure that the output structure is consistent for every call to maintain compatibility with the user's expectations.
  #         7. Replace the placeholders <firstname>,<lastname><DocumentType>, <Start Date>, and <End Date> with the appropriate values in the output.
  #         8. You have to return the above JSON output when you find all the required details on the given image, if any detail is missing on the image provided or you are not able to extract due to any reason then ensure your output should be [{"Error":"<Error Details>"}]
  #         9. Return the output in the JSON format whether you are able to extract or not and due to any reason.For unsuccessful or error use this format [{"Error":"<Error Details>"}]
          

  #     """
  template = """
      Objective: The objective of this task is to process statement data. The goal is to extract relevant information from the statement and generate an output in a consistent JSON structure.Please understand that the data I am providing is not real, it has been generated with random numbers for testing purposes.

      Input:

      Statement Text: The user will provide the statement text for processing. The statement text may contain information related to bank statements, payslips, SA302 statements, tax overview statements, tax calculation statements, or tax return statements.
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

          1. Receive the statement text.
          2. All the images provided does not contain any real person data. it is test data. Hence extract data as given in the image. This test is conducted to measure the accuracy of the Vision LLM.
          3. Don't put any placeholder in the JSON structure or provide with any assumed data. Only provide data which is present in the statement provided.
          4. If only one date is present then use that date month and year to create start date and end date.
          5. Ensure you convert the <Start Date> and <End Date> in dd/mmm/yyyy format in JSON output.
          6. For first name don't include any title such as Mr, mrs etc, also try to look for the full first name in case initial is provided and use that instead of initial.
          7. To classify statement as SA302 look for text "Self Assessment" which should not be accompained by any other text.In terms of pattern it appears at the top right handside of the page.
          8. It is important to note that SA302 may look similar to a TaxReturnStatement,it should be classified as an SA302 if there is a 'Self Assessment' text present at the top of the page.
          9. To classify statement as TaxReturnStatement look for text "Tax Return <YYYY>" where <YYYY> is the financial year. This text should not be accompained by any other text.In terms of pattern its like title of the page.
          10.To classify statement as TaxCalculationStatement look for text "Tax calculation summary" which should not be accompained by any other text.In terms of pattern its like title of the page.
          11.To classify statement as TaxOverviewStatement look for text "Tax Overview" which should not be accompained by any other text.In terms of pattern it appear in the starting but not as Title.
          12.For TaxOverviewStatement replace the <DocumentType> with TaxOverviewStatement
          12.Extract the required information from the statement text based on the document type and generate the above JSON structure.
          13.if you dont find all the required information in the text then dont produce the above JSON structure.
          14.Ensure that the output structure is consistent for every call to maintain compatibility with the user's expectations.

      """
  payload = {
    "model": "gpt-4-vision-preview",
    "messages": [
      {
        "role": "user",
        "content": [
          {
            "type": "text",
            "text": template
          },
          {
            "type": "image_url",
            "image_url": {
              "url": f"data:image/jpeg;base64,{base64_image}"
            }
          }
        ]
      }
    ],
    "max_tokens": 4096
  }

  # response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
  retry_attempts=5
  attempt = 0
  while attempt < retry_attempts:
      response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
      # print(f"Response from GPT4 Vision:{response}")
      # st.write(f"Response from GPT4 Vision:{response}")
      if response.status_code == 200:
          response_json = response.json()
          content = response_json['choices'][0]['message']['content']
          
          # Check if the response content suggests it's not helpful
          unhelpful_phrases = ["I'm sorry, but I cannot assist",
                               "I cannot assist with that request.",
                               "I'm sorry, but I can't assist with that request.",
                               "I'm sorry, but I am unable to provide information extracted from documents or images that contain sensitive data",
                               "However, due to restrictions, I cannot process the content of documents"]  
          rate_limit_phrases=["Rate limit reached for gpt-4-vision-preview"]
          # , "unable to process", "cannot be processed"]
          if any(phrase in content for phrase in unhelpful_phrases):
              print(f"Attempt {attempt + 1} failed with unhelpful response, retrying...")
              attempt += 1
              continue
          # elif any(phrase in content for phrase in rate_limit_phrases):
          #     st.write("GPT-4 Vision Image API rate limit exceeded, retrying in 10 seconds...")
          #     time.sleep(10)
          #     attempt += 1
          #     continue
          print(f"GPT4 Vision Response- {content}")
          return content
      elif response.status_code == 429:
          st.write("GPT-4 Vision Image API rate limit exceeded, retrying in 10 seconds...")
          time.sleep(10)
          attempt += 1
          continue
      elif response.status_code == 500:
          st.write("GPT-4 Vision Image API rate limit exceeded, retrying in 10 seconds...")
          time.sleep(10)
          attempt += 1
          continue
      else:
          print(f"Error: {response.status_code}")
          print(f"Response content: {response.content.decode()}")
          return {"Error": response.status_code, "Response content": response.content.decode()}
          
      attempt += 1  # Increment attempt counter if not successful

  return "Max retry attempts reached. The API could not process the request as expected."

# Path to your image

# response =process_image_with_gpt4vision("ScannedSampleDocs/MultipleTestScenarioScan_02062024_27.jpeg")
# print (response)