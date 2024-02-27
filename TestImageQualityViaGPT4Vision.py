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
      Objective: The objective is to classify the quality of the image in to High, medium and low. Please see below instructions on how to classify it and also output format:
      
      Instructions:
      
      
        1.Low:

            1.1 Look for images that have visible distortions, artifacts, or pixelation.
            1.2 Check for blurry or out-of-focus images.
            1.3 Identify images with poor lighting or exposure.
            1.4 Consider images with low resolution.

        2.Medium:

            2.1 Look for images that are reasonably clear and well-defined.
            2.2 Check for minor imperfections or noise that do not significantly impact the overall quality.
            2.3 Consider images with average lighting and exposure.
            2.4 Identify images with moderate resolution.

        3.High:

            3.1 Look for images that are sharp, clear, and well-defined.
            3.2 Check for minimal or no imperfections, noise, or artifacts.
            3.3 Consider images with excellent lighting and exposure.
            3.4 Identify images with high resolution.
            
        4.Unknown:
            4.1 Dont make any assumptions. if you can't classify then categorize it as Unknown. 
      
      Output Format: 
        It should be JSON with no additional text as per below format.
      
              {"Low":<BooleanValue>,
              "Medium":<BooleanValue>,
              "High":<BooleanValue>,
              "Unknown":<BooleanValue>}
              
              In above JSON format replace the <BooleanValue> with True or False based on the instructions
            
  
      
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
        #   st.write("GPT-4 Vision Image API rate limit exceeded, retrying in 10 seconds...")
          time.sleep(10)
          attempt += 1
          continue
      elif response.status_code == 500:
        #   st.write("GPT-4 Vision Image API rate limit exceeded, retrying in 10 seconds...")
          time.sleep(10)
          attempt += 1
          continue
      else:
          print(f"Error: {response.status_code}")
          print(f"Response content: {response.content.decode()}")
          return {"Error": response.status_code, "Response content": response.content.decode()}
          
      attempt += 1  # Increment attempt counter if not successful

  return {"Error": response.status_code, "Response content": response.content.decode()}

# Path to your image

response =process_image_with_gpt4vision("/Users/sugupta/Natwest_Document_Checker_Updated/ScannedSampleDocs/17078380550366512313106012722704.jpg")
print (response)